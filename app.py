import streamlit as st
import openai

# --- Page Config ---
st.set_page_config(page_title="AI Interview Question Analyzer", layout="centered")
st.title("🧠 AI Interview Question Analyzer")
st.caption("Built by Ritika Arora · Powered by OpenRouter")

# --- API Key Input ---
api_key = st.text_input("🔑 Enter your OpenRouter API Key", type="password")

# --- Question Input ---
question_input = st.text_area("✍️ Paste one or more interview questions (one per line)", height=250)

# --- Model Selector ---
model = st.selectbox("🤖 Choose a Model", [
    "anthropic/claude-3-opus",
    "openai/gpt-4",
    "mistralai/mistral-7b-instruct",
    "meta-llama/llama-3-70b-instruct"
])

# --- Analyze Button ---
if st.button("🔍 Analyze"):
    if not api_key:
        st.error("Please enter your OpenRouter API key.")
    elif not question_input.strip():
        st.error("Please paste at least one question.")
    else:
        openai.api_key = api_key
        openai.api_base = "https://openrouter.ai/api/v1"

        # Process each question line-by-line
        questions = [q.strip() for q in question_input.strip().split("\n") if q.strip()]

        for q in questions:
            prompt = f"""
You are an expert technical interviewer.

Please analyze the following interview question and provide:

1. Difficulty level (Easy/Medium/Hard)
2. Skills tested
3. Time estimate to solve
4. Any issues (ambiguity, bias, outdated tech, unclear expectations)
5. Suggestions to improve the question
6. A sample answer (if applicable)

Question: {q}
"""

            try:
                with st.spinner(f"Analyzing: {q}"):
                    response = openai.ChatCompletion.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=500,
                    )
                    result = response['choices'][0]['message']['content']
                    st.markdown(f"---\n### 🔹 Question: {q}")
                    st.markdown(result)
            except Exception as e:
                st.error(f"Error analyzing question: {q}\n\n{e}")
