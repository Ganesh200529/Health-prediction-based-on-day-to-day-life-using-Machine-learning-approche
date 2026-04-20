import streamlit as st
import google.generativeai as genai
def chatbot_page():
    st.markdown("<h1 style='text-align: center; color: #574e37;'>👨‍⚕️ Chat with Bot</h1>", unsafe_allow_html=True)
    st.write("I'm your virtual Doctor Bot. Do you need suggestions for your food diet or any health tips?")
    
    api_key = "AIzaSyAwGeUPMwLQNOa02OKCyALfLlQ1wyIw8FI" # Hardcoded Gemini Key
    
    if "doc_bot_chat" not in st.session_state:
        st.session_state.doc_bot_chat = [{"role": "assistant", "content": "Hello! I'm your virtual Doctor Bot. How can I help you today?"}]
        
    for msg in st.session_state.doc_bot_chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    with st.form("chat_form", clear_on_submit=True):
        c1, c2 = st.columns([4, 1])
        user_input = c1.text_input("Ask...", label_visibility="collapsed", placeholder="Ask about health or diet...")
        submit = c2.form_submit_button("Send")
        
    if submit and user_input:
        st.session_state.doc_bot_chat.append({"role": "user", "content": user_input})
        st.rerun() 
        
    if st.session_state.doc_bot_chat and st.session_state.doc_bot_chat[-1]["role"] == "user":
        with st.chat_message("assistant"):
            user_msg = st.session_state.doc_bot_chat[-1]["content"]
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = f"You are a helpful doctor and dietician bot. Suggest diet and clarify medical doubts safely. The user states: {user_msg}"
                    response = model.generate_content(prompt)
                    reply = response.text
                except Exception as e:
                    reply = f"API Error: {e}"
            else:
                reply = "⚠️ Developer notice: Please add your Gemini API Key in the code to activate AI responses!"
            
            st.write(reply)
            st.session_state.doc_bot_chat.append({"role": "assistant", "content": reply})
