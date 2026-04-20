import streamlit as st
from home_page import home_page
from login_page import login_page
from signup_page import signup_page
from user_home_page import user_home_page
from chatbot_page import chatbot_page

st.set_page_config(page_title="Healthcare Application", page_icon="🩺", layout="wide")
# Initialize session state / check query parameters for standalone tabs
if "page" in st.query_params:
    st.session_state["current_page"] = st.query_params.get("page")
elif "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

# Page rendering logic
if st.session_state["current_page"] == "home":
    home_page()
elif st.session_state["current_page"] == "login":
    login_page()
elif st.session_state["current_page"] == "signup":
    signup_page()
elif st.session_state["current_page"] == "user_home" and st.session_state["logged_in"]:
    user_home_page()
elif st.session_state["current_page"] == "chatbot":
    chatbot_page()
else:
    st.error("Something went wrong. Please reload the app.")
