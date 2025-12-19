import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="Harun Fathurrozaq | Portfolio",
    page_icon="📊",
    layout="wide"
)

# =====================
# MODERN LIGHT CSS + ANIMATION
# =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap');

html, body {
    font-family: 'Inter', sans-serif;
    background-color: #F8FAFC;
}

h1, h2, h3 {
    color: #0F172A;
}

.hero {
    background: linear-gradient(120deg, #E0F2FE, #F8FAFC);
    padding: 70px;
    border-radius: 28px;
    animation: fadeSlide 1.2s ease;
}

.card {
    background: white;
    padding: 28px;
    border-radius: 22px;
    box-shadow: 0px 15px 35px rgba(15,23,42,0.08);
    transition: all 0.35s ease;
    animation: fadeUp 1s ease;
}

.card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0px 25px 55px rgba(56,189,248,0.35);
}

img {
    border-radius: 22px;
    animation: zoomIn 1.2s ease;
}

.sidebar .sidebar-content {
    background-color: #FFFFFF;
}

@keyframes fadeUp {
    from {opacity: 0; transform: translateY(30px);}
    to {opacity: 1; transform: translateY(0);}
}

@keyframes fadeSlide {
    from {opacity: 0; transform: translateX(-40px);}
    to {opacity: 1; transform: translateX(0);}
}

@keyframes zoomIn {
    from {opacity: 0; transform: scale(0.9);}
    to {opacity: 1; transform: scale(1);}
}
</style>
""", unsafe_allow_html=True)

# =====================
# SIDEBAR NAVIGATION
# =====================
st.sidebar.markdown("## 📌 Portfolio Saya")
menu = st.sidebar.radio(
    "",
    ["🏠 Home", "👤 About Me", "📂 Projects", "🤖 Predict ML", "📞 Contact"]
)

st.sidebar.markdown("---")
st.sidebar.caption("© Harun Fathurrozaq • Data Analyst")

# =====================
# HOME
# =====================
if menu == "🏠 Home":
    st.markdown("""
    <div class="hero">
        <h1>Hi, I'm Harun 👋</h1>
        <h2>Data Analyst & Machine Learning Enthusiast</h2>
        <p>
        I turn raw data into insights, dashboards,
        and predictive models to help business decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    c1.markdown("<div class='card'><h3>📊 Data Analysis</h3><p>EDA & business insight</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='card'><h3>📈 Visualization</h3><p>Interactive dashboards</p></div>", unsafe_allow_html=True)
    c3.markdown("<div class='card'><h3>🤖 Machine Learning</h3><p>Prediction & evaluation</p></div>", unsafe_allow_html=True)

# =====================
# ABOUT ME (USING YOUR PHOTO)
# =====================
elif menu == "👤 About Me":
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("assets/about_me.jpg", use_container_width=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h2>Harun Fathurrozaq</h2>
        <p><b>📍 Asal:</b> Yogyakarta</p>
        <p><b>💼 Role:</b> Data Analyst</p>
        <p>
        Saya adalah Data Analyst yang fokus pada
        pengolahan data, visualisasi interaktif,
        dan machine learning untuk mendukung
        pengambilan keputusan bisnis.
        </p>
        </div>
        """, unsafe_allow_html=True)

# =====================
# PROJECTS
# =====================
elif menu == "📂 Projects":
    st.markdown("# 📂 Bank Customer Churn Project")

    df = pd.read_csv("data/Bank Customer Churn Prediction.csv")

    country = st.multiselect(
        "🌍 Filter Country",
        df["country"].unique(),
        default=df["country"].unique()
    )
    df = df[df["country"].isin(country)]

    c1, c2, c3 = st.columns(3)

    c1.markdown(f"<div class='card'><h3>👥 Customer</h3><h1>{len(df)}</h1></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='card'><h3>📉 Churn Rate</h3><h1>{round(df['churn'].mean()*100,2)}%</h1></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='card'><h3>💰 Avg Balance</h3><h1>{round(df['balance'].mean(),2)}</h1></div>", unsafe_allow_html=True)

    fig = px.bar(
        df.groupby("country")["churn"].mean().reset_index(),
        x="country",
        y="churn",
        color="country"
    )
    st.plotly_chart(fig, use_container_width=True)

# =====================
# PREDICT ML
# =====================
elif menu == "🤖 Predict ML":
    st.markdown("# 🤖 Customer Churn Prediction")

    df = pd.read_csv("data/Bank Customer Churn Prediction.csv")
    X = df[["credit_score", "age", "balance", "active_member"]]
    y = df["churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))

    st.markdown(f"<div class='card'><h3>🎯 Accuracy</h3><h1>{round(acc*100,2)}%</h1></div>", unsafe_allow_html=True)

    credit = st.slider("Credit Score", 300, 900, 650)
    age = st.slider("Age", 18, 80, 35)
    balance = st.number_input("Balance", 0.0, 300000.0, 50000.0)
    active = st.selectbox("Active Member", [0, 1])

    if st.button("🚀 Predict"):
        prob = model.predict_proba([[credit, age, balance, active]])[0][1]
        if prob > 0.5:
            st.error(f"⚠️ High Churn Risk ({round(prob*100,2)}%)")
        else:
            st.success(f"✅ Low Churn Risk ({round((1-prob)*100,2)}%)")

# =====================
# CONTACT
# =====================
elif menu == "📞 Contact":
    st.markdown("""
    <div class="card">
    <h3>📧 Email</h3>
    <p>harunfathurrozaq01@gmail.com</p>

    <h3>💻 GitHub</h3>
    <p><a href="https://github.com/harunfrzq" target="_blank">github.com/harunfrzq</a></p>

    <h3>🔗 LinkedIn</h3>
    <p><a href="https://www.linkedin.com/in/harun-fathurrozaq-88b8821b2" target="_blank">
    linkedin.com/in/harun-fathurrozaq
    </a></p>
    </div>
    """, unsafe_allow_html=True)
