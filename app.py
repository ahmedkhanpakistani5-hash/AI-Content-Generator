import os
import streamlit as st
from groq import Groq

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Content Generator",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Content Generator")
st.write("Generate AI content using Groq API")

# -----------------------------
# Load API Key
# -----------------------------
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ Groq API Key not found.")
    st.stop()

client = Groq(api_key=api_key)

# -----------------------------
# Sidebar
# -----------------------------
content_type = st.sidebar.selectbox(
    "Choose Content Type",
    [
        "Blog",
        "Email",
        "Instagram Caption",
        "LinkedIn Post",
        "Product Description"
    ]
)

# -----------------------------
# User Input
# -----------------------------
topic = st.text_input("Enter your topic")

# -----------------------------
# Generate Button
# -----------------------------
if st.button("Generate Content"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")
    else:

        prompt = f"""
Write a professional {content_type} about:

{topic}

Make it engaging, clear, and well-structured.
"""

        try:
            with st.spinner("Generating..."):

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                result = response.choices[0].message.content

            st.success("Content Generated Successfully!")

            st.subheader("Generated Content")

            st.write(result)

            st.download_button(
                "📥 Download",
                data=result,
                file_name="generated_content.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error: {e}")
