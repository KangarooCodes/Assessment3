from flask import Flask, redirect, request, jsonify, render_template
import requests
from forex_python.converter import CurrencyRates


app = Flask(__name__)

url = 'https://api.exchangerate.host/convert?'
response = requests.get(url)
data = response.json()

@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/convert')
def show_conversion():
    input = request.args.get('input')
    input_upper = input.upper()
    output = request.args.get('output')
    output_upper = output.upper()
    amount = request.args.get('amount')
    amount_upper = amount.upper()
    
    new_url = url+f"from={input_upper}"+f"&to={output_upper}"+f"&amount={amount_upper}"
    
    new_response = requests.get(new_url)
    
    new_data = new_response.json()
    result_to_str = round(new_data['result'],2)
    result_str = str(result_to_str)
    
    print(request.args)
    print(data)
    
    return render_template('base.html',input=input_upper,to=output_upper,
                           amount=amount_upper,result=result_str,url=new_url)

# Below is a test page to see if conversion matches expectation
@app.route('/test')
def test_():
        
    new_url = 'https://api.exchangerate.host/convert?from=USD&to=USD&amount=1200'
    
    new_response = requests.get(new_url)
    
    new_data = new_response.json()
    result_to_str = round(new_data['result'],2)
    result_str = str(result_to_str)
    
    if result_str == '1200':
        return render_template('correct.html')
    else:
        return render_template('error.html')