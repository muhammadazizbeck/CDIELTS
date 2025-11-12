# backend/writing/ai_openai.py
import requests
import json
from django.conf import settings

def evaluate_with_openai(submission):
    task = submission.task
    essay = submission.answer

    prompt = f"""
You are an official IELTS Writing examiner (Band 9 expert).
Evaluate this IELTS Writing {task.task_type.upper()} essay.

Question:
{task.question}

Student's essay:
{essay}

Return ONLY valid JSON:
{{
  "score": 8.0,
  "coherence": 8.5,
  "grammar": 8.0,
  "vocabulary": 7.5,
  "response": 8.0,
  "feedback": "• Excellent structure and examples\\n• Strong vocabulary range\\n• Clear position throughout"
}}
"""

    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",  
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 700
    }

    try:
        response = requests.post(settings.OPENAI_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        content = data['choices'][0]['message']['content'].strip()

        # JSON parse
        result = json.loads(content)

        # Ballarni float va round qilish
        for key in ['score', 'coherence', 'grammar', 'vocabulary', 'response']:
            if key in result:
                try:
                    result[key] = round(float(result[key]), 1)
                except:
                    result[key] = 6.0

        return result

    except Exception as e:
        print(f"OpenAI xato: {e}")
        return {
            "score": 6.0,
            "coherence": 6.0,
            "grammar": 6.0,
            "vocabulary": 6.0,
            "response": 6.0,
            "feedback": "OpenAI API ishlamadi, keyinroq qayta urinib ko‘ring."
        }

