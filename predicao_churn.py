import pickle

import pandas as pd
from flask import Flask, render_template, request

# molezinha, só tem que setar as pastas de template e assets
app = Flask(__name__, template_folder='template', static_folder='template/assets')

# Treina lá, usa cá
modelo_pipeline = pickle.load(open('models/pipe.pkl', 'rb'))


@app.route('/')
def home():
    return render_template("homepage.html")


@app.route('/dados_cliente')
def dados_cliente():
    return render_template("form.html")


def get_data():
    CreditScore = request.form.get('CreditScore')
    Geography = request.form.get('Geography')
    Gender = request.form.get('Gender')
    Age = request.form.get('Age')
    Tenure = request.form.get('Tenure')
    Balance = request.form.get('Balance')
    NumOfProducts = request.form.get('NumOfProducts')
    HasCrCard = request.form.get('HasCrCard')
    IsActiveMember = request.form.get('IsActiveMember')
    EstimatedSalary = request.form.get('EstimatedSalary')
   

    d_dict = {'CreditScore': [CreditScore], 'Geography': [Geography], 'Gender': [Gender],
              'Age': [Age], 'Tenure': [Tenure], 'Balance': [Balance],
              'NumOfProducts': [NumOfProducts], 'HasCrCard': [HasCrCard],
              'IsActiveMember': [IsActiveMember], 'EstimatedSalary': [EstimatedSalary]}

    return pd.DataFrame.from_dict(d_dict, orient='columns')


@app.route('/send', methods=['POST'])
def show_data():
    df = get_data()
    df = df[['Geography', 'Gender', 'CreditScore', 'Age', 'Tenure',
       'Balance', 'NumOfProducts', 'EstimatedSalary', 'HasCrCard',
       'IsActiveMember']]

    prediction = modelo_pipeline.predict(df)
    outcome = 'ESSE CLIENTE VAI EMBORA'
    outcome2 = 'ESSE CLIENTE VAI EMBORA'
    imagem = 'chefe_brabo.jpg'
    if prediction == 0:
        outcome = 'Ufa... esse cliente vai ficar!'
        outcome2 = 'Ufa... esse cliente vai ficar!'
        imagem = 'chefe_feliz.jpg'

    return render_template('result.html', tables=[df.to_html(classes='data', header=True, col_space=10)],
                           result=outcome, imagem=imagem, gitproba=proba)


if __name__ == "__main__":
    app.run(debug=True)
