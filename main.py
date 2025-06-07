# === File: gemini_server.py ===
from fastapi import FastAPI, Request
import google.generativeai as genai
import uvicorn

app = FastAPI()
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"  # Replace with your actual Gemini API key
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

@app.post("/answer")
async def get_best_answer(request: Request):
    data = await request.json()
    question = data.get("question")
    choices = data.get("choices")

    prompt = f"""You are answering a Kahoot quiz.

Question: {question}
Choices:
A. {choices[0]}
B. {choices[1]}
C. {choices[2]}
D. {choices[3]}

Respond with just the correct letter (A, B, C, or D)."""

    response = model.generate_content(prompt)
    return {"answer": response.text.strip().upper()}

# Run with: uvicorn gemini_server:app --reload --port 8000


# === File: kahoot_bot.py ===
import asyncio
from kahoot import client
import requests

GEMINI_SERVER_URL = "http://localhost:8000/answer"
GAME_PIN = input("Game PIN: ")
NICKNAME = input("Bot Nickname: ")

bot = client()

@bot.on("ready")
async def on_ready():
    print("✅ Joined game as", NICKNAME)

@bot.on("question")
async def on_question(question):
    q_text = question.question
    choices = [c or "" for c in question.choices]

    print("\n❓ Question:", q_text)
    for i, choice in enumerate(choices):
        print(f"{chr(65+i)}. {choice}")

    try:
        r = requests.post(GEMINI_SERVER_URL, json={"question": q_text, "choices": choices})
        answer_letter = r.json()["answer"]
        index = "ABCD".index(answer_letter)
        print(f"🤖 Gemini recommends: {answer_letter}")
        await question.answer(index)
    except Exception as e:
        print("❌ Error from Gemini server:", e)
        await question.answer(0)  # default safe answer

@bot.on("finish")
def on_finish(data):
    print("🏁 Game finished.")

bot.join(GAME_PIN, NICKNAME)
