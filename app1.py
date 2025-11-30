import streamlit as st
import streamlit.components.v1 as components
from generate_knowledge_graph1 import generate_knowledge_graph

# Page config
st.set_page_config(
    page_title="Knowledge Graph Generator",
    layout="wide",
    initial_sidebar_state="auto"
)

# Custom CSS
st.markdown("""
    <style>
    /* Page background gradient */
    body {
        background: linear-gradient(to right, #ffafbd, #ffc3a0, #2193b0, #6dd5ed);
    }
    .stApp {
        background: transparent;
    }

    /* Center container */
    .center-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        border-radius: 20px;
        background-color: rgba(0,0,0,0.5);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }

    h1 {
        color: #ffffff;
        text-shadow: 2px 2px 4px #000000;
    }

    .upload-btn {
        background: linear-gradient(90deg, #f6d365 0%, #fda085 100%);
        color: #fff !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        margin-top: 10px;
        border: none;
        cursor: pointer;
        transition: 0.3s ease;
    }

    .upload-btn:hover {
        background: linear-gradient(90deg, #fda085 0%, #f6d365 100%);
        transform: scale(1.05);
    }

    .text-area {
        border-radius: 10px;
        padding: 10px;
        width: 80%;
        margin: 10px auto;
    }
    </style>
""", unsafe_allow_html=True)

# Centered container
st.markdown('<div class="center-container">', unsafe_allow_html=True)
st.markdown("## 📘 Knowledge Graph Generator (FREE Groq API – LLaMA-3)")
st.markdown("Generate an interactive knowledge graph from text. Upload a `.txt` file or paste text below.")

# Input method radio
input_method = st.radio("Choose input method:", ["Upload txt File", "Paste Text"], horizontal=True)

text = ""
if input_method == "Upload txt File":
    uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
    if uploaded_file:
        text = uploaded_file.read().decode("utf-8")

else:
    text = st.text_area("Paste your text here", height=200)

# Generate button
if st.button("Generate Knowledge Graph", key="generate", help="Click to generate the knowledge graph"):
    if not text:
        st.warning("Please provide text or upload a file!")
    else:
        with st.spinner("Generating knowledge graph..."):
            net = generate_knowledge_graph(text)
            st.success("Knowledge graph generated successfully!")
            output_file = "knowledge_graph.html"
            net.save_graph(output_file)
            HtmlFile = open(output_file, 'r', encoding='utf-8')
            components.html(HtmlFile.read(), height=1000)

st.markdown('</div>', unsafe_allow_html=True)
