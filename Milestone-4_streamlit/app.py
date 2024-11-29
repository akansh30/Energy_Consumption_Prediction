import pandas as pd
import streamlit as st  # type: ignore
import joblib

class EnergyConsumptionApp:
    def __init__(self):
        st.set_page_config(
            page_title="Energy Consumption Prediction App",
            page_icon="⚡",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        self.setup_page()
        self.load_resources()

    def setup_page(self):
        # Set a fixed background and text color
        st.markdown("""
        <style>
        .stApp {
            background-color: #E8F5E9; /* Light Pastel Green Background */
            color: #2E7D32; /* Dark Green Text */
        }
        .main-header {
            background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .prediction-card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            color: #2E7D32; /* Dark Green Text inside prediction cards */
        }
        </style>
        """, unsafe_allow_html=True)

    def load_resources(self):
        try:
            # Load models and feature names
            self.linear_model = joblib.load("pkl_folder/linear_model.pkl") 
            self.ridge_model = joblib.load("pkl_folder/ridge_model.pkl")
            self.feature_names = joblib.load("pkl_folder/feature_names.pkl")
            st.success("Resources loaded successfully!")
        except Exception as e:
            st.error(f"Error loading resources: {e}")

    def run(self):
        st.markdown("<div class='main-header'><h1>⚡ Energy Consumption Prediction</h1></div>", unsafe_allow_html=True)

        st.sidebar.markdown("## ⚙️ Feature Input")

        # Feature inputs for the model
        voltage = st.sidebar.slider("Voltage (V)", 220.0, 255.0, 240.0)
        global_intensity = st.sidebar.slider("Global Intensity (A)", 0.0, 20.0, 4.63)
        sub_metering_1 = st.sidebar.slider("Sub Metering 1 (Wh)", 0.0, 50.0, 1.12)
        sub_metering_2 = st.sidebar.slider("Sub Metering 2 (Wh)", 0.0, 50.0, 1.30)
        sub_metering_3 = st.sidebar.slider("Sub Metering 3 (Wh)", 0.0, 50.0, 6.46)

        # DateTime inputs
        date = st.sidebar.date_input("Select Date", value=pd.Timestamp("2024-11-28"))
        time = st.sidebar.time_input("Select Time", value=pd.Timestamp("2024-11-28 12:00:00").time())

        # Convert Date and Time to derived features
        date_time = pd.Timestamp.combine(date, time)
        year = date_time.year
        month = date_time.month
        day = date_time.day
        hour = date_time.hour
        minute = date_time.minute

        # Assume default values for additional features
        is_holiday = 0  # Default: Not a holiday
        light = 1       # Default: Daylight
        weekday = date_time.weekday()  # Extract weekday (0=Monday, 6=Sunday)

        # Prepare input data with all features
        input_data = pd.DataFrame({
            "Global_reactive_power": [0.0],  # Default or slider value
            "Voltage": [voltage],
            "Global_intensity": [global_intensity],
            "Sub_metering_1": [sub_metering_1],
            "Sub_metering_2": [sub_metering_2],
            "Sub_metering_3": [sub_metering_3],
            "Year": [year],
            "Month": [month],
            "Day": [day],
            "Hour": [hour],
            "Minute": [minute],
            "Is_holiday": [is_holiday],
            "Light": [light],
            "Weekday": [weekday]
        })[self.feature_names]  # Ensure correct feature order

        # Predictions
        try:
            linear_pred = self.linear_model.predict(input_data)[0]
            ridge_pred = self.ridge_model.predict(input_data)[0]

            # Display predictions
            st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
            st.subheader("🔮 Predictions")
            st.write(f"**Linear Regression Prediction:** {linear_pred:.2f} kW")
            st.write(f"**Ridge Regression Prediction:** {ridge_pred:.2f} kW")
            st.markdown('</div>', unsafe_allow_html=True)

        except ValueError as e:
            st.error(f"Prediction error: {e}")

        st.markdown("""
<div style="
    background-color: #FBE9E7; /* Light peach background */
    color: #D84315; /* Dark orange text */
    border: 2px solid #FFAB91; /* Lighter orange border */
    border-radius: 8px;
    padding: 15px;
    margin-top: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
">
<h3>📜 Disclaimer</h3>
<p><strong>Important Notice:</strong></p>
<ul>
<li>This tool provides energy consumption predictions based on historical data.</li>
<li>It is intended for informational purposes only.</li>
<li>For critical energy planning, consult a certified energy expert.</li>
</ul>
</div>
""", unsafe_allow_html=True)



# Main function to run the app
def main():
    app = EnergyConsumptionApp()
    app.run()


if __name__ == "__main__":
    main()