import requests, json, os
from decouple import config


GROK_API_KEY = config("GROK_API_KEY")
GROK_API_URL = config("GROK_API_URL")

def evaluate_with_grok(submission):
    task = submission.task
    essay = submission.answer

    prompt = f"""You are an official IELTS examiner (Band 9 expert).
                Evaluate this IELTS Writing {task.task_type.upper()} essay.

                Question:
                {task.question}

                Student's essay:
                {essay}

                Return ONLY valid JSON:
                {{
                "score": 7.5,
                "coherence": 8.0,
                "grammar": 7.5,
                "vocabulary": 7.0,
                "response": 7.5,
                "feedback": "• Excellent paragraphing\\n• Use more academic words\\n• Add Uzbekistan example\\n• Conclusion stronger"
                }}
                """

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "grok-3",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 600
    }

    try:
        r = requests.post(GROK_API_URL, headers=headers, json=payload, timeout=20)
        r.raise_for_status()
        content = r.json()['choices'][0]['message']['content']
        
        json_start = content.find("{")
        json_end = content.rfind("}") + 1
        result = json.loads(content[json_start:json_end])
        
        for key in ['score','coherence','grammar','vocabulary','response']:
            result[key] = round(float(result[key]), 1)
            
        return result
    except Exception as e:
        print("Grok error:", e)
        return {
            "score": 5.5, "coherence": 5.5, "grammar": 5.5,
            "vocabulary": 5.5, "response": 5.5,
            "feedback": "Grok temporarily unavailable. Trying again..."
        }