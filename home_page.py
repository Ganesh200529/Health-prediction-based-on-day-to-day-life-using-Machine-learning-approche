import streamlit as st

# Navigation function
def navigate_to_page(page_name):
    st.session_state["current_page"] = page_name
    st.experimental_rerun()
def home_page():
    #add info about the eye disease detection system in the sidebar
    st.markdown(
    """
    <style>
    /* Apply background image to the main content area */
    .main {
        background-image: url("https://nodens.eu/wp-content/uploads/2019/10/AdobeStock_281967200.jpeg");  
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    col1,col2,col3 = st.columns([1,8,1])
    col2.markdown(
        """
        <div style="text-align: center; padding: 1px; background-color: red ; border-radius: 90px; border: 2px solid black;">
            <p style="color: white; font-size: 40px;"><b>Health Prediction based on Life Activity</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )
    #add image
    st.write("")
    st.write("")
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.gifer.com/7BZb.gif" alt="Health" width="500" height=400">
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5,col6 = st.columns([1.5, 1, 1, 1, 1,1])
    with col2:
        if st.button("Login",type="primary"):
            navigate_to_page("login")
    with col5:
        if st.button("Sign Up",type="primary"):
            navigate_to_page("signup")
