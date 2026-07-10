import streamlit as st
from prediction_helper import predict

st.title("Credit Risk Assessment System")
st.caption(
    "Default probability prediction and credit scoring using Logistic Regression."
)

# Creating 4 rows
row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

with row1[0]:
    age = st.number_input(
        "Age",
        min_value=28,
        max_value=100,
        step=1
    )

with row1[1]:
    income = st.number_input(
        "Income (₹)",
        min_value=0,
        value=1200000,
        format="%d"
    )

with row1[2]:
    loan_amount = st.number_input(
        "Loan Amount (₹)",
        min_value=0,
        value=2560000,
        format="%d"
    )

# Calculate Loan-to-Income Ratio
loan_to_income = loan_amount / income if income > 0 else 0

with row2[0]:
    st.text("Loan to Income Ratio:")
    st.text(f"{loan_to_income:.2f}")

with row2[1]:
    loan_tenure_months = st.number_input(
        "Loan Tenure (Months)",
        min_value=0,
        value=36
    )

with row2[2]:
    avg_dpd_per_delinquency = st.number_input(
        "Average DPD",
        min_value=0,
        value=20
    )

with row3[0]:
    delinquency_ratio = st.number_input(
        "Delinquency Ratio",
        min_value=0,
        max_value=100,
        value=30
    )

with row3[1]:
    credit_utilization_ratio = st.number_input(
        "Credit Utilization Ratio",
        min_value=0,
        max_value=100,
        value=30
    )

with row3[2]:
    number_of_open_accounts = st.number_input(
        "Open Loan Accounts",
        min_value=1,
        max_value=4,
        value=2
    )

with row4[0]:
    residence_type = st.selectbox(
        "Residence Type",
        options=["Owned", "Mortgage", "Rented"]
    )

with row4[1]:
    loan_purpose = st.selectbox(
        "Loan Purpose",
        options=["Education", "Home", "Personal", "Auto"]
    )

with row4[2]:
    loan_type = st.selectbox(
        "Loan Type",
        options=["Unsecured", "Secured"]
    )

# Calculate credit_utilization_per_income
credit_utilization_per_income = credit_utilization_ratio/loan_to_income

if st.button("Calculate Risk", type="primary"):

    probability, credit_score, rating = predict(
        age,
        income,
        loan_amount,
        loan_to_income,
        loan_tenure_months,
        avg_dpd_per_delinquency,
        delinquency_ratio,
        credit_utilization_ratio,
        number_of_open_accounts,
        residence_type,
        loan_purpose,
        loan_type,
        credit_utilization_per_income
    )

    with st.container(border=True):

        col1, col2, col3 = st.columns(3)

        col1.metric("Default Probability", f"{probability:.2%}")
        col2.metric("Credit Score", credit_score)
        col3.metric("Rating", rating)

        if probability <= 0.25:
            st.success("🟢 Low Risk Borrower")
        elif probability <= 0.6667:
            st.warning("🟡 Moderate Risk Borrower")
        else:
            st.error("🔴 High Risk Borrower")

st.divider()

with st.expander("Frequently Asked Questions"):

    st.markdown("#### What does default mean?")
    st.write(
        "A default occurs when a borrower fails to repay a loan according to the agreed terms. "
        "In this application, the model estimates the likelihood of a borrower defaulting."
    )

    st.markdown("#### What is Default Probability?")
    st.write(
        "Default Probability represents the estimated chance that a borrower will default on the loan. "
        "A lower probability indicates lower credit risk."
    )

    st.markdown("#### How is the Credit Score calculated?")
    st.write(
        "The credit score is derived from the predicted probability of default. "
        "Borrowers with a lower default probability receive a higher credit score on a scale of 300–900."
    )

    st.markdown("#### Does a high credit score guarantee loan approval?")
    st.write(
        "No. This application provides an estimate of credit risk. "
        "Actual lending decisions also consider factors such as employment, income verification, "
        "credit history, and institution-specific policies."
    )

    st.markdown("#### Which machine learning model powers this application?")
    st.write(
        "This application uses a Logistic Regression classifier trained on historical borrower data "
        "to estimate default probability and assess credit risk."
    )

st.write("---")

st.components.v1.html("""
<div style="
    text-align: center;
    font-size: 14px;
    color: #94a3b8;
    padding: 10px;
">
    👨‍💻 <b>Ansh Panchal</b> | AIML Student<br>
    📊 Passionate about Data Science & ML Engineering<br><br>

    🔗 Connect with me:<br>
    <a href="https://www.linkedin.com/in/4nshh/" target="_blank" style="color:#22c55e;">LinkedIn</a> |
    <a href="https://github.com/4nshhh" target="_blank" style="color:#22c55e;">GitHub</a>
</div>
""", height=150)