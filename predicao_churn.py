import pickle

import pandas as pd
import numpy as np
from flask import Flask, render_template, request

# Setar as pastas de template e assets
app = Flask(__name__, template_folder='template', static_folder='template/assets')

# Importando o modelo
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
    df = df[['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure',
             'Balance', 'NumOfProducts', 'HasCrCard', 'EstimatedSalary', 'IsActiveMember',
             ]]

    prediction = modelo_pipeline.predict(df)
    proba = np.ravel(modelo_pipeline.predict_proba(df))
    prob = str(round(proba[1]*100, 2))
    outcome = 'Esse cliente vai embora!'
    outcome2 = "Probabilidade de Churn: " + prob + "%"
    imagem = 'sad.jpg'
    if prediction == 0:
        prob = str(round(proba[0]*100, 2))
        outcome = 'Esse cliente vai ficar!'
        outcome2 = "Probabilidade de Retenção: " + prob + "%"
        imagem = 'happy.jpg'

    return render_template('result.html', tables=[df.to_html(classes='data', header=True, col_space=10)],
                           result=outcome, imagem=imagem, result2=outcome2)


if __name__ == "__main__":
    app.run(debug=True)
