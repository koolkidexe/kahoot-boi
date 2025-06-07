import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Kahoot Gemini Bot", layout="centered")
st.title("🤖 Kahoot Auto Answer Bot with Gemini")

# Inputs
api_key = st.text_input("🔑 Enter your Gemini API Key", type="password")
question = st.text_area("❓ Kahoot Question")
answers_input = st.text_area("🔢 Answer Choices (one per line, max 4)")

submit = st.button("🔍 Get Best Answer")

# Process
if submit:
    if not api_key or not question or not answers_input:
        st.error("Please fill in all fields.")
    else:
        # Setup Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
        answers = answers_input.strip().split("\n")

        if len(answers) > 4:
            st.error("Please enter only up to 4 choices.")
        else:
            prompt = f"""You are helping answer a multiple choice Kahoot quiz.
Question: {question}
Options:
{chr(65)}. {answers[0] if len(answers) > 0 else ''}
{chr(66)}. {answers[1] if len(answers) > 1 else ''}
{chr(67)}. {answers[2] if len(answers) > 2 else ''}
{chr(68)}. {answers[3] if len(answers) > 3 else ''}

Only return the letter of the most likely correct answer (A, B, C, or D) — nothing else.
"""

            with st.spinner("Thinking with Gemini..."):
                try:
                    response = model.generate_content(prompt)
                    ai_answer = response.text.strip().upper()
                    if ai_answer in ["A", "B", "C", "D"]:
                        st.success(f"✅ Gemini recommends: **{ai_answer}**")
                    else:
                        st.warning("❌ Gemini's response wasn't a valid option:\n\n" + response.text)
                except Exception as e:
                    st.error(f"Gemini error: {e}")
