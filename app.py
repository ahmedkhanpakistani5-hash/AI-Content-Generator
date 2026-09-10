import os
import streamlit as st
from groq import Groq

# Page settings
st.set_page_config(
    page_title="AI Content Generator",
    page_icon="🤖",
    layout="centered"
)
# Custom dark AI-style design
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e1b4b, #111827);
        color: white;
    }

    /* Main text */
    h1, h2, h3, h4, p, label {
        color: white !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827, #1e1b4b);
    }

    /* Text area and inputs */
    textarea, input {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #475569 !important;
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #475569 !important;
    }

    /* Generate button */
    .stButton > button {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
        padding: 10px;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #8b5cf6, #6366f1);
        color: white;
    }

    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #06b6d4, #3b82f6);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
    }

    /* Divider */
    hr {
        border-color: #475569;
    }

    /* Footer */
    .stCaption {
        color: #94a3b8 !important;
    }
</style>
""", unsafe_allow_html=True)
# Title
st.title("🤖 AI Content Generator")
st.write("Create high-quality content using AI")

# API key
api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

if not api_key:
    st.error("Groq API key not found!")
    st.stop()

client = Groq(api_key=api_key)

# Sidebar
st.sidebar.header("⚙️ Content Settings")

content_type = st.sidebar.selectbox(
    "📝 Content Type",
    [
        "Blog",
        "Email",
        "LinkedIn Post",
        "Instagram Caption",
        "Facebook Post",
        "Product Description",
        "YouTube Script",
        "Story",
        "Tweet / X Post"
    ]
)

tone = st.sidebar.selectbox(
    "🎯 Tone",
    [
        "Professional",
        "Friendly",
        "Creative",
        "Persuasive",
        "Funny",
        "Simple"
    ]
)

length = st.sidebar.selectbox(
    "📏 Length",
    [
        "Short",
        "Medium",
        "Long"
    ]
)

# Main input
st.subheader("📝 Enter Your Topic")

topic = st.text_area(
    "What do you want to write about?",
    placeholder="Example: Artificial Intelligence in education",
    height=120
)

# Generate button
if st.button("🚀 Generate Content", use_container_width=True):

    if not topic.strip():
        st.warning("Please enter a topic first.")

    else:

        prompt = f"""
You are a professional content writer.

Create a {content_type} about:
{topic}

Requirements:
- Tone: {tone}
- Length: {length}
- Make it clear and engaging.
- Use proper grammar.
- Make the content useful and original.
"""

        try:
            with st.spinner("🤖 AI is generating your content..."):

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

            st.success("✅ Content Generated Successfully!")

            st.subheader("📄 Generated Content")

            # Text area makes it easy to select and copy
            st.text_area(
                "Copy your content:",
                result,
                height=400
            )

            # Download button
            st.download_button(
                label="📥 Download Content",
                data=result,
                file_name="generated_content.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# Footer
st.markdown("---")
st.caption("🤖 AI Content Generator | Powered by Groq | Built with Streamlit")
