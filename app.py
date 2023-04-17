from flask import Flask, request, render_template
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
    input = request.form['input']
    output = request.form['output']
    amount = request.form['amount']
    
    
    # Adds user inputs into url for conversion #
    new_url = url+f"from={input}"+f"&to={output}"+f"&amount={amount}"
    
    new_response = requests.get(new_url)
    
    new_data = new_response.json()
    if input is not None and output is not None:
        if len(input) is not 3 or len(output) is not 3:
            error = "Please Fill In All Boxes"        
            return render_template('base.html',
                               error=error, input=input, to=output, amount=amount)
        elif not amount:
            error = "Please Fill In All Boxes"        
            return render_template('base.html',
                               error=error, input=input, to=output, amount=amount)
        else:
            result_to_str = round(new_data['result'],2)
            result_str = str(result_to_str)
            return render_template('base.html',input=input,to=output,
                           amount=amount,result=result_str,url=new_url)
    return "" #prevents "The view function for 'show_conversion' did not return a valid response."