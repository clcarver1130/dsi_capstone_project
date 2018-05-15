
from flask import Flask, render_template, request
import pickle
from api_pipeline import predict_default


app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET'])
def form():
    '''Render a page containing a form  where the user can input the borrower information'''
    return render_template('form.html')

@app.route('/predict', methods = ['POST', 'GET'])
def predict():
    data = request.form
    pred = predict_default(data)
    return render_template('predict.html', prediction=pred)

if __name__ == '__main__':
    app.run(debug=True, port=5008)
