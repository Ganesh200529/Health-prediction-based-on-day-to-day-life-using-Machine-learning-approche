import streamlit as st
from streamlit_option_menu import option_menu
from database import fetch_user
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import google.generativeai as genai
model=joblib.load('kmeans_model.pkl')
import requests
YOUTUBE_API_KEY = "AIzaSyDYEeSTrT7pPpVzpmaJ491gxogVxfWwpvM"

def fetch_youtube_videos(query, max_results=10):
    url = f"https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'key': YOUTUBE_API_KEY,
        'maxResults': max_results
    }
    response = requests.get(url, params=params)
    videos = []
    if response.status_code == 200:
        data = response.json()
        for item in data['items']:
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            videos.append({'video_id': video_id, 'title': video_title})
    return videos

from database import add_daily,fetch_all_daily
def navigate_to_page(page_name):
    st.session_state["current_page"] = page_name
    st.experimental_rerun()
def plot_combined_charts(df):
    fig, axes = plt.subplots(3, 3, figsize=(18, 12))
    
    # Sleep Duration Distribution
    axes[0, 0].hist(df['sleep_duration'], bins=10, edgecolor='black')
    axes[0, 0].set_title('Sleep Duration Distribution', color='red')
    
    # Weight Distribution
    axes[0, 1].hist(df['weight'], bins=10, edgecolor='black', color='orange')
    axes[0, 1].set_title('Weight Distribution', color='green')
    
    # Physical Activity Level Distribution
    axes[0, 2].hist(df['physical_activity_level'], bins=10, edgecolor='black', color='green')
    axes[0, 2].set_title('Physical Activity Level Distribution', color='blue')
    
    # Stress Level Distribution
    axes[1, 0].hist(df['stress_level'], bins=10, edgecolor='black', color='red')
    axes[1, 0].set_title('Stress Level Distribution', color='magenta')
    
    # Heart Rate Distribution
    axes[1, 1].hist(df['heart_rate'], bins=10, edgecolor='black', color='cyan')
    axes[1, 1].set_title('Heart Rate Distribution', color='yellow')
    
    # Daily Steps Distribution
    axes[1, 2].hist(df['daily_steps'], bins=10, edgecolor='black', color='magenta')
    axes[1, 2].set_title('Daily Steps Distribution', color='orange')
    
    # Drinking Water Intake Distribution
    axes[2, 0].hist(df['drinking_water'], bins=10, edgecolor='black')
    axes[2, 0].set_title('Drinking Water Intake Distribution', color='red')
    
    # Weight vs Heart Rate Scatter Plot
    sns.scatterplot(x=df["weight"], y=df['heart_rate'], hue=df['BMI_category'], ax=axes[2, 1], palette='viridis')
    axes[2, 1].set_title('Weight vs Heart Rate', color='yellow')
    
    # Daily Steps vs Calories Burned Line Chart
    axes[2, 2].plot(df['daily_steps'], df['calories_burned'], marker='o', color='maroon')
    axes[2, 2].set_title('Daily Steps vs Calories Burned', color='maroon')
    
    plt.tight_layout()
    return fig
def user_home_page():
    user = fetch_user(st.session_state["current_user"])
    with st.sidebar:
        st.markdown(f"<h1 style='text-align: center;'>𝐖𝐄𝐋𝐂𝐎𝐌𝐄 👋 {user[1]}</h1>", unsafe_allow_html=True)
        st.image('https://media3.giphy.com/media/kU4mcmHfmV7YhuIj6J/giphy.gif?cid=6c09b952z44hzi7l9vygfdk0n27sf6zkug3gs4ayrdagf4qt&ep=v1_stickers_search&rid=giphy.gif&ct=s', use_column_width=True)
        select = option_menu(
            "",
            ["Patient Profile",'Daily Updates', 'Analytics',"Statistics","Health Care","Logout"],
            icons=['person-square','calendar','bar-chart','file-bar-graph-fill','youtube','person-fill-lock'], 
            menu_icon="cast",
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"padding": "0", "background-color": "#f7e8bc"}, 
                "icon": {"color": "black", "font-size": "20px"},    
                "nav-link": {
                    "font-size": "16px",
                    "margin": "0px",
                    "color": "black",                                          
                },   
                "nav-link-selected": {
                    "background-color": "#dbbd12",                            
                },
            },
        )
        
    def render_doctor_bot():
        st.markdown(
            """
            <style>
            .floating-bot-container {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 320px;
                z-index: 9999;
                background-color: #dea509;
                padding: 1px;
                border-radius: 15px;
            }
            .floating-bot-btn {
                background-color: #f7e8bc;
                border: 3px solid #d65804;
                border-radius: 15px;
                box-shadow: 2px 2px 15px rgba(0,0,0,0.3);
                padding: 10px;
                display: block;
                text-align: center;
                text-decoration: none !important;
                color: black !important;
                font-weight: bold;
                font-family: sans-serif;
                transition: background-color 0.3s;
            }
            .floating-bot-btn:hover {
                background-color: #f0dba1;
            }
            </style>
            <div class="floating-bot-container">
                <a href="/?page=chatbot" target="_blank" class="floating-bot-btn">
                    👨‍⚕️ Chat with Doctor Bot
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

    render_doctor_bot()

    if select == 'Health Care':
        st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://images.rawpixel.com/image_800/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvcm0zNzNiYXRjaDE1LXJtMjA4LTA0LmpwZw.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        </style>
        """,
        unsafe_allow_html=True
        )
        st.markdown("<h1 style='text-align: center; color: #d65804;'>Health Care Tips</h1>", unsafe_allow_html=True)
        col1,col2,col3=st.columns(3)
        problem=col2.selectbox("Select the problem",['','Diabetes','Heart Disease','Cancer','Obesity','Asthma','Arthritis','Stroke','Osteoporosis','Alzheimer','Depression',
        'Hypertension','Kidney Disease','Liver Disease','Lung Disease','Thyroid Disease','Mental Health','Skin Care','Hair Care','Eye Care','Dental Care',
        'Ear Care','Foot Care','Hand Care','Nail Care','Pregnancy Care','Child Care'])
        query = f"{problem} health tips"
        videos = fetch_youtube_videos(query)
        if problem:
            # Display videos in rows of 3
            for i in range(0, len(videos), 2):
                cols = st.columns(2)  # Create 3 columns
                for j, video in enumerate(videos[i:i+2]):  # Iterate over videos for the current row
                    with cols[j]:
                        st.video(f"https://www.youtube.com/watch?v={video['video_id']}")
    elif select == 'Patient Profile':
        st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://media.istockphoto.com/id/1395883623/video/abstract-polygonal-space-with-dots-and-lines-motion-data-technology-and-scientific.jpg?s=640x640&k=20&c=dxZnHo8jREUg9tmBRh-swYazxBExUB3FXdhuPiAoCcM=');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        </style>
        """,
        unsafe_allow_html=True
        )

        # Extracting user data from session state after successful login
        if user:
            name, age, gender,disease,occupation = user[1], user[3], user[4],user[5],user[6]
            blood_group = user[8] if len(user) > 8 and user[8] else "N/A"
            height = user[9] if len(user) > 9 and user[9] else "N/A"
            weight = user[10] if len(user) > 10 and user[10] else "N/A"
            bmi = user[11] if len(user) > 11 and user[11] else "N/A"
            bmi_category = user[12] if len(user) > 12 and user[12] else "N/A"
            if gender == 'Male👦🏻':
                image_link = "https://img.freepik.com/photos-premium/elevez-votre-marque-avatar-amical-qui-reflete-professionnalisme-ideal-pour-directeurs-ventes_1283595-18531.jpg?semt=ais_hybrid"
            else:
                image_link = "https://cdn-icons-png.flaticon.com/512/219/219969.png"

            # CSS Styling for vertical container
            profile_css = """
            <style>
                .profile-container {
                    background-image:url(https://img.freepik.com/free-vector/clean-medical-background-with-frame-vector_53876-166665.jpg);
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    padding: 50px;
                    border-radius: 50px;
                    box-shadow: 10px 8px 12px rgba(0, 0, 0, 0.15);
                    max-width: 400px;
                    border: 2px solid black;
                    margin-left: 100%;
                    margin: auto;
                    font-family: Arial, sans-serif;
                    text-align: center;
                }
                .profile-header {
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 1px;
                    color: #333;
                }
                .profile-item {
                    font-size: 18px;
                    margin-bottom: 10px;
                    color: #555;
                }
                .profile-image img {
                    border-radius: 50%;
                    max-width: 250px;
                    max-height: 250px;
                    margin-bottom: 0px;
                }
            </style>
            """

            # HTML Structure for vertical alignment
            profile_html = f"""
            <div class="profile-container">
                <div class="profile-image">
                    <img src="{image_link}" alt="User Image">
                </div>
                <div class="profile-details">
                    <div class="profile-header">Patient Report</div>
                    <div class="profile-item"><strong>Name:</strong> {name}</div>
                    <div class="profile-item"><strong>Age:</strong> {age}</div>
                    <div class="profile-item"><strong>Gender:</strong> {gender}</div>
                    <div class="profile-item"><strong>Blood Group:</strong> {blood_group}</div>
                    <div class="profile-item"><strong>Height (cm):</strong> {height}</div>
                    <div class="profile-item"><strong>Weight (kg):</strong> {weight}</div>
                    <div class="profile-item"><strong>BMI Category:</strong> {bmi_category} ({bmi})</div>
                    <div class="profile-item"><strong>Disease:</strong> {disease}</div>
                    <div class="profile-item"><strong>Occupation:</strong> {occupation}</div>
                </div>
            </div>
            """

            # Display styled content
            st.markdown(profile_css + profile_html, unsafe_allow_html=True)
    elif select == 'Daily Updates':
        st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url("https://t4.ftcdn.net/jpg/04/24/30/93/360_F_424309320_UkOxg2z3sq7yXwGnWCO6xBXkRI4byhnI.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-color: rgba(255, 255, 255, 0.5);
            background-blend-mode: overlay;
        }
        </style>
        """,
        unsafe_allow_html=True
        )
        st.markdown("<h1 style='text-align: center; color:red;'>Update Your Daily Health Data</h1>", unsafe_allow_html=True)
        username = user[1]
        gender = user[3]
        age = user[4]
        #fetch last row of daily updates
        daily_data = fetch_all_daily(user[2])
        if daily_data:
            daily_data_df = pd.DataFrame(daily_data)
            wt, slp, qslp, pal, sl, bmi, bp, hr, ds, rr, bv, cb, bt, dw, dus = daily_data_df.tail(1).values[0][2:]
        else:
            wt, slp, qslp, pal, sl, bmi, bp, hr, ds, rr, bv, cb, bt, dw, dus = 0, 0, 0, 0, 0, 'Normal', 0, 0, 0, 0, 0, 0, 0, 0, 0
        with st.form('Daily Updates'):
            col1,col2=st.columns(2)
            weight = col1.number_input("**Weight(In Kg's)**", value=wt)
            sleep_duration = col2.number_input("**Sleep Duration(In Hours)**", value=slp)
            # Hidden from UI, preserving last known database values to prevent ML/DB breakage
            quality_of_sleep = qslp
            physical_activity_level = pal
            stress_level =  st.slider("**Stress Level**", min_value=0, max_value=10, value=sl)
            col1,col2=st.columns(2)
            # Extrapolate BMI Category from the profile calculation to pass downstream implicitly
            BMI_category = user[12] if len(user) > 12 and user[12] else "Normal weight"
            blood_pressure = col2.number_input("**Blood Pressure (mmHg)**", min_value=0, max_value=200, value=bp)
            heart_rate = col1.number_input("**Heart Rate (bpm)**", min_value=0, max_value=200, value=hr)
            daily_steps = col2.number_input("**Daily Steps**", min_value=0, value=ds)
            respiratory_rate = col1.number_input("**Respiratory Rate (breaths/min)**", min_value=0, value=rr)
            blood_volume = col2.number_input("**Blood Volume (L)**", min_value=0, value=bv)
            calories_burned = col1.number_input("**Calories Burned (Kcal)**", min_value=0, value=cb)
            body_temperature = col2.number_input("**Body Temperature (°C)**", min_value=0, value=bt)
            drinking_water = col1.number_input("**Drinking Water (In Liter's)**", min_value=0, value=dw)
            daily_usage_of_smart_phone = col2.number_input("**Daily Usage of Smart Phone(In Hour's)**", min_value=0, value=dus)
            col1,col2,col3=st.columns([2,1,2])
            if col2.form_submit_button("Submit",type='primary'):
                if username:
                    add_daily(user[0],user[2], weight, sleep_duration, quality_of_sleep, physical_activity_level, stress_level, BMI_category, blood_pressure, heart_rate, daily_steps, respiratory_rate, blood_volume, calories_burned, body_temperature, drinking_water, daily_usage_of_smart_phone)
                    st.success("Daily updates submitted successfully!")
                else:
                    st.error("Please fill in all fields before submitting.")
    elif select == 'Analytics':
        st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            
            color: #050505;
            background-image: url("https://t3.ftcdn.net/jpg/07/86/34/68/360_F_786346890_E4BqkCpTHWZg4LIcBnqG2MdyB1Afxz1z.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-color: rgba(255, 255, 255, 0.6);
            background-blend-mode: overlay;
        }
        </style>
        """,
        unsafe_allow_html=True
        )
        st.markdown("<h1 style='text-align: center;color:#d65804;'>Analytics of Patient</h1>", unsafe_allow_html=True)
        daily_data = fetch_all_daily(user[2])
        if daily_data:
            daily_data_df = pd.DataFrame(daily_data)
            columns = ['ID','mail', 'weight', 'sleep_duration', 'quality_of_sleep',
                        'physical_activity_level', 'stress_level', 'BMI_category', 'blood_pressure', 'heart_rate',
                        'daily_steps', 'respiratory_rate', 'blood_volume', 'calories_burned', 'body_temperature',
                        'drinking_water', 'daily_usage_of_smart_phone']
            #make a dataframe with column names
            daily_data_df.columns=columns
            df=daily_data_df.drop(['ID','mail'],axis=1)
            st.write(df)
            if st.checkbox('Show Analytics'):
                fig = plot_combined_charts(df)
                st.pyplot(fig)
                col1, col2 = st.columns(2)
                # Unique usage times and their counts
                unique_times = df['daily_usage_of_smart_phone'].unique()
                counts = df['daily_usage_of_smart_phone'].value_counts()
                colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'orange']

                # Sleep Duration Distribution
                fig, ax = plt.subplots()
                ax.hist(df['sleep_duration'], bins=10, edgecolor='black')
                ax.set_xlabel('Sleep Duration (hours)')
                ax.set_ylabel('Frequency')
                col1.markdown(f'<h3 style="color: red; text-align: center;">Sleep Duration Distribution</h3>', unsafe_allow_html=True)
                col1.pyplot(fig)
                
                # Weight Distribution
                fig, ax = plt.subplots()
                ax.hist(df['weight'], bins=10, edgecolor='black', color='orange')
                ax.set_xlabel('Weight')
                ax.set_ylabel('Frequency')
                col2.markdown(f'<h3 style="color: green; text-align: center;">Weight Distribution</h3>', unsafe_allow_html=True)
                col2.pyplot(fig)

                # Physical Activity Level Distribution
                fig, ax = plt.subplots()
                ax.hist(df['physical_activity_level'], bins=10, edgecolor='black', color='green')
                ax.set_xlabel('Physical Activity Level')
                ax.set_ylabel('Frequency')
                col1.markdown(f'<h3 style="color: blue; text-align: center;">Physical Activity Level Distribution</h3>', unsafe_allow_html=True)
                col1.pyplot(fig)

                fig, ax = plt.subplots()
                ax.hist(df['stress_level'], bins=10, edgecolor='black', color='red')
                ax.set_xlabel('Stress Level')
                ax.set_ylabel('Frequency')
                col2.markdown(f'<h3 style="color: magenta; text-align: center;">Stress Level Distribution</h3>', unsafe_allow_html=True)    
                col2.pyplot(fig)
                col1,col2=st.columns(2)
                fig, ax = plt.subplots()
                ax.hist(df['heart_rate'], bins=10, edgecolor='black', color='cyan')
                ax.set_xlabel('Heart Rate')
                ax.set_ylabel('Frequency')
                col1.markdown(f'<h3 style="color: yellow; text-align: center;">Heart Rate Distribution</h3>', unsafe_allow_html=True)
                col1.pyplot(fig)

                fig, ax = plt.subplots()
                ax.hist(df['daily_steps'], bins=10, edgecolor='black', color='magenta')
                ax.set_xlabel('Daily Steps')
                ax.set_ylabel('Frequency')
                col2.markdown(f'<h3 style="color: orange; text-align: center;">Daily Steps Distribution</h3>', unsafe_allow_html=True)
                col2.pyplot(fig)

                fig, ax = plt.subplots()
                ax.bar(unique_times, counts, color=colors)
                ax.set_xlabel('Usage Time (hours)')
                ax.set_ylabel('Frequency')
                ax.tick_params(axis='x', rotation=45)
                col1.markdown(f'<h3 style="color: green; text-align: center;">Smartphone Usage Time Distribution</h3>', unsafe_allow_html=True)
                col1.pyplot(fig)

                # Plotting Drinking Water (liters)
                fig, ax = plt.subplots()
                ax.hist(df['drinking_water'], bins=10, edgecolor='black')
                ax.set_xlabel('Drinking Water Intake (liters)')
                ax.set_ylabel('Frequency')
                col2.markdown(f'<h3 style="color: red; text-align: center;">Drinking Water Intake Distribution</h3>', unsafe_allow_html=True)
                col2.pyplot(fig)
                col1,col2=st.columns(2)
                bmi_plot = df['BMI_category'].value_counts().plot(kind='bar', color=['#FF9999', '#66B2FF'], figsize=(6, 4))
                col1.markdown(f'<h3 style="color: blue; text-align: center;">BMI Category Distribution</h3>', unsafe_allow_html=True)
                col1.pyplot(bmi_plot.figure)

                fig = plt.figure(figsize=(6, 4))
                sns.scatterplot(x=df['weight'], y=df['heart_rate'], hue=df['BMI_category'], palette='viridis')
                col2.markdown(f'<h3 style="color: yellow; text-align: center;">Weight vs Heart Rate</h3>', unsafe_allow_html=True)
                col2.pyplot(fig)
                col1, col2 = st.columns(2)

                line_chart = pd.DataFrame({
                    'Daily Steps': df['daily_steps'],
                    'Calories Burned': df['calories_burned']
                })
                col1.markdown(f'<h3 style="color: maroon; text-align: center;">Daily Steps vs Calories Burned</h3>', unsafe_allow_html=True)  
                col1.line_chart(line_chart)

                fig = plt.figure(figsize=(6, 4))
                col2.markdown(f'<h3 style="color: green; text-align: center;">Blood Pressure Distribution</h3>', unsafe_allow_html=True)
                sns.histplot(df['blood_pressure'], kde=True, color='purple')
                col2.pyplot(fig)
                categories = ['sleep_duration', 'quality_of_sleep', 'stress_level', 'blood_pressure', 'heart_rate']
                values = df[categories].iloc[0].values.tolist()
                col1, col2=st.columns(2)
                # Append the first value to the end of the list to close the radar chart
                values += values[:1]

                # Append an empty string to categories to match the number of angles and values
                categories += [categories[0]]

                # Calculate the angles for the radar chart
                angles = [n / float(len(values)) * 2 * 3.14 for n in range(len(values))]

                # Create the radar chart
                fig = plt.figure(figsize=(6, 6))
                ax = fig.add_subplot(111, polar=True)

                # Set the angle for the first category at the top
                ax.set_theta_offset(3.14 / 2)
                ax.set_theta_direction(-1)

                # Set the limits for the radial axis
                ax.set_ylim(0, 10)

                # Plot the data on the radar chart
                ax.plot(angles, values, color='blue', linewidth=2, linestyle='solid')

                # Fill the area under the curve
                ax.fill(angles, values, color='blue', alpha=0.4)

                # Set the labels for the categories
                ax.set_xticks(angles)
                ax.set_xticklabels(categories)

                # Display the plot
                col1.markdown(f'<h3 style="color: red; text-align: center;">Health Radar Chart</h3>', unsafe_allow_html=True)
                col1.pyplot(fig)

                numerical_columns = ['weight', 'sleep_duration', 'quality_of_sleep', 'physical_activity_level', 'stress_level', 
                     'blood_pressure', 'heart_rate', 'daily_steps', 'respiratory_rate', 'blood_volume', 
                     'calories_burned', 'body_temperature', 'drinking_water', 'daily_usage_of_smart_phone']

                # Compute the correlation matrix
                correlation_matrix = df[numerical_columns].corr()

                # Generate the heatmap
                fig = plt.figure(figsize=(10, 8))
                sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
                col2.markdown(f'<h3 style="color: blue; text-align: center;">Correlation Matrix</h3>', unsafe_allow_html=True)
                col2.pyplot(fig)
        else:
            st.error("No data available for analytics.")    


    elif select == 'Statistics':
        st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url("https://media.istockphoto.com/id/911633218/vector/abstract-geometric-medical-cross-shape-medicine-and-science-concept-background.jpg?s=612x612&w=0&k=20&c=eYz8qm5xa5wbWCWKgjOpTamavekYv8XqPTA0MC4tHGA=");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-color: rgba(255, 255, 255, 0.5);
            background-blend-mode: overlay;
        }
        </style>
        """,
        unsafe_allow_html=True
        )
        alerts=0
        st.markdown("<h1 style='text-align: center; color: #d65804;'>Statistics of Patient</h1>", unsafe_allow_html=True)
        try:
            daily_data = fetch_all_daily(user[2])
            daily_data_df = pd.DataFrame(daily_data)
            if daily_data_df.empty:
                st.error("No data available for statistics.")
            else:
                columns = ['ID','mail', 'weight', 'sleep_duration', 'quality_of_sleep',
                            'physical_activity_level', 'stress_level', 'BMI_category', 'blood_pressure', 'heart_rate',
                            'daily_steps', 'respiratory_rate', 'blood_volume', 'calories_burned', 'body_temperature',
                            'drinking_water', 'daily_usage_of_smart_phone']
                #make a dataframe with column names
                daily_data_df.columns=columns
                df=daily_data_df.drop(['ID','mail'],axis=1)
                st.write(df)
                weight_diff = df['weight'].diff()
                if max(diff < 0 for diff in weight_diff):
                    st.error("Alert: Weight is gradually decreasing!")
                    alerts+=1
                    st.divider()
                # If all differences are positive, weight is increasing
                elif max(diff > 0 for diff in weight_diff):
                    st.error("Alert: Weight is gradually increasing!")
                    alerts+=1
                    st.divider()
                duration_diff = df['sleep_duration'].diff()
                # If all differences are negative, sleep duration is decreasing
                if max(diff < 0 for diff in duration_diff):
                    st.error("Alert: Sleep duration is decreasing. Consider regulating sleep for 6 hours regularly.")
                    alerts+=1
                    st.divider()
                quality_diff = df['quality_of_sleep'].diff()
                    # If all differences are negative, quality of sleep is decreasing
                if max(diff < 0 for diff in quality_diff):
                    st.error("Alert: Quality of sleep is consistently decreasing. Consider consulting a healthcare professional.")
                    alerts+=1
                    st.success("Suggestion: Keep a consistent sleep schedule, create a relaxing bedtime routine, and avoid caffeine and electronics before bed.")
                    st.divider()
                activity_diff = df['physical_activity_level'].diff()
                    # If all differences are negative, physical activity level is decreasing
                if max(diff < 0 for diff in activity_diff):
                    st.error("Alert: Physical activity level is consistently decreasing. Consider incorporating more exercise into your routine.")
                    alerts+=1
                    st.success("Suggestion: Aim for at least 150 minutes of moderate-intensity aerobic activity or 75 minutes of vigorous-intensity activity per week, along with muscle-strengthening activities on two or more days per week.")
                    st.divider()
                stress_diff = df['stress_level'].diff()
                    # If all differences are positive, stress level is consistently increasing
                if max(diff > 0 for diff in stress_diff):
                    st.error("Alert: Stress level is consistently increasing. It's important to take steps to manage stress.")
                    alerts+=1
                    st.success("Suggestion: Practice stress-reduction techniques such as deep breathing, meditation, exercise, and maintaining a healthy lifestyle. Consider seeking support from a therapist or counselor if needed.")
                    st.divider()
                systolic_diff = df['blood_pressure'].diff()
                if max(diff > 0 for diff in systolic_diff):
                    alerts+=1
                    st.error("Alert: Blood pressure is consistently increasing. Monitor your blood pressure regularly and consider consulting a healthcare professional.")
                    st.success("Suggestion: Implement lifestyle changes such as reducing sodium intake, increasing physical activity, maintaining a healthy weight, and managing stress.")
                    st.divider()
                # If all differences are negative for systolic and diastolic, blood pressure is consistently decreasing
                elif max(diff < 0 for diff in systolic_diff):
                    alerts+=1
                    st.error("Alert: Blood pressure is consistently decreasing. Monitor your blood pressure regularly and consider consulting a healthcare professional.")
                    st.success("Suggestion: Monitor your blood pressure closely and consult with a healthcare provider to ensure it's within a healthy range.")
                    st.divider()
                rate_diff = df['heart_rate'].diff()
                # If all differences are negative, heart rate is consistently decreasing
                if max(diff < 0 for diff in rate_diff):
                    alerts+=1
                    st.error("Alert: Heart rate is consistently decreasing. Monitor your heart rate and consider consulting a healthcare professional.")
                    st.success("Suggestion: Focus on cardiovascular exercises, maintain a healthy diet, and manage stress levels to improve heart health.")
                    st.divider()
                # If all differences are positive, heart rate is consistently increasing
                elif max(diff > 0 for diff in rate_diff):
                    alerts+=1
                    st.error("Alert: Heart rate is consistently increasing. Monitor your heart rate and consider consulting a healthcare professional.")
                    st.success("Suggestion: Check for factors such as physical exertion, stress, or caffeine intake that might be causing the increase. Consider consulting with a healthcare provider for further evaluation.")
                    st.divider()
                if df['daily_steps'].sum() == 0:
                    alerts+=1
                    st.error("Alert: No steps recorded. It's important to stay active throughout the day.")
                    st.success("Suggestion: Aim to incorporate physical activity into your daily routine. Start with small, achievable goals and gradually increase your activity level.")
                    st.divider()
                # If steps are consistently decreasing
                elif max(df['daily_steps'].iloc[i] >= df['daily_steps'].iloc[i + 1] for i in range(len(df) - 1)):
                    alerts+=1
                    st.error("Alert: Daily steps are consistently decreasing. It's important to maintain physical activity levels.")
                    st.success("Suggestion: Find activities you enjoy and set specific goals to increase your daily step count. Consider walking meetings, taking the stairs, or going for a walk during breaks.")
                    st.divider()
                # If steps are not consistently maintained
                else:
                    alerts+=1
                    st.error("Alert: Daily steps are not consistently maintained. It's important to strive for regular physical activity.")
                    st.success("Suggestion: Set a daily step goal and track your progress using a pedometer or smartphone app. Try to incorporate walking into your daily routine, such as walking instead of driving for short trips.")
                    st.divider()
                rate_diff = df['respiratory_rate'].diff()
                # If all differences are negative, respiration rate is consistently decreasing
                if max(diff < 0 for diff in rate_diff):
                    alerts+=1
                    st.error("Alert: Respiration rate is consistently decreasing. Monitor your respiratory health and consider consulting a healthcare professional.")
                    st.success("Suggestion: Practice deep breathing exercises, maintain good posture, and ensure proper hydration and ventilation in your environment.")
                    st.divider()
                avg_blood_volume = df['blood_volume'].mean()
                # Define thresholds for low and high blood volume levels
                low_threshold = avg_blood_volume * 0.9
                high_threshold = avg_blood_volume * 1.1
                # Check blood volume levels and provide recommendations
                if df['blood_volume'].min() < low_threshold:
                    alerts+=1
                    st.error("Alert: Blood volume is low. Consult with a healthcare professional for further evaluation.")
                    st.success("Suggestion: Ensure adequate hydration and consider consuming iron-rich foods to support healthy blood volume levels.")
                    st.divider()
                avg_calories_burned = df['calories_burned'].mean()
                # Define thresholds for low and high calories burned levels
                low_threshold = avg_calories_burned * 0.9
                high_threshold = avg_calories_burned * 1.1

                # Check calories burned levels and provide recommendations
                if df['calories_burned'].min() < low_threshold:
                    alerts+=1
                    st.error("Alert: Calories burned are low. Consider increasing physical activity.")
                    st.success("Suggestion: Incorporate more exercise into your routine, such as brisk walking, jogging, or cycling. Set achievable goals and track your progress.")
                    st.divider()
                elif df['calories_burned'].max() > high_threshold:
                    alerts+=1
                    st.error("Alert: Calories burned are high. Ensure a balanced approach to exercise and nutrition.")
                    st.success("Suggestion: Maintain a well-rounded diet with plenty of fruits, vegetables, lean proteins, and whole grains. Avoid overexertion and ensure adequate rest and recovery.")
                    st.divider()
                normal_low = 97.0
                normal_high = 99.0
                # Check if any temperature readings are outside the normal range
                if max(temp < normal_low or temp > normal_high for temp in df['body_temperature']):
                    alerts+=1
                    st.error("Alert: Body temperature is outside the normal range.")
                    st.success("Suggestion: If you have a fever (temperature above 100.4°F or 38°C), consult a healthcare professional. Otherwise, monitor your temperature and consider rest and hydration if you feel unwell.")
                    st.divider()
                # Define recommended water intake levels
                recommended_low = 2.0  # liters
                recommended_high = 4  # liters
                # Check if any water intake readings are below the recommended range
                if max(water < recommended_low for water in df['drinking_water']):
                    alerts+=1
                    st.error("Alert: Drinking water intake is below the recommended range.")
                    st.success("Suggestion: Increase your water intake to ensure proper hydration. Aim to drink at least 8 glasses (approximately 2 liters) of water per day.")
                    st.divider()
                # Define recommended smartphone usage range
                recommended_low = 0  # hours (minimum)
                recommended_high = 2  # hours (maximum for healthy usage)
                # Check if any usage time readings are above the recommended maximum
                if max(usage > recommended_high for usage in df['daily_usage_of_smart_phone']):
                    alerts+=1
                    st.error("Alert: Daily usage time of smartphone is above the recommended range.")
                    st.success("Suggestion: Limit screen time and take breaks from smartphone use. Consider setting usage limits or using apps that track and manage screen time.")
                    st.divider()
                #scale the data
                from sklearn.preprocessing import StandardScaler
                sc=StandardScaler()
                df_scaled=sc.fit_transform(df.drop(['BMI_category'],axis=1))
                #take the last row of the data 
                #i have only 13 features in last row but model needs 16 features so i will add 0 to the missing features
                import numpy as np
                data=df_scaled[-1:]
                data=np.append(data,[0,0])
                cluster=model.predict([data])
                if alerts<=3 or cluster==0:
                    st.markdown(f'<h1 style="color: green; text-align: center;">Low Risk, Stay Healthy</h1>', unsafe_allow_html=True)
                elif alerts<=6 or cluster==1:
                    st.markdown(f'<h1 style="color: orange; text-align: center;">Moderate Risk, Do Regular Checkups</h1>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<h1 style="color: red; text-align: center;">Consult a Doctor</h1>', unsafe_allow_html=True)
                    col1,col2,col3=st.columns(3)
                    col2.image("https://png.pngtree.com/png-clipart/20230816/original/pngtree-doctor-consultation-icon-visit-vector-consultation-vector-picture-image_10832751.png",use_column_width=True)
        except Exception as e:
            st.error('Only few data points available for statistics. Try again Tomorrow 📆')
    elif select == 'Logout':
        st.session_state["logged_in"] = False
        st.session_state["current_user"] = None
        navigate_to_page("home")
