from langchain_openai import OpenAI
import json
import re


def generate_quiz(text):
    llm = OpenAI(temperature=0)

    # ---------- TRY 1: STRICT JSON ----------
    json_prompt = f"""
    Generate 5 multiple choice questions from the content below.

    RULES:
    - Return ONLY valid JSON
    - No explanations
    - No markdown
    - No extra text

    Format:
    [
      {{
        "question": "Question text",
        "options": {{
          "A": "Option A",
          "B": "Option B",
          "C": "Option C",
          "D": "Option D"
        }},
        "answer": "A"
      }}
    ]

    Content:
    {text}
    """

    response = llm.invoke(json_prompt)

    try:
        json_text = re.search(r"\[.*\]", response, re.S).group()
        quiz = json.loads(json_text)
        if quiz:
            return quiz
    except Exception:
        pass

    # ---------- TRY 2: FALLBACK (PLAIN TEXT MCQs) ----------
    fallback_prompt = f"""
    Create 5 multiple choice questions from the content below.

    Format EXACTLY like this:

    Q1. Question text
    A. option
    B. option
    C. option
    D. option
    Answer: A

    Content:
    {text}
    """

    response = llm.invoke(fallback_prompt)

    return parse_fallback_quiz(response)


def parse_fallback_quiz(text):
    quiz = []
    questions = re.split(r"\nQ\d+\.", text)

    for q in questions:
        if "Answer:" not in q:
            continue

        lines = q.strip().split("\n")
        question = lines[0].strip()

        options = {}
        answer = None

        for line in lines[1:]:
            if re.match(r"[A-D]\.", line):
                key = line[0]
                options[key] = line[2:].strip()
            elif "Answer:" in line:
                answer = line.split("Answer:")[-1].strip()

        if question and options and answer:
            quiz.append({
                "question": question,
                "options": options,
                "answer": answer
            })

    return quiz
