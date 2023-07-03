from flask import Flask, Response, current_app, make_response, redirect, render_template, request, send_from_directory, session
import pandas as pd
from transformer import transform, predict_churn
import os
app = Flask(__name__, static_url_path='')
app.secret_key = os.urandom(28)
app.config["SESSION_TYPE"] = "filesystem"
df = pd.DataFrame()

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['GET', 'POST'])
def form():
    global df
    if request.method == 'POST':
        form_data = {
            'gender': request.form['gender'],
            'SeniorCitizen': request.form['SeniorCitizen'],
            'Partner': request.form['Partner'],
            'Dependents': request.form['Dependents'],
            'tenure': request.form['tenure'],
            'PhoneService': request.form['PhoneService'],
            'MultipleLines': request.form['MultipleLines'],
            'InternetService': request.form['InternetService'],
            'OnlineSecurity': request.form['OnlineSecurity'],
            'OnlineBackup': request.form['OnlineBackup'],
            'DeviceProtection': request.form['DeviceProtection'],
            'TechSupport': request.form['TechSupport'],
            'StreamingTV': request.form['StreamingTV'],
            'StreamingMovies': request.form['StreamingMovies'],
            'Contract': request.form['Contract'],
            'PaperlessBilling': request.form['PaperlessBilling'],
            'PaymentMethod': request.form['PaymentMethod'],
            'MonthlyCharges': request.form['MonthlyCharges'],
            'TotalCharges': request.form['TotalCharges']
        }
        df_telco_transformed = transform(form_data)
        churn = "Yes" if predict_churn(df_telco_transformed) else "No"
        df = pd.DataFrame(form_data, index=[0])
        df.insert(0, "Churn", churn)


        return redirect("/result")
    else:
        return render_template('form.html')


@app.route('/result', methods=['GET','POST'])
def result():
    df.insert(0, "Sr.No", list(range(1, len(df) + 1)))
    return render_template("result.html", column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)

@app.route('/processfile', methods=['GET','POST'])
def process_file():
    global df
    
    f = request.files['file']

    if not str(f.filename).endswith(".csv"):
        return "<h1>Invalid file</h1>"
    
    f.save(f.filename)  
    df = pd.read_csv(f.filename)
    df.dropna(inplace=True)
 
    ans = []

    for i in df.iterrows():
        try:
            churn = "Yes" if predict_churn(transform(i[1].to_dict())) else "No"
        except Exception as e:
            print("Info: ", e)
            df.drop(i[0], axis=0, inplace=True)
            continue
        ans.append(churn)

    if "Churn" in df:
        df = df.drop(["Churn"], axis=1)
    df.insert(0, "Churn", ans)
    return "Processed"

@app.route('/downloadfile', methods=['GET'])
def download_file():
    df['SeniorCitizen'] = df['SeniorCitizen'].map({1:'Yes', 0:'No','Yes':'Yes','No':'No'})
    resp = make_response(df.to_csv(index_label=False,index=None))
    resp.headers["Content-Disposition"] = "attachment; filename=result.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp

if __name__ == '__main__':
    app.run(debug=True)
