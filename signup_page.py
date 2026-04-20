import streamlit as st
from database import add_user
import re
def navigate_to_page(page_name):
    st.session_state["current_page"] = page_name
    st.rerun()  # Using st.rerun() to fix a common VS Code warning instead of experimental_rerun
def validate_mail(mail):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', mail) is not None

def check_password_strength(password):
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("at least 8 characters")
        
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("a lowercase letter")
        
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("an uppercase letter")
        
    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("a number")
        
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("a special character")
        
    if score < 3:
        return "Weak", feedback
    elif score < 5:
        return "Medium", feedback
    else:
        return "Strong", []
def signup_page():
    st.markdown(
    """
    <style>
    /* Apply background image to the main content area */
    .main {
        background-image: url("https://blindspot.ai/assets/img/intro-background.svg?3");  
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    col1,col2,col3 = st.columns([1,5,1])
    with col2.form(key="signup_form"):
        col1,col2 = st.columns([10,1])
        col1.title("Sign Up Here!!!")
        if col2.form_submit_button('🏚️'):
            navigate_to_page("home")
        col1,col2=st.columns([1,1])
        name=col1.text_input("Enter Name")
        email = col2.text_input("Email", key="signup_email")
        col1,col2=st.columns([1,1])
        age=col1.slider("Age", 0, 100, 0, 1)
        gender=col2.selectbox("Gender", ["Male👦🏻","Female👩🏻","Others"])
        col1,col2=st.columns([1,1])
        disease_choice=col1.selectbox("Do you have any disease?",["Lung Disease","Heart Disease","Diabetes","Eye Disease","Kidney Disease","Brain Disease","Muscle Disease","Skin Disease","Migraine","Blood Cancer","Breast Cancer","Others","None"])
        disease_custom=col1.text_input("Specify disease (If 'Others' selected)")
        blood_group=col2.selectbox("Blood Group",["A+","A-","B+","B-","AB+","AB-","O+","O-"])
        occupation_choice=col2.selectbox("Occupation",["Student👨🏻‍🎓","Doctor👨🏻‍⚕️","Engineer👨🏻‍🔧","Teacher👩🏻‍🏫","Businessman👨🏻‍💼","Others"])
        occupation_custom=col2.text_input("Specify occupation (If 'Others' selected)")
        
        disease = disease_custom if disease_choice == "Others" else disease_choice
        occupation = occupation_custom if occupation_choice == "Others" else occupation_choice

        col1,col2=st.columns([1,1])
        height = col1.number_input("Height (cm) - for BMI", min_value=0.0, format="%.1f")
        weight = col2.number_input("Weight (kg) - for BMI", min_value=0.0, format="%.1f")

        col1,col2=st.columns([1,1])
        password = col1.text_input("Create a Password", type="password", key="signup_password")
        retyped_password = col2.text_input("Retype Password", type="password", key="signup_retyped_password")
        col1,col2,col3 = st.columns([1,4,1])
        with col1:
            signup_submit = st.form_submit_button("Sign Up🔏", type='primary')
        with col3:
            signin_submit = st.form_submit_button("Sign In🙋🏽‍♂️", type='primary')
            
        if signin_submit:
            navigate_to_page("login")
            
        if signup_submit:
            strength, feedback = check_password_strength(password)
            
            if not name or not email or not age or not disease or not occupation:
                st.error("Please fill in all details.")
            elif not validate_mail(email):
                st.error("Invalid email address. Please enter a valid email address.")
            elif password != retyped_password:
                st.error("Passwords do not match.")
            elif strength != "Strong":
                if strength == "Weak":
                    st.error(f"Password Strength: **{strength}**. Please enter a Strong password.")
                elif strength == "Medium":
                    st.warning(f"Password Strength: **{strength}**. Please enter a Strong password.")
                st.info(f"To make your password strong, please include: {', '.join(feedback)}.")
            else:
                try:
                    if height > 0 and weight > 0:
                        height_in_m = height / 100.0
                        bmi_val = round(weight / (height_in_m * height_in_m), 2)
                        
                        if bmi_val < 18.5:
                            bmi_cat = "Underweight"
                        elif bmi_val < 25.0:
                            bmi_cat = "Normal weight"
                        elif bmi_val < 30.0:
                            bmi_cat = "Overweight"
                        else:
                            bmi_cat = "Obesity"
                    else:
                        bmi_val = 0.0
                        bmi_cat = "Unknown"
                        
                    add_user(name, email, age, gender, disease, occupation, password, blood_group, height, weight, bmi_val, bmi_cat)
                    st.success("Account created successfully!!")
                    navigate_to_page("login")
                except Exception as e:
                    st.error(e)