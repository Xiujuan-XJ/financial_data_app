from flask import Flask,request,render_template,redirect,url_for,jsonify,send_from_directory,send_file
from werkzeug.utils import secure_filename
from datetime import datetime
import pandas as pd
import os
import process 
import matplotlib.pyplot as plt
from flask_cors import CORS, cross_origin
import json
from collections import defaultdict

app = Flask(__name__)
cors = CORS(app)

UPLOAD_FOLDER = 'uploads'
CHART_FOLDER = 'charts'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = set('csv')


#set file type constraints
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # if 'file' not in request.files:
    #     return jsonify({'error': 'No file part'}), 400
    if request.method == 'POST':
        file=request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if not file or not file.filename.endswith('.csv'):
            return jsonify({'error': 'Invalid file type'}), 400
        filename=secure_filename(file.filename)
        file_path=os.path.join(UPLOAD_FOLDER,filename)
        file.save(file_path) #save raw data
        data = pd.read_csv(file_path,parse_dates = ['Date'],dayfirst=True)

        summary = summarize_data(data)
        # save summary
        summary_path = os.path.join(UPLOAD_FOLDER, 'summary.csv')
        #charts = generate_charts(data)
        
        # preprocess the data & save data
        yearly_expenses=process_data(data)
        
        return jsonify({"message": "File uploaded successfully","yearly_expenses":yearly_expenses}),200
  
    return render_template('upload.html')

def summarize_data(data):
    # Example: Summarize data by category
    summary = data.groupby('Category').sum().reset_index()
    return summary


def process_data(data):
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    res=defaultdict()

    # calculate yearly expenses
    data['Year'] = data['Year'].astype(str)
    yearly_expenses = data.groupby(['Year'],as_index=False).agg({'Amount':'sum'}).rename(columns={"Year": "category", "Amount": "amount"}).to_dict(orient='dict')
   
    # Calculate Monthly expenses
    data['year_month'] = data['Year'].astype(str)+'-'+data['Month'].astype(str)
    monthly_expenses = data.groupby(['year_month'],as_index=False).agg({'Amount':'sum'}).rename(columns={"year_month": "category", "Amount": "amount"}).to_dict(orient='dict')
    monthly_expenses
    
    # Calculate total expenses by category
    category_totals = data.groupby('Category',as_index=False).agg({'Amount':'sum'}).rename(columns={"Category": "category", "Amount": "amount"}).to_dict(orient='dict')

    # caluclate yearly expenses by category
    data['category_yearly'] = data['Category']+' '+data['Year'].astype(str)
    yearly_expenses_per_category=data.groupby(['category_yearly'],as_index=False).agg({'Amount':'sum'}).rename(columns={"category_yearly": "category", "Amount": "amount"}).to_dict(orient='dict')

    
    res={'yearly_expenses':yearly_expenses,
    'monthly_expenses': monthly_expenses,
    'category_totals': category_totals,
    'yearly_expenses_per_category': yearly_expenses_per_category
    }

    with open(os.path.join(CHART_FOLDER,'yearly_expenses.json'), 'w',encoding='utf-8') as outfile:
        #json.dumps(yearly_expenses, default=pd.DataFrame.to_dict)#outfile.write(yearly_expenses)
        json.dump(res, outfile, ensure_ascii=True, indent=4)
    return res


def calculate_yearly_expenses(data):
    yearly_expenses = data.groupby(['Year'],as_index=False).agg({'Amount':'sum'}).to_dict('records')
    with open(os.path.join(CHART_FOLDER,'yearly_expenses.json'), 'w',encoding='utf-8') as outfile:
        json.dump(yearly_expenses, outfile, ensure_ascii=True, indent=4)
    return yearly_expenses



@app.route('/read', methods=['GET'])
def read_data():
    path=os.path.join(CHART_FOLDER,'yearly_expenses.json') 
    f = open(path)    
    res=json.load(f) 
    return jsonify(res)               
    
    
@app.route('/extract',methods=['GET'])
def extract_data(file_path):
    res=dict()
    df = pd.read_csv(file_path, parse_dates = ['Date'],dayfirst=True)
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    
    
    
    # Calculate yearly expenses
    yearly_expenses = df.groupby(['Year'],as_index=False).agg({'Amount':'sum'}).rename(columns={"Year": "category", "Amount": "amount"}).to_json(orient='records')
    
    
    # Calculate Monthly expenses
    monthly_expenses = df.groupby(['Year','Month'],as_index=False).rename(columns={"year_month": "category", "Amount": "amount"}).agg({'Amount':'sum'}).to_json(orient='records')

    
    # Calculate total expenses by category
    category_totals = df.groupby('Category',as_index=False).rename(columns={"Category": "category", "Amount": "amount"}).agg({'Amount':'sum'})
    category_totals_json=category_totals.to_json(orient='records')
    
    # caluclate yearly expenses by category
    yearly_expenses_per_category=df.groupby(['Category','Year'],as_index=False).rename(columns={"category_yearly": "category", "Amount": "amount"}).agg({'Amount':'sum'})
    yearly_expenses_per_category_json=yearly_expenses_per_category.to_json(orient='records')
    
    # Calculate total expenses 
    total_expenses = df['Amount'].sum()
    
    #return has 2 part: {'amount': 1000, 'category': 'food'}
    res={
    'category_totals': category_totals,
    'yearly_expenses': yearly_expenses,
    'monthly_expenses': monthly_expenses,
    'category_totals_json': category_totals_json,
    'yearly_expenses_per_category_json': yearly_expenses_per_category_json,
    'total_expenses': total_expenses
}
    return jsonify(res)
    
    

def generate_charts(data):
    charts = {}
    # Example pie chart
    plt.figure()
    data.groupby('Category')['Amount'].sum().plot.pie()
    pie_chart_path = os.path.join(CHART_FOLDER, 'pie_chart.png')
    plt.savefig(pie_chart_path)
    charts['pie_chart'] = pie_chart_path
    
    
    # Example bar chart
    plt.figure()
    data.groupby('Category')['Amount'].sum().plot.bar()
    bar_chart_path = os.path.join(CHART_FOLDER, 'bar_chart.png')
    plt.savefig(bar_chart_path)
    charts['bar_chart'] = bar_chart_path
    return charts


@app.route('/chart/<chart_name>', methods=['GET'])
def get_chart(chart_name):
    chart_path = os.path.join(CHART_FOLDER, chart_name)
    if os.path.exists(chart_path):
        return send_file(chart_path, mimetype='image/png')
    else:
        return jsonify({'error': 'Chart not found'}), 404
    
    
@app.route('/download')
def download():
    return render_template('download.html',files=os.listdir(UPLOAD_FOLDER))


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True,port=8000)
    



