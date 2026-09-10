import os
import streamlit as st
from groq import Groq

# Page Settings
st.set_page_config(page_title="AI Content Generator", page_icon="🤖")

st.title("🤖 AI Content Generator")
st.write("Generate AI content using Groq API")

# Get API Key
api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

if not api_key:
    st.error("Groq API Key not found!")
    st.stop()

client = Groq(api_key=api_key)

# Sidebar
content_type = st.sidebar.selectbox(
    "Select Content Type",
    [
        "Blog",
        "Email",
        "Instagram Caption",
        "LinkedIn Post",
        "Product Description"
    ]
)

topic = st.text_input("Enter your topic")

if st.button("Generate Content"):

    if topic == "":
        st.warning("Please enter a topic.")
    else:

        prompt = f"""
        Write a professional {content_type} about:
        {topic}
        """

        with st.spinner("Generating..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

        result = response.choices[0].message.content

        st.subheader("Generated Content")
        st.write(result)

        st.download_button(
            "Download",
            result,
            file_name="content.txt"
        )
