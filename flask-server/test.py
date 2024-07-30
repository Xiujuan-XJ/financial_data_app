from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
load_dotenv()

app=Flask(__name__)

#Mmbers API route
@app.route('/members')
def members():
    return {'members': ['Alice', 'Bob','dummies']}

if __name__ == '__main__':
    app.run(debug=True,port=8000)