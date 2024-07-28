from flask import Flask, request, jsonify, send_file
import pandas as pd
import matplotlib.pyplot as plt
import io
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return "Welcome to the Financial Data Visualization WebApp"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        data = pd.read_csv(filepath)
        summary = process_data(data)
        return jsonify({"message": "File uploaded successfully", "summary": summary.to_dict()})
    else:
        return jsonify({"error": "Invalid file type"})

def process_data(data):
    # Example: Summarize data by category
    summary = data.groupby('category').sum().reset_index()
    return summary

def generate_chart(data, chart_type='bar'):
    plt.figure(figsize=(10, 6))
    if chart_type == 'bar':
        plt.bar(data['category'], data['amount'])
    elif chart_type == 'pie':
        plt.pie(data['amount'], labels=data['category'], autopct='%1.1f%%')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

@app.route('/chart', methods=['GET'])
def get_chart():
    chart_type = request.args.get('type', 'bar')
    data = pd.read_csv(os.path.join(UPLOAD_FOLDER, 'yourfile.csv'))  # Replace 'yourfile.csv' with actual uploaded file name
    summary = process_data(data)
    chart = generate_chart(summary, chart_type)
    return send_file(chart, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
