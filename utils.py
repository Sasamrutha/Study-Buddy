import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a study assistant for Indian students.

When given a topic or study note, respond in EXACTLY this format
with these EXACT section headers. No extra text before or after.

## SIMPLE EXPLANATION
Explain the topic in plain English as if talking to a classmate.
Use a real-world analogy wherever possible.
Keep it to 4-6 sentences.

## 5-POINT SUMMARY
1. [key point]
2. [key point]
3. [key point]
4. [key point]
5. [key point]

## PRACTICE QUESTIONS
Q1 (Easy): [question]
Q2 (Medium): [question]
Q3 (Hard): [question]

## DIFFICULTY RATING
Rating: [Beginner / Intermediate / Advanced]
Why: [one sentence explaining why you gave this rating]
"""

def get_explanation(topic: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": f"Topic: {topic}"}
            ],
            temperature=0.3,
            max_tokens=1000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"