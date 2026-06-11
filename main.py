import streamlit as st
from prediction_helper import predict

st.set_page_config(
    page_title="Insurance Premium Prediction",
    layout="wide"
)

# ===================== CSS =====================
st.markdown("""
<style>
.main .block-container { padding-top: 0 !important; }
.main { background-color: #f0f4f8; }
[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e5e7eb; }

[data-testid="stSidebar"] label {
    color: #1e293b !important;
    font-weight: 600 !important;
}

.top-header {
    background-color: #2563eb;
    padding: 14px 28px;
    display: flex;
    justify-content: space-between;
    border-radius: 12px;
    margin-bottom: 20px;
    color: white;
    font-weight: 700;
}

.result-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    margin-top: 20px;
}

.premium-value {
    font-size: 40px;
    font-weight: 700;
    color: #16a34a;
}
</style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================
st.markdown("""
<div class="top-header">
    <div>🛡️ Insurance Premium Prediction</div>
    <div>AI Model</div>
</div>
""", unsafe_allow_html=True)

# ===================== SIDEBAR =====================
with st.sidebar:

    st.markdown("### Enter Details")

    age = st.slider("Age", 18, 100, 28)
    gender = st.selectbox("Gender", ["Male", "Female"])
    region = st.selectbox("Region", ["Northwest", "Southeast", "Northeast", "Southwest"])
    bmi_category = st.selectbox("BMI Category", ["Normal", "Obesity", "Overweight", "Underweight"])

    smoking_status = st.selectbox("Smoking Status", ["No Smoking", "Occasional", "Regular"])

    medical_history = st.selectbox(
        "Medical History",
        [
            "No Disease",
            "Diabetes",
            "High blood pressure",
            "Diabetes & High blood pressure",
            "Thyroid",
            "Heart disease",
            "High blood pressure & Heart disease",
            "Diabetes & Thyroid",
            "Diabetes & Heart disease"
        ]
    )

    income = st.number_input("Annual Income", 0, 10000000, 55000)
    insurance_plan = st.selectbox("Insurance Plan", ["Bronze", "Silver", "Gold"])

    with st.expander("More Details"):
        dependants = st.number_input("Dependants", 0, 20, 0)
        employment = st.selectbox("Employment Status", ["Salaried", "Self-Employed", "Freelancer"])
        marital = st.selectbox("Marital Status", ["Unmarried", "Married"])
        genetic_risk = st.number_input("Genetical Risk", 0, 5, 1)

    predict_btn = st.button("Predict Premium")

# ===================== INPUT =====================
input_dict = {
    "Age": age,
    "Number of Dependants": dependants,
    "Income in Lakhs": income,
    "Genetical Risk": genetic_risk,
    "Insurance Plan": insurance_plan,
    "Employment Status": employment,
    "Gender": gender,
    "Marital Status": marital,
    "BMI Category": bmi_category,
    "Smoking Status": smoking_status,
    "Region": region,
    "Medical History": medical_history
}

# ===================== MAIN =====================
if predict_btn:
    prediction = predict(input_dict)

    if hasattr(prediction, "__len__"):
        prediction = prediction[0]

    st.markdown(f"""
    <div class="result-card">
        <div>Estimated Premium</div>
        <div class="premium-value">${prediction:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
