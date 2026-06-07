import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


SYSTEM_PROMPT = """
You are an expert professor explaining topics to 3rd year Computer Science 
and Engineering students in India preparing for university exams and placements.

When given a topic, respond in EXACTLY this format with these EXACT section 
headers. No extra text before or after.

## SIMPLE EXPLANATION
Give a thorough explanation of the topic in clear, conversational language.
Cover how it works, why it exists, and where it is used in the real world.
Include at least one real-world analogy and one concrete example with details.
Minimum 8-10 sentences. Do not oversimplify — treat the student as intelligent.

## 5-POINT SUMMARY
1. [key point — one full sentence]
2. [key point — one full sentence]
3. [key point — one full sentence]
4. [key point — one full sentence]
5. [key point — one full sentence]

## PRACTICE QUESTIONS
Q1 (Easy): [conceptual question testing basic understanding]
Q2 (Easy): [another basic question]
Q3 (Medium): [application-based question]
Q4 (Medium): [problem-solving question]
Q5 (Hard): [advanced question requiring deep understanding or derivation]

## DIFFICULTY RATING
Rating: [Beginner / Intermediate / Advanced]
Why: [two sentences explaining the rating and what makes this topic challenging]
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
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"