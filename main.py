import streamlit as st
from prediction_helper import predict

st.set_page_config(
    page_title="Insurance Premium Prediction",
    layout="wide"
)

# ===================== CSS =====================
st.markdown("""
<style>

/* Global */
.main .block-container { padding-top: 0 !important; }
.main { background-color: #f0f4f8; }
[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e5e7eb; }

/* Fix sidebar label visibility */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSlider label p,
[data-testid="stSidebar"] .stSelectbox label p,
[data-testid="stSidebar"] .stNumberInput label p {
    color: #1e293b !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

/* Wider slider track */
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {
    padding-left: 0 !important;
    padding-right: 0 !important;
}
[data-testid="stSidebar"] .stSlider {
    width: 100% !important;
}

/* Top header */
.top-header {
    background-color: #2563eb;
    padding: 14px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
    border-radius: 12px;
}
.top-header-title {
    font-size: 20px;
    font-weight: 700;
    color: white;
}
.top-header-about {
    font-size: 13px;
    color: rgba(255,255,255,0.85);
}

/* Hero */
.hero-title {
    font-size: 75px;
    font-weight: 700;
    color: white;
    line-height: 1.2;
    margin-bottom: 8px;
}
.hero-subtitle {
    font-size: 25px;
    color: #64748b;
    line-height: 1.6;
    margin-bottom: 0;
}

/* Result card */
.result-card {
    background-color: white;
    padding: 24px 28px;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    margin-top: 20px;
    display: flex;
    align-items: center;
    gap: 20px;
}
.result-icon-wrap {
    width: 60px; height: 60px;
    background-color: #dcfce7;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px; flex-shrink: 0;
}
.result-label { font-size: 13px; color: #64748b; margin-bottom: 4px; }
.premium-value { font-size: 42px; font-weight: 700; color: #16a34a; line-height: 1; margin-bottom: 8px; }
.result-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background-color: #dcfce7; color: #15803d;
    padding: 4px 12px; border-radius: 999px;
    font-size: 13px; font-weight: 500;
}

/* Summary card */
.summary-card {
    background-color: white;
    padding: 22px 26px;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    margin-top: 16px;
}
.summary-title {
    font-size: 17px; font-weight: 700; color: #0f172a; margin-bottom: 16px;
}
.summary-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
}
.s-item {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 10px 12px;
    background-color: #f8fafc;
    border-radius: 10px;
    border: 1px solid #f1f5f9;
}
.s-icon {
    width: 34px; height: 34px;
    border-radius: 8px; background-color: #eff6ff;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
}
.s-label { font-size: 11px; color: #94a3b8; margin-bottom: 2px; }
.s-val { font-size: 14px; font-weight: 600; color: #1e293b; }

/* Note box */
.note-box {
    display: flex; align-items: flex-start; gap: 8px;
    background-color: #eff6ff; border: 1px solid #bfdbfe;
    border-radius: 10px; padding: 12px 16px;
    margin-top: 16px; font-size: 13px; color: #1e40af;
}

/* Blue predict button */
[data-testid="stSidebar"] .stButton > button {
    background-color: #2563eb !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 12px !important;
    height: auto !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #1d4ed8 !important;
}

</style>
""", unsafe_allow_html=True)

# ===================== OPTIONS =====================

categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer'],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High blood pressure',
        'Diabetes & High blood pressure', 'Thyroid', 'Heart disease',
        'High blood pressure & Heart disease', 'Diabetes & Thyroid',
        'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}

# ===================== SIDEBAR =====================

with st.sidebar:

    st.markdown(
        '<div style="display:flex;align-items:center;gap:10px;padding:8px 0 18px 0;">'
        '<div style="background:#2563eb;border-radius:8px;width:32px;height:32px;'
        'display:flex;align-items:center;justify-content:center;font-size:17px;">🛡️</div>'
        '<span style="font-size:16px;font-weight:700;color:#0f172a;">Premium Prediction</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p style="font-size:12px;font-weight:600;color:#64748b;text-transform:uppercase;'
        'letter-spacing:0.05em;margin-bottom:12px;">👤 Enter Customer Details</p>',
        unsafe_allow_html=True
    )

    age = st.slider("Age", min_value=18, max_value=100, value=28)
    gender = st.selectbox("Gender", categorical_options["Gender"])
    region = st.selectbox("Region", categorical_options["Region"])
    bmi_category = st.selectbox("BMI Category", categorical_options["BMI Category"])

    smoking_display = st.selectbox("Smoking Status", ['Non-smoker', 'Occasional', 'Regular'])
    smoking_map = {'Non-smoker': 'No Smoking', 'Occasional': 'Occasional', 'Regular': 'Regular'}
    smoking_status_model = smoking_map[smoking_display]

    medical_display = st.selectbox("Medical History", [
        'No', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
        'Thyroid', 'Heart disease', 'High blood pressure & Heart disease',
        'Diabetes & Thyroid', 'Diabetes & Heart disease'
    ])
    medical_history_model = 'No Disease' if medical_display == 'No' else medical_display

    # exercise_frequency = st.slider("Exercise Frequency (days/week)", min_value=0, max_value=7, value=3)
    income = st.number_input("Annual Income (USD)", min_value=0, max_value=10000000, value=55000, step=1000)
    income_lakhs = round(income / 100000 * 83, 2)
    insurance_plan = st.selectbox("Insurance Plan", categorical_options["Insurance Plan"])
    number_of_dependants = st.number_input("Dependants", min_value=0, max_value=20, value=0)
    employment_status = st.selectbox("Employment Status", categorical_options["Employment Status"])
    marital_status = st.selectbox("Marital Status", categorical_options["Marital Status"])
    genetical_risk = st.number_input("Genetical Risk (0-5)", min_value=0, max_value=5, value=1)

    predict_btn = st.button("📊 Predict Premium", use_container_width=True)

# ===================== INPUT DICT =====================

input_dict = {
    'Age': age,
    'Number of Dependants': number_of_dependants,
    'Income in Lakhs': income_lakhs,
    'Genetical Risk': genetical_risk,
    'Insurance Plan': insurance_plan,
    'Employment Status': employment_status,
    'Gender': gender,
    'Marital Status': marital_status,
    'BMI Category': bmi_category,
    'Smoking Status': smoking_status_model,
    'Region': region,
    'Medical History': medical_history_model
}

# ===================== HEADER =====================

st.markdown(
    '<div class="top-header">'
    '<div class="top-header-title">🛡️ Insurance Premium Prediction</div>'
    '<div class="top-header-about">ℹ️ About</div>'
    '</div>',
    unsafe_allow_html=True
)

# ===================== HERO =====================

hero_left, hero_right = st.columns([2, 1])

with hero_left:
    st.markdown(
        '<div class="hero-title">Predict Your Insurance Premium</div>'
        '<div class="hero-subtitle">Fill in your details in the sidebar and click on '
        "'Predict Premium' to estimate your expected insurance premium.</div>",
        unsafe_allow_html=True
    )

with hero_right:
    try:
        st.image("ml_project_image.png", use_container_width=True)
    except:
        pass

# ===================== PREDICTION =====================

if predict_btn:

    prediction = predict(input_dict)
    if hasattr(prediction, "__len__"):
        prediction = prediction[0]

    # --- Result card (f-string, no .format needed) ---
    st.markdown(
        f'<div class="result-card">'
        f'<div class="result-icon-wrap">✅</div>'
        f'<div>'
        f'<div class="result-label">Estimated Premium</div>'
        f'<div class="premium-value">${prediction:,.2f}</div>'
        f'<div class="result-badge">✓ This is the estimated premium for your provided details.</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # --- Input summary (build HTML as a variable to avoid .format() vs f-string conflict) ---
    summary_html = (
        '<div class="summary-card">'
        '<div class="summary-title">Input Summary</div>'
        '<div class="summary-grid">'

        '<div class="s-item"><div class="s-icon">👤</div>'
        f'<div><div class="s-label">Age</div><div class="s-val">{age}</div></div></div>'

        '<div class="s-item"><div class="s-icon">🚻</div>'
        f'<div><div class="s-label">Gender</div><div class="s-val">{gender}</div></div></div>'

        '<div class="s-item"><div class="s-icon">📍</div>'
        f'<div><div class="s-label">Region</div><div class="s-val">{region}</div></div></div>'

        '<div class="s-item"><div class="s-icon">⚖️</div>'
        f'<div><div class="s-label">BMI Category</div><div class="s-val">{bmi_category}</div></div></div>'

        '<div class="s-item"><div class="s-icon">🚬</div>'
        f'<div><div class="s-label">Smoking Status</div><div class="s-val">{smoking_display}</div></div></div>'

        '<div class="s-item"><div class="s-icon">🏥</div>'
        f'<div><div class="s-label">Medical History</div><div class="s-val">{medical_display}</div></div></div>'

        '<div class="s-item"><div class="s-icon">💰</div>'
        f'<div><div class="s-label">Annual Income</div><div class="s-val">${income:,}</div></div></div>'

        '<div class="s-item"><div class="s-icon">📋</div>'
        f'<div><div class="s-label">Insurance Plan</div><div class="s-val">{insurance_plan}</div></div></div>'


        '</div></div>'
    )
    st.markdown(summary_html, unsafe_allow_html=True)

    st.markdown(
        '<div class="note-box">ℹ️ <span><b>Note:</b> This prediction is based on machine learning '
        'models and should not be considered as actual insurance pricing.</span></div>',
        unsafe_allow_html=True
    )
