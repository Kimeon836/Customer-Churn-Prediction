import pickle
import pandas as pd

def transform(data: dict) -> pd.DataFrame:
    features = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
        'PhoneService', 'PaperlessBilling', 'MonthlyCharges', 'TotalCharges',
        'MultipleLines_No', 'MultipleLines_No phone service',
        'MultipleLines_Yes', 'InternetService_DSL',
        'InternetService_Fiber optic', 'InternetService_No',
        'OnlineSecurity_No', 'OnlineSecurity_No internet service',
        'OnlineSecurity_Yes', 'OnlineBackup_No',
        'OnlineBackup_No internet service', 'OnlineBackup_Yes',
        'DeviceProtection_No', 'DeviceProtection_No internet service',
        'DeviceProtection_Yes', 'TechSupport_No',
        'TechSupport_No internet service', 'TechSupport_Yes', 'StreamingTV_No',
        'StreamingTV_No internet service', 'StreamingTV_Yes',
        'StreamingMovies_No', 'StreamingMovies_No internet service',
        'StreamingMovies_Yes', 'Contract_Month-to-month', 'Contract_One year',
        'Contract_Two year', 'PaymentMethod_Bank transfer',
        'PaymentMethod_Credit card', 'PaymentMethod_Electronic check',
        'PaymentMethod_Mailed check']
    
    one_hot_encoding_columns = ['MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
                                'TechSupport', 'StreamingTV',  'StreamingMovies', 'Contract', 'PaymentMethod']
    telco = {}
    for k, v in data.items():
        if k not in features and k not in one_hot_encoding_columns: continue
        telco[k] = [v]

    df_telco = pd.DataFrame.from_dict(telco)

    df_telco_transformed = pd.get_dummies(df_telco, columns = one_hot_encoding_columns,)
    filtered = {}
    for k in features:
        if k in df_telco_transformed.columns:
            filtered[k] = df_telco_transformed[k]
        else:
            filtered[k] = [0]
    df_telco_transformed = pd.DataFrame(filtered)

    label_encoding_columns = ['gender', 'Partner', 'Dependents', 'PaperlessBilling', 'PhoneService', 'SeniorCitizen']

    for column in label_encoding_columns:
        if column == 'gender':
            df_telco_transformed[column] = df_telco_transformed[column].map({'Female': 1, 'Male': 0})
        elif column == 'SeniorCitizen':
            df_telco_transformed[column] = df_telco_transformed[column].map({'Yes': 1, 'No': 0, 0: 0, 1:1})
        else: 
            df_telco_transformed[column] = df_telco_transformed[column].map({'Yes': 1, 'No': 0})
    

    return df_telco_transformed

def predict_churn(df_telco: pd.DataFrame, filename='finalized_model.sav') -> bool:
    loaded_model = pickle.load(open(filename, 'rb'))
    
    output = loaded_model.predict(df_telco.values)[0]

    return output == 1

if __name__ == "__main__":
    test = {
    'gender': 'Male',
    'SeniorCitizen': '0',
    'Partner': 'No',
    'Dependents': 'No',
    'tenure': '2',
    'PhoneService': 'Yes',
    'MultipleLines': 'No',
    'InternetService': 'DSL',
    'OnlineSecurity': 'Yes',
    'OnlineBackup': 'No',
    'DeviceProtection': 'Yes',
    'TechSupport': 'No',
    'StreamingTV': 'No',
    'StreamingMovies': 'No',
    'Contract': 'Month-to-month',
    'PaperlessBilling': 'Yes',
    'PaymentMethod': 'Mailed check',
    'MonthlyCharges': '53.85',
    'TotalCharges': '108.15'
}
    df = transform(test)
