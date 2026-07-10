import pandas as pd
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "artifacts" / "model_data.joblib"

# Load the model and its components
model_data = joblib.load(MODEL_PATH)
model = model_data['model']
features = model_data['features']
scaler = model_data['scaler']
cols_to_scale = model_data['cols_to_scale']


def prepare_df(age, income, loan_amount, loan_to_income,loan_tenure_months, avg_dpd_per_delinquency, delinquency_ratio, credit_utilization_ratio, number_of_open_accounts, residence_type, loan_purpose, loan_type, credit_utilization_per_income):

    # Creating Dictionary in same format as model expects
    input_dict = {
        'age': age,
        'loan_tenure_months': loan_tenure_months,
        'number_of_open_accounts': number_of_open_accounts,
        'credit_utilization_ratio': credit_utilization_ratio,
        'loan_to_income': loan_to_income,
        'delinquency_ratio': delinquency_ratio,
        'avg_dpd_per_delinquency': avg_dpd_per_delinquency,
        'credit_utilization_per_income': credit_utilization_per_income,

        'residence_type_Owned': 1 if residence_type == 'Owned' else 0,
        'residence_type_Rented': 1 if residence_type == 'Rented' else 0,

        'loan_purpose_Education': 1 if loan_purpose == 'Education' else 0,
        'loan_purpose_Home': 1 if loan_purpose == 'Home' else 0,
        'loan_purpose_Personal': 1 if loan_purpose == 'Personal' else 0,

        'loan_type_Unsecured': 1 if loan_type == 'Unsecured' else 0,

        # Additional columns used during scaling (With dummy values)
        'number_of_dependants': 1,
        'years_at_current_address': 1,
        'sanction_amount': 1,
        'processing_fee': 1,
        'gst': 1,
        'net_disbursement': 1,
        'principal_outstanding': 1,
        'bank_balance_at_application': 1,
        'number_of_closed_accounts': 1,
        'enquiry_count': 1,
    }

    # Creating Dataframe
    df = pd.DataFrame([input_dict])

    # Scaling the data
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    # Reducing the Dataframe to only features(Which model expects)
    df = df[features]

    return df

# Function for rating
def get_rating(score):
    if 300 <= score < 500:
        return 'Poor'
    elif 500 <= score < 650:
        return 'Average'
    elif 650 <= score < 750:
        return 'Good'
    elif 750 <= score <= 900:
        return 'Excellent'
    else:
        return 'Undefined'

# Here base_score is the min value of our score and if we add scale length to base score we get 900 means the entire range 300-900
def calculate_credit_score(input_df, base_score=300, scale_length=600):

    # Predict probability of default
    default_probability = model.predict_proba(input_df)[0][1]
    non_default_probability = 1 - default_probability

    # Convert probability into a credit score (300–900)
    credit_score = int(base_score + non_default_probability * scale_length)

    # Assign credit rating based on the score
    rating = get_rating(credit_score)

    return default_probability, credit_score, rating

def predict(age, income, loan_amount, loan_to_income,loan_tenure_months, avg_dpd_per_delinquency, delinquency_ratio, credit_utilization_ratio, number_of_open_accounts, residence_type, loan_purpose, loan_type, credit_utilization_per_income):

    # This function does all the preprocessing and returns the dataframe
    input_df = prepare_df(age, income, loan_amount, loan_to_income,loan_tenure_months, avg_dpd_per_delinquency, delinquency_ratio, credit_utilization_ratio, number_of_open_accounts, residence_type, loan_purpose, loan_type, credit_utilization_per_income)

    probability, credit_score, rating = calculate_credit_score(input_df)

    return probability, credit_score, rating