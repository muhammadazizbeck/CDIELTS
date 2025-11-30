from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from writing.models import WritingTask2,WritingTask1
from writing.serializers import WritingTask1Serializer,WritingTask2Serializer

import google.generativeai as genai
import json, re
from django.conf import settings

class WritingTask1APIView(APIView):
    def get(self,request):
        writings1 = WritingTask1.objects.all()
        serializer = WritingTask1Serializer(writings1,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class WritingTask1RetrieveAPIView(APIView):
    def get(self,request,pk):
        writing1 = WritingTask1.objects.get(pk=pk)
        serializer = WritingTask1Serializer(writing1)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
class WritingTask2APIView(APIView):
    def get(self,request):
        writings2 = WritingTask2.objects.all()
        serializer = WritingTask2Serializer(writings2,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class WritingTask2RetrieveAPIView(APIView):
    def get(self,request,pk):
        writing2 = WritingTask2.objects.get(pk=pk)
        serializer = WritingTask2Serializer(writing2)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


class CheckTask1APIView(APIView):
    def post(self, request):
        report = request.data.get("report", "").strip()
        if not report:
            return Response({"error": "Insho matni yuborilmagan"}, status=status.HTTP_400_BAD_REQUEST)

        word_count = len(report.split())
        if word_count < 150:
            return Response({
                "error": f"Task 1 kamida 150 so‘z bo‘lishi kerak. Hozir: {word_count} so‘z"
            }, status=status.HTTP_400_BAD_REQUEST)

        task = WritingTask1.objects.last()
        if not task:
            return Response({"error": "Task 1 topilmadi. Admin panelda yarating"}, status=status.HTTP_404_NOT_FOUND)

        prompt = f"""Siz tajribali IELTS Writing Task 1 rasmiy examinerisiz.
            Hozir talaba javobini rasmiy band descriptorlar bo‘yicha diqqat bilan o‘qib, baholang.

            Grafik sarlavhasi: {task.title}
            So‘z soni: {word_count}

            Talaba javobi:
            {report}

            Endi har bir mezon bo‘yicha alohida band bering (0.0, 0.5, 1.0 … 9.0 gacha).
            Javobni faqat quyidagi JSON formatda, o‘zbek tilida qaytaring. Hech qanday qo‘shimcha matn, izoh yoki belgilar yozmang!

            {{
            "overall": BAND,
            "task_achievement": BAND,
            "coherence_and_cohesion": BAND,
            "lexical_resource": BAND,
            "grammatical_range_and_accuracy": BAND,
            "feedback": "2-3 ta jumladan iborat qisqa maslahat."
            }}
            """
        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,          
                    "max_output_tokens": 1000,
                    "top_p": 0.8,
                    "top_k": 40
                }
            )
            text = response.text.strip()

            json_match = re.search(r"\{.*\}", text, re.DOTALL)
            if not json_match:
                return Response({"error": "Gemini noto‘g‘ri format berdi", "raw": text}, status=500)

            result = json.loads(json_match.group())

            
            scores = [
                result["task_achievement"],
                result["coherence_and_cohesion"],
                result["lexical_resource"],
                result["grammatical_range_and_accuracy"]
            ]
            avg = sum(scores) / 4
            result["overall"] = round(avg * 2) / 2   

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "Server xatosi", "detail": str(e)}, status=500)


# TASK 2 tekshirish
class CheckTask2APIView(APIView):
    def post(self, request):
        report = request.data.get("report", "").strip()
        if not report:
            return Response({"error": "Insho matni yuborilmagan"}, status=400)

        word_count = len(report.split())
        if word_count < 250:
            return Response({
                "error": f"Task 2 kamida 250 so‘z (tavsiya 250+) bo‘lishi kerak. Hozir: {word_count}"
            }, status=400)

        task = WritingTask2.objects.last()
        if not task:
            return Response({"error": "Task 2 topilmadi"}, status=404)

        prompt = f"""Siz tajribali IELTS Writing Task 2 rasmiy examinerisiz.
            Hozir talaba javobini rasmiy band descriptorlar bo‘yicha diqqat bilan o‘qib, baholang.

            Grafik sarlavhasi: {task.title}
            So‘z soni: {word_count}

            Talaba javobi:
            {report}

            Endi har bir mezon bo‘yicha alohida band bering (0.0, 0.5, 1.0 … 9.0 gacha).
            Javobni faqat quyidagi JSON formatda, o‘zbek tilida qaytaring. Hech qanday qo‘shimcha matn, izoh yoki belgilar yozmang!

            {{
            "overall": BAND,
            "task_achievement": BAND,
            "coherence_and_cohesion": BAND,
            "lexical_resource": BAND,
            "grammatical_range_and_accuracy": BAND,
            "feedback": "2-3 ta jumladan iborat qisqa maslahat."
            }}
            """

        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,           
                    "max_output_tokens": 800,
                    "top_p": 0.8,
                    "top_k": 40
                }
            )
            text = response.text.strip()
            json_match = re.search(r"\{.*\}", text, re.DOTALL)
            result = json.loads(json_match.group())

            scores = [result["task_achievement"], result["coherence_and_cohesion"],
                      result["lexical_resource"], result["grammatical_range_and_accuracy"]]
            result["overall"] = round(sum(scores)/4 * 2) / 2

            return Response(result)

        except Exception as e:
            return Response({"error": str(e)}, status=500)



       

    


