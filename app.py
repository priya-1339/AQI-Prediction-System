import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="EOGB-AQI Predictor", page_icon="🌿", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

/* ===== Full App Background — Light Green ===== */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stBottom"],
section[data-testid="stSidebar"],
.main, .block-container {
    background-color: #ecfdf5 !important;
}

/* ===== Base Font & Body Text — Dark Green ===== */
html, body, [class*="css"], p, span, div {
    font-family: 'Inter', sans-serif;
    color: #14532d;
}

/* ===== Headings — Dark Green ===== */
h1, h2, h3, h4, h5, h6,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5 {
    color: #14532d !important;
    font-weight: 700;
}

/* ===== Subtitle / paragraph text ===== */
[data-testid="stMarkdownContainer"] p {
    color: #166534 !important;
}

/* ===== Horizontal rule ===== */
hr {
    border-color: #bbf7d0;
}

/* ===== Buttons ===== */
div.stButton > button {
    background-color: #16a34a !important;
    color: white !important;
    border: none;
    border-radius: 8px;
    font-weight: 600;
}

div.stButton > button:hover {
    background-color: #15803d !important;
}

/* ===== Section Headers ===== */
.sec-head {
    background-color: #166534;
    color: white !important;
    padding: 8px 16px;
    border-radius: 8px;
    font-weight: 600;
    margin-bottom: 8px;
}

/* ===== Number Input Labels ===== */
div[data-testid="stNumberInput"] label,
div[data-testid="stNumberInput"] label p {
    color: #15803d !important;
    font-weight: 600;
}

/* ===== Number Input Boxes ===== */
div[data-testid="stNumberInput"] input {
    background-color: #f0fdf4 !important;
    color: #14532d !important;
    border: 1px solid #86efac !important;
    border-radius: 6px;
}

div[data-testid="stNumberInput"] input:focus {
    border-color: #16a34a !important;
    box-shadow: 0 0 0 2px #bbf7d0 !important;
}

/* ===== Checkbox — Enable text in Green ===== */
div[data-testid="stCheckbox"] label,
div[data-testid="stCheckbox"] label p,
div[data-testid="stCheckbox"] span {
    color: #16a34a !important;
    font-weight: 600 !important;
}

div[data-testid="stCheckbox"] input[type="checkbox"] {
    accent-color: #16a34a;
}

/* ===== Expander ===== */
div[data-testid="stExpander"] > details > summary,
div[data-testid="stExpander"] summary {
    background-color: #16a34a !important;
    color: white !important;
    padding: 10px;
    border-radius: 8px;
    font-weight: 600;
}

div[data-testid="stExpander"] > details {
    background-color: #f0fdf4 !important;
    border: 1px solid #bbf7d0;
    border-radius: 8px;
}

/* ===== AQI Table ===== */
.aqi-table {
    width: 100%;
    border-collapse: collapse;
}

.aqi-table th {
    background-color: #166534;
    color: white;
    padding: 8px 12px;
}

.aqi-table td {
    background: #dcfce7;
    color: #14532d;
    padding: 7px 12px;
}

.aqi-table tr:nth-child(even) td {
    background: #bbf7d0;
}

/* ===== AQI Result Card ===== */
.aqi-card {
    text-align: center;
    padding: 20px;
    border-radius: 12px;
    margin: 16px 0;
}

.aqi-value {
    font-size: 3rem;
    font-weight: 700;
    line-height: 1.1;
}

.aqi-label {
    font-size: 1.4rem;
    font-weight: 600;
    margin-top: 6px;
}

/* ===== Health Tip ===== */
.health-tip {
    background: #dcfce7;
    border-left: 5px solid #16a34a;
    color: #14532d !important;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin-top: 12px;
}

/* ===== Footer ===== */
.footer {
    color: #166534 !important;
    text-align: center;
    margin-top: 24px;
    font-size: 0.85rem;
}

/* ===== Remove stray white backgrounds ===== */
div[data-testid="stForm"],
div[data-testid="stVerticalBlock"],
div[data-testid="column"],
div[data-testid="stHorizontalBlock"] {
    background: transparent !important;
}

/* ===== Alert / error box ===== */
div[data-testid="stAlert"] {
    background-color: #f0fdf4 !important;
    color: #14532d !important;
    border-color: #86efac !important;
}
</style>
""", unsafe_allow_html=True)

# ── Load model ──
@st.cache_resource
def load_model():
    return pickle.load(open("aqi_model.pkl", "rb"))

try:
    model = load_model()
except FileNotFoundError:
    st.error("❌ aqi_model.pkl not found. Place it in the same folder as app.py")
    st.stop()

# ── AQI Category ──
def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good",        "#16a34a", "🟢", "Air quality is satisfactory. Enjoy outdoor activities freely."
    elif aqi <= 100:
        return "Satisfactory","#65a30d",  "🟡", "Minor discomfort for sensitive individuals. Most people can go outside normally."
    elif aqi <= 200:
        return "Moderate",    "#d97706",  "🟠", "People with respiratory issues may face discomfort. Limit prolonged outdoor exertion."
    elif aqi <= 300:
        return "Poor",        "#dc2626",  "🔴", "Everyone may experience health effects. Avoid outdoor activities, especially children and elderly."
    elif aqi <= 400:
        return "Very Poor",   "#7c3aed",  "🟣", "Health alert! Serious effects for everyone. Stay indoors and use air purifiers."
    else:
        return "Severe",      "#7f1d1d",  "⚫", "Emergency conditions. Avoid all outdoor activities. Wear N95 mask if going out."

# ── Default mean values ──
DEFAULTS = {
    'PT08.S1(CO)':   1099.8,
    'C6H6(GT)':      10.08,
    'PT08.S2(NMHC)': 939.2,
    'PT08.S3(NOx)':  794.8,
    'PT08.S4(NO2)':  1457.0,
    'PT08.S5(O3)':   1022.9,
    'AH':            1.025,
}

# ── Header ──
st.markdown("## 🌿 EOGB-AQI Predictor")
st.markdown("##### Air Quality Index Prediction · CPCB Standards · Gradient Boosting Model")
st.markdown("---")

# ── AQI Range Table ──
with st.expander("📊 AQI Range Reference — Click to view", expanded=False):
    st.markdown("""
    <table class="aqi-table">
        <tr><th>AQI Range</th><th>Category</th><th>Health Impact</th></tr>
        <tr><td>0 – 50</td><td>🟢 Good</td><td>Minimal impact on health</td></tr>
        <tr><td>51 – 100</td><td>🟡 Satisfactory</td><td>Minor discomfort for sensitive people</td></tr>
        <tr><td>101 – 200</td><td>🟠 Moderate</td><td>Discomfort for people with respiratory issues</td></tr>
        <tr><td>201 – 300</td><td>🔴 Poor</td><td>Health effects for everyone on prolonged exposure</td></tr>
        <tr><td>301 – 400</td><td>🟣 Very Poor</td><td>Serious health effects, stay indoors</td></tr>
        <tr><td>401 – 500</td><td>⚫ Severe</td><td>Emergency conditions, avoid all outdoor activity</td></tr>
    </table>
    """, unsafe_allow_html=True)

st.markdown("")
st.markdown("### 🔬 Enter Pollutant Values")
st.markdown("Check the box to enable optional sensor fields. Unchecked fields use dataset mean values automatically.")
st.markdown("")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="sec-head">🌫️ Main Pollutants</div>', unsafe_allow_html=True)
    co   = st.number_input("CO(GT) — mg/m³",        value=2.15,  step=0.1)
    nox  = st.number_input("NOx(GT) — ppb",          value=246.9, step=1.0)
    no2  = st.number_input("NO2(GT) — µg/m³",        value=113.0, step=1.0)
    temp = st.number_input("Temperature (°C)",        value=18.3,  step=0.5)
    rh   = st.number_input("Relative Humidity (%)",   value=49.2,  step=1.0)

    st.markdown('<div class="sec-head">🔧 Optional Sensors</div>', unsafe_allow_html=True)

    use_s3 = st.checkbox("Enable PT08.S3 — NOx Sensor")
    nox_s  = st.number_input("PT08.S3(NOx) — sensor", value=794.8,  step=10.0, disabled=not use_s3)

    use_s4 = st.checkbox("Enable PT08.S4 — NO2 Sensor")
    no2_s  = st.number_input("PT08.S4(NO2) — sensor", value=1457.0, step=10.0, disabled=not use_s4)

    use_ah = st.checkbox("Enable Absolute Humidity")
    ah     = st.number_input("Absolute Humidity",      value=1.025,  step=0.01, disabled=not use_ah)

with col2:
    st.markdown('<div class="sec-head">🔧 Optional Sensors</div>', unsafe_allow_html=True)

    use_s1   = st.checkbox("Enable PT08.S1 — CO Sensor")
    co_s     = st.number_input("PT08.S1(CO) — sensor",    value=1099.8, step=10.0, disabled=not use_s1)

    use_c6h6 = st.checkbox("Enable C6H6 — Benzene")
    c6h6     = st.number_input("C6H6(GT) — µg/m³",        value=10.08,  step=0.1,  disabled=not use_c6h6)

    use_s2   = st.checkbox("Enable PT08.S2 — NMHC Sensor")
    nmhc     = st.number_input("PT08.S2(NMHC) — sensor",  value=939.2,  step=10.0, disabled=not use_s2)

    use_s5   = st.checkbox("Enable PT08.S5 — O3 Sensor")
    o3_s     = st.number_input("PT08.S5(O3) — sensor",    value=1022.9, step=10.0, disabled=not use_s5)

# ── Final values ──
final_co_s  = co_s  if use_s1   else DEFAULTS['PT08.S1(CO)']
final_c6h6  = c6h6  if use_c6h6 else DEFAULTS['C6H6(GT)']
final_nmhc  = nmhc  if use_s2   else DEFAULTS['PT08.S2(NMHC)']
final_nox_s = nox_s if use_s3   else DEFAULTS['PT08.S3(NOx)']
final_no2_s = no2_s if use_s4   else DEFAULTS['PT08.S4(NO2)']
final_o3_s  = o3_s  if use_s5   else DEFAULTS['PT08.S5(O3)']
final_ah    = ah     if use_ah   else DEFAULTS['AH']

st.markdown("")

# ── Predict ──
if st.button("🔍 Predict AQI", type="primary", use_container_width=True):

    X_input = np.array([[
        co, final_co_s, final_c6h6, final_nmhc,
        nox, final_nox_s, no2, final_no2_s,
        final_o3_s, temp, rh, final_ah
    ]])

    predicted_aqi = model.predict(X_input)[0]
    predicted_aqi = max(0, round(predicted_aqi, 1))
    category, color, emoji, health_tip = get_aqi_category(predicted_aqi)

    st.markdown(f"""
    <div class="aqi-card" style="background:{color}15; border:2px solid {color}55;">
        <div class="aqi-value" style="color:{color};">{predicted_aqi}</div>
        <div class="aqi-label" style="color:{color};">{emoji} {category}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="health-tip" style="border-color:{color};">
        <strong>Health Advisory:</strong> {health_tip}
    </div>
    """, unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div class="footer">
    EOGB-AQI Framework · Gradient Boosting Model · CPCB Standards · Final Year Project
</div>
""", unsafe_allow_html=True)
