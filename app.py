from flask import Flask, redirect, request, jsonify, render_template
import requests
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.debug = True

toolbar = DebugToolbarExtension(app)

url = 'https://api.exchangerate.host/convert?'
response = requests.get(url)
data = response.json()

@app.route('/')
def home_page():
    # Inital Page #
    
    return render_template('index.html')


@app.route('/convert', methods=["GET","POST"])
def show_conversion():
        
    # Makes sure conversion inputs are UpperCase #
    input = request.args.get('input')
    output = request.args.get('output')
    amount = request.args.get('amount')
    
    # Adds user inputs into url for conversion #
    new_url = url+f"from={input.upper()}"+f"&to={output.upper()}"+f"&amount={amount}"
    
    new_response = requests.get(new_url)
    
    new_data = new_response.json()

    if len(input) is not 3 and len(output) is 3:
        input = "USD (Default)"
        new_url = url+f"from=USD"+f"&to={output}"+f"&amount={amount}"
        new_response = requests.get(new_url)
        new_data = new_response.json()
        result_to_str = round(new_data['result'],2)
        result_str = str(result_to_str)
        return render_template('base.html',input=input,to=output,
                           amount=amount,result=result_str,url=new_url)
    elif len(output) is 3:
        result_to_str = round(new_data['result'],2)
        result_str = str(result_to_str)
        return render_template('base.html',input=input.upper(),to=output.upper(),
                           amount=amount,result=result_str,url=new_url)
    else:
        return render_template('index.html')
