# AQI Prediction System

## Overview

The AQI Prediction System is a Machine Learning-based web application that predicts the Air Quality Index (AQI) using environmental parameters. The project helps users assess air quality levels and promotes environmental awareness by providing quick and accurate AQI predictions.

## Features

* Predicts Air Quality Index (AQI) using machine learning models.
* User-friendly web interface built with Streamlit.
* Data preprocessing and feature engineering.
* Real-time AQI prediction based on user inputs.
* Model serialization using Pickle files for efficient deployment.

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit
* Pickle

## Project Structure

AQI-Prediction-System/
│
├── app.py                  # Streamlit web application
├── aqi_model.pkl           # Trained machine learning model
├── features.pkl            # Feature information
├── requirements.txt        # Required dependencies
├── AQI_Prediction.ipynb    # Model development notebook
└── README.md

## Installation

1. Clone the repository:

git clone https://github.com/priya-1339/AQI-Prediction-System.git

2. Navigate to the project directory:

cd AQI-Prediction-System

3. Install dependencies:

pip install -r requirements.txt

4. Run the application:

streamlit run app.py

## Usage

1. Enter the required air quality parameters.
2. Click the Predict button.
3. View the predicted AQI value and corresponding air quality assessment.

## Machine Learning Workflow

* Data Collection
* Data Cleaning and Preprocessing
* Feature Selection
* Model Training
* Model Evaluation
* Model Deployment using Streamlit

## Future Enhancements

* Integration with live air quality APIs.
* AQI forecasting for future dates.
* Interactive visualizations and dashboards.
* Support for multiple cities and regions.

## Author

Priyadarshini Amara

B.Tech (Data Science)

## License

This project is intended for educational and research purposes.
