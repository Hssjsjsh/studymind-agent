import streamlit as st
import os
from agent.agent import chat
from agent.tools.pdf_tool import load_pdf

st.set_page_config(
    page_title="StudyMind Agent",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 StudyMind Agent")
st.caption("Your AI research and study assistant")

with st.sidebar:
    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader(
        "Upload a PDF to chat with",
        type=["pdf"]
    )
    if uploaded_file:
        save_path = f"docs/{uploaded_file.name}"
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        with st.spinner("Indexing your document..."):
            result = load_pdf(save_path)
        st.success(f"✅ {uploaded_file.name} indexed!")

    st.divider()
    st.header("⚙️ Tools Available")
    st.markdown("🔍 Web Search")
    st.markdown("📄 PDF Chat")
    st.markdown("📧 Send Email")
    st.markdown("📅 Calendar")

    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi! I'm StudyMind 🧠 I can search the web, read your PDFs, send emails, and schedule study sessions. What do you need help with?"
    })

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat(prompt)
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })