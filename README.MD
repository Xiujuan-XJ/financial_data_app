# Financial Data Visualization Web Application

## Overview

This web application allows users to upload CSV files containing financial data and visualizes the data using interactive charts. It consists of a Flask backend for data processing and a React frontend for user interaction and data display.

## Features

- CSV file upload
- Data processing and analysis
- Interactive charts (Pie chart ,Bar chart & line chart for expenses)
- Responsive design

## Tech Stack

- Backend: Flask (Python)
- Frontend: React (JavaScript)
- Charts: Chart.js with react-chartjs-2

## Prerequisites

- Python 3.12
- Node.js 14+
- npm 6+

## Installation

### Backend Setup

1. Download and unzip the zip folder

2. Set up a Python virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate 
   ```

3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd client
   ```

2. Install the required npm packages:
   ```
   npm install
   npm i react-chartjs-2 chart.js
   ```

## Running the Application

1. Start the Flask backend:
   ```
   cd flask-server
   python3 app.py
   ```
   The backend will start running on `http://localhost:8000`. 
   To test it you may wanan try http://http://127.0.0.1:8000/ to see whether it has webUI   

2. In a new terminal, start the React frontend:
   ```
   cd client
   npm run dev
   ```
   The frontend will start running on `http://localhost:3000`.

3. Open your web browser and visit `http://http://localhost:5173/` to use the application.

## Usage

1. Prepare a CSV file with your financial data. The file should have the following columns:
   - Date: in the format YYYY-MM-DD
   - Category: the expense category
   - Amount: the expense amount
   - In the project we use '5_years_financial_data.csv' in the main directory

2. On the web application, click the "Choose File" button and select your CSV file.

3. Click the "Upload" button to upload and process your file.

4. Click 'view summary', the application will display chart according to your options:
   - A line chart 
   - A pie chart 
   - A bar chart 
   of The total category expenses over 5 years, Monthly expenses, yearly expenses, yearly expenses per category. 



## Contact

Xiujuan Guo - guoxiujuan1129@gmail.com

Project Link: https://github.com/your-username/financial-data-viz

