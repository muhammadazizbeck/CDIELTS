# views.py — faqat FreeDictionaryAPIView ni quyidagiga almashtiring
import asyncio
import aiohttp
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
import hashlib


class FreeDictionaryAPIView(APIView):

    # Har bir foydalanuvchi uchun alohida kesh (ixtiyoriy, xohlamasangiz o‘chirib qo‘ying)
    # @method_decorator(vary_on_headers("Authorization"))
    @method_decorator(cache_page(60 * 60 * 24 * 30))  # 30 kun kesh
    def get(self, request):
        word = request.GET.get('q', '').strip().lower()
        if not word:
            return Response({"error": "So‘z kiriting: ?q=apple"}, status=status.HTTP_400_BAD_REQUEST)

        # Kesh kalitini yaratamiz
        cache_key = f"dict_{hashlib.md5(word.encode()).hexdigest()}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)  # Tezlik: 0.01 sek!

        # Yangi so‘rov – async bilan parallel ishlaymiz
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.fetch_word_data(word))
        loop.close()

        # Natijani keshga joylaymiz
        cache.set(cache_key, result, 60 * 60 * 24 * 30)

        return Response(result)

    async def fetch_word_data(self, word):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            # 1. Inglizcha ma'lumot olish
            dict_task = asyncio.create_task(self.fetch_dictionaryapi(session, word))

            # 2. Agar kerak bo‘lsa – o‘zbekchadan inglizchaga tarjima
            eng_word = word
            if not word.replace(" ", "").isascii():  # o‘zbekcha harflar bor
                eng_word = await self.translate_uz_to_en_async(session, word)
                if not eng_word:
                    return {"found": False, "message": "Tarjima topilmadi"}
                dict_task = asyncio.create_task(self.fetch_dictionaryapi(session, eng_word))

            eng_data = await dict_task
            if not eng_data:
                return {"found": False, "message": "So‘z topilmadi"}

            # Tarjimalar parallel olinadi
            uzbek_word = await self.translate_en_to_uz_async(session, eng_data["word"])
            def_uz = await self.translate_en_to_uz_async(session, eng_data["definition"])
            example_uz = await self.translate_en_to_uz_async(session, eng_data["example"]) if eng_data["example"] else None

            return {
                "found": True,
                "searched_word": word,
                "english": eng_data["word"],
                "uzbek": uzbek_word or word,
                "part_of_speech": eng_data["part_of_speech"],
                "definition_en": eng_data["definition"],
                "definition_uz": def_uz or "[Tarjima xatosi]",
                "example_en": eng_data["example"],
                "example_uz": example_uz,
                "phonetic": eng_data["phonetic"]
            }

    async def fetch_dictionaryapi(self, session, word):
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        try:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                item = data[0]
                meaning = item["meanings"][0]
                defin = meaning["definitions"][0]
                return {
                    "word": item["word"],
                    "part_of_speech": meaning.get("partOfSpeech", "noun"),
                    "definition": defin["definition"],
                    "example": defin.get("example"),
                    "phonetic": item.get("phonetic") or item.get("phonetics", [{}])[0].get("text", "")
                }
        except:
            return None

    async def translate_en_to_uz_async(self, session, text):
        if not text:
            return None
        try:
            url = "https://api.mymemory.translated.net/get"
            async with session.get(url, params={"q": text, "langpair": "en|uz"}) as resp:
                data = await resp.json()
                return data["responseData"]["translatedText"]
        except:
            return "[Tarjima xatosi]"

    async def translate_uz_to_en_async(self, session, text):
        try:
            url = "https://api.mymemory.translated.net/get"
            async with session.get(url, params={"q": text, "langpair": "uz|en"}) as resp:
                data = await resp.json()
                return data["responseData"]["translatedText"].strip().lower()
        except:
            return None