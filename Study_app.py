import streamlit as st
from io import BytesIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

df = pd.read_csv('student_test_scores.csv')

X = df[['study_hours']]
y = df['test_score']

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

Real_poly = PolynomialFeatures(degree = 2)
X_real_poly = Real_poly.fit_transform(X)

#retrain model on all data
retrain = LinearRegression()
retrain.fit(X_real_poly, y)

polypred = retrain.predict(X_real_poly)


from sklearn.metrics import r2_score, mean_absolute_error

r2 = r2_score(y, polypred)
mae = mean_absolute_error(y,polypred) 

st.markdown(
    "<h1 style='color:black;'>📘 Study Hours to Score Predictor</h1>",
    unsafe_allow_html=True
)


st.markdown(
    "<h3 style='color:black;'>📊 Model Performance</h3>",
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div style='color: black; font-size: 18px;'>
        🧠 <strong>R² Score:</strong> {round(r2, 4)} <br>
        📏 <strong>MAE:</strong> {round(mae, 2)}
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://i.imgur.com/rsunhtC.jpeg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)





st.markdown(
    """
    <style>
    .stNumberInput label {
        color: black !important;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown("<label style='color: black;'>Enter your name</label>", unsafe_allow_html=True)
username = st.text_input(" ", label_visibility="collapsed")

hours = st.number_input("Enter Study Hours", min_value=0.0, step=0.1)

# Example: Load your model and data
# model = trained LinearRegression()
# poly = trained PolynomialFeatures()

# User input

    
# Always show button
if st.button("Predict Score"):
    if not username.strip():
        st.error("❌ Please enter your name before predicting.")
    else:
        # Proceed with prediction if username is valid
        X_input = np.array([[hours]])
        X_input_poly = Real_poly.transform(X_input)
        score = retrain.predict(X_input_poly)[0]


    # Store data in CSV
        log_entry = {
            'Name': username,
            'Study Hours': hours,
            'Predicted Score': round(score, 2),
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        log_df = pd.DataFrame([log_entry])
        csv_file = "user_predictions_log.csv"
        if os.path.exists(csv_file):
            log_df.to_csv(csv_file, mode='a', header=False, index=False)
        else:
            log_df.to_csv(csv_file, mode='w', header=True, index=False)
    
    
        # Display styled prediction
        # If score is negative, show red box and set score to 0
        if score < 0:
           
            score = 0  # Set to zero after display
            st.markdown(
                f"""
                <div style='
                    background-color: #ff4d4d;
                    color: white;
                    padding: 12px 18px;
                    border-radius: 8px;
                    font-size: 18px;
                    font-weight: bold;
                    margin-top: 10px;
                '>
                    ⚠️ Predicted Test Score was negative. Set to 0.
                </div>
                """,
                unsafe_allow_html=True
            )
            
        else:
            st.markdown(
                f"""
                <div style='
                    background-color: black;
                    color: white;
                    padding: 12px 18px;
                    border-radius: 8px;
                    font-size: 18px;
                    font-weight: bold;
                    margin-top: 10px;
                '>
                    🎯 Predicted Test Score: {score:.2f}
                </div>
                """,
                unsafe_allow_html=True
            )
    
    
        # Custom feedback message
            # Custom feedback message with bright backgrounds
        if hours >= 9.50:
            st.markdown(
                """
                <div style='
                    background-color: #fff3cd;
                    color: #856404;
                    padding: 15px;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: bold;
                    border: 1px solid #ffeeba;
                    text-align: center;
                '>
                    ⚠️ You’ve studied a lot — consider taking a break!
                </div>
                """,
                unsafe_allow_html=True
            )
    
        elif hours <= 0.3:
            st.markdown(
                """
                <div style='
                    background-color: #90EE90;
                    color: #60190c;
                    padding: 15px;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: bold;
                    border: 1px solid #bee5eb;
                    text-align: center;
                '>
                    ℹ️ A bit more study time might help improve your score!
                </div>
                """,
                unsafe_allow_html=True
            )
    
        elif 0.4 <= hours <= 9.49:
            st.markdown(
                """
                <div style='
                    background-color: #d1ecf1;
                    color: #0c5460;
                    padding: 15px;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: bold;
                    border: 1px solid #bee5eb;
                    text-align: center;
                '>
                    ✅ Great balance — keep it up!
                </div>
                """,
                unsafe_allow_html=True
            )
        
       
    
    
        # Plot regression line and user's point
        X_range = np.linspace(0, 10, 100).reshape(-1, 1)
        y_range = retrain.predict(Real_poly.transform(X_range))
        
    
    
        with plt.style.context('dark_background'):
            
            fig, ax = plt.subplots(figsize=(8, 5), facecolor='black')  # Make figure background black
            ax.set_facecolor('black')  # Make plot area background black
            
            ax.plot(X_range, y_range, label='Regression Line', color='cyan')
            ax.scatter(hours, score, color='yellow', s=100, label='Your Prediction')
            
            ax.set_xlabel("Study Hours", color='white')
            ax.set_ylabel("Predicted Score", color='white')
            ax.set_title(f"{username}'s Study Hours vs Predicted Test Score", color='white')
            
            ax.tick_params(colors='white')  # Make axis ticks white
            ax.grid(True, color='gray')
            ax.legend()
            
            st.pyplot(fig)  # ✅ Use fig, not plt
            
            buffer = BytesIO()
            fig.savefig(buffer, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())
            buffer.seek(0)
    
            st.download_button(
                label="📥 Download This Chart as PNG",
                data=buffer,
                file_name=f"{username}_score_chart.png",
                mime="image/png"
            )
            
            if os.path.exists("user_predictions_log.csv"):
                
                st.markdown("<h3 style='color: black;'>🗂️ Past User Predictions</h3>", unsafe_allow_html=True)
    
                log_display = pd.read_csv("user_predictions_log.csv")
                log_display['Predicted Score'] = log_display['Predicted Score'].apply(lambda x: max(0, x))
                st.dataframe(log_display)
            


            
        
   
# Step 1: Prepare X_range and prediction line
X_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
y_range = retrain.predict(Real_poly.transform(X_range))

# Step 2: Plot
with plt.style.context('dark_background'):
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='black')
    ax.set_facecolor('black')

    # Scatter plot of actual data
    ax.scatter(X, y, color='yellow', s=60, label='Actual Data')

    # Polynomial regression line
    ax.plot(X_range, y_range, color='cyan', linewidth=2.5, label='Polynomial Regression Line')

    ax.set_xlabel("Study Hours", color='white')
    ax.set_ylabel("Test Score", color='white')
    ax.set_title("Polynomial Regression Fit", color='white')
    ax.tick_params(colors='white')
    ax.grid(True, color='gray')
    ax.legend()

    st.pyplot(fig)


df_results = pd.DataFrame({
    'Study Hours': X['study_hours'],           
    'Actual Score': y,
    'Predicted Score': polypred.astype(int)
})
df_results

