#streamlit 聊天渲染
import streamlit as st
def render_chat(messages:list[dict],summary:str):
    for item in messages:
        with st.chat_message(item["role"]):
            st.write(item["content"])

