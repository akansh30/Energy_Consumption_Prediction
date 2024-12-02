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
        st.markdown("""
        <style>
        .stApp {
            background-color: #E3F2FD; /* Light Blue Background */
            color: #0D47A1; /* Dark Blue Text */
        }
        .main-header {
            background: linear-gradient(135deg, #2196F3 0%, #64B5F6 100%);
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
            color: #0D47A1; /* Dark Blue Text inside prediction cards */
        }
        .stButton > button {
            background-color: #1E88E5; /* Blue Button */
            color: white;
            border-radius: 12px;
            padding: 10px 20px;
            border: none;
            font-size: 16px;
        }
        .stButton > button:hover {
            background-color: #1565C0; /* Darker Blue on hover */
        }
        .blue-text {
            color: #0D47A1; /* Dark Blue Text */
            font-weight: bold;
            font-size: 18px;
        }
        </style>
        """, unsafe_allow_html=True)

    def load_resources(self):
        try:
            self.linear_model = joblib.load("pkl_folder/linear_model.pkl") 
            self.ridge_model = joblib.load("pkl_folder/ridge_model.pkl")
            self.feature_names = joblib.load("pkl_folder/feature_names.pkl")
        except Exception as e:
            st.error(f"Error loading resources: {e}")

    def run(self):
        st.markdown("<div class='main-header'><h1>⚡ Energy Consumption Prediction</h1></div>", unsafe_allow_html=True)

        # Organize features into two columns
        st.markdown("<span class='blue-text'>⚙️ Enter Feature Values:</span>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<span style="color: #0D47A1; font-weight: bold;">Voltage (V)</span>', unsafe_allow_html=True)
            voltage = st.number_input("", min_value=220.0, max_value=255.0, value=240.0, step=0.1)

            st.markdown('<span style="color: #0D47A1; font-weight: bold;">Global Intensity (A)</span>', unsafe_allow_html=True)
            global_intensity = st.number_input("", min_value=0.0, max_value=20.0, value=4.63, step=0.1)

            st.markdown('<span style="color: #0D47A1; font-weight: bold;">Sub Metering 1 (Wh)</span>', unsafe_allow_html=True)
            sub_metering_1 = st.number_input("", min_value=0.0, max_value=50.0, value=1.12, step=0.1)

        with col2:
            st.markdown('<span style="color: #0D47A1; font-weight: bold;">Sub Metering 2 (Wh)</span>', unsafe_allow_html=True)
            sub_metering_2 = st.number_input("", min_value=0.0, max_value=50.0, value=1.30, step=0.1)

            st.markdown('<span style="color: #0D47A1; font-weight: bold;">Sub Metering 3 (Wh)</span>', unsafe_allow_html=True)
            sub_metering_3 = st.number_input("", min_value=0.0, max_value=50.0, value=6.46, step=0.1)

        st.markdown("---")

        # Date and Time inputs
        st.markdown("<span class='blue-text'>📅 Date and Time Inputs</span>", unsafe_allow_html=True)
        st.markdown('<span style="color: #0D47A1; font-weight: bold;">Select Date</span>', unsafe_allow_html=True)
        date = st.date_input("", value=pd.Timestamp("2024-11-28"))
        
        st.markdown('<span style="color: #0D47A1; font-weight: bold;">Select Time</span>', unsafe_allow_html=True)
        time = st.time_input("", value=pd.Timestamp("2024-11-28 12:00:00").time())

        # Convert Date and Time to derived features
        date_time = pd.Timestamp.combine(date, time)
        year, month, day, hour, minute = date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute
        is_holiday = 0  # Default: Not a holiday
        light = 1       # Default: Daylight
        weekday = date_time.weekday()

        # Prepare input data
        input_data = pd.DataFrame({
            "Global_reactive_power": [0.0],
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
        })[self.feature_names]

        # Button for predictions
        if st.button("🔮 Predict Energy Consumption"):
            try:
                linear_pred = self.linear_model.predict(input_data)[0]
                ridge_pred = self.ridge_model.predict(input_data)[0]

                # Display predictions
                st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                st.markdown('<span style="color: #1E88E5; font-size: 24px; font-weight: bold;">🔮 Predictions</span>', unsafe_allow_html=True)
                st.write(f"**Linear Regression Prediction:** {linear_pred:.2f} kW")
                st.write(f"**Ridge Regression Prediction:** {ridge_pred:.2f} kW")
                st.markdown('</div>', unsafe_allow_html=True)

            except ValueError as e:
                st.error(f"Prediction error: {e}")


# Main function to run the app
def main():
    app = EnergyConsumptionApp()
    app.run()


if __name__ == "__main__":
    main()
