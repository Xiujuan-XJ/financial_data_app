from flask import Flask,request,render_template,redirect,url_for,jsonify,send_from_directory,send_file
from werkzeug.utils import secure_filename
from datetime import datetime
import pandas as pd
import os
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
        #preprocess the data & save data
        yearly_expenses=process_data(data)
        #generate_charts(data)  
        #generate_charts(data)
        return jsonify({"message": "File uploaded successfully","yearly_expenses":yearly_expenses}),200
  
    return render_template('upload.html')

# def summarize_data(data):
#     # Example: Summarize data by category
#     summary = data.groupby('Category').sum().reset_index()
#     return summary


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
        json.dump(res, outfile, ensure_ascii=True, indent=4)
        
    return res



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
    
    

def generate_charts(df):
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    
    #barchart
    category_totals=df.groupby('Category',as_index=False).agg({'Amount':'sum'}).plot(kind='bar',x='Category',y='Amount',title='Total Amount Spent on Each Category',xlabel='Category',ylabel='Amount')
    bar_chart_path = os.path.join(CHART_FOLDER, 'category_totals.png')
    category_totals.figure.savefig(bar_chart_path)
    
    #line chart
    yearly_expenses_per_category=df.groupby(['Category','Year']).agg({'Amount':'sum'})
    for date, new_df in yearly_expenses_per_category.groupby(level = 0):
        plt.plot(new_df.index.get_level_values('Year').values,new_df['Amount'],label=new_df.index.get_level_values('Category')[0])
    plt.xlabel('Year')
    plt.ylabel('Amount')
    plt.title('Yearly Expenses per Category')
    plt.legend()
    line_chart_path = os.path.join(CHART_FOLDER, 'yearly_expenses_per_category.png')
    plt.savefig(line_chart_path)




if __name__ == '__main__':
    app.run(debug=True,port=8000)
    



