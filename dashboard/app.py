# Application Streamlit du projet CrediTrust Scoring (Activité 4).
# Deux sections :
#   1. Analyse de données : graphiques et KPIs sur le fichier loan_data.csv.
#   2. Simulateur : formulaire connecté au modèle entraîné (train_model.py)
#      pour accorder ou refuser un prêt en temps réel, avec probabilité.

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="CrediTrust Scoring", page_icon="💳", layout="wide")


# --- Chargement des données et du modèle (mis en cache pour ne pas recharger à chaque clic) ---
@st.cache_data
def load_data():
    df = pd.read_csv("../data/loan_data.csv")
    return df.dropna(subset=["Loan_Status"]).drop(columns=["Loan_ID"]).reset_index(drop=True)


@st.cache_resource
def load_model_artifacts():
    model = joblib.load("models/model.joblib")
    scaler = joblib.load("models/scaler.joblib")
    prep = joblib.load("models/preprocessing.joblib")
    return model, scaler, prep


df = load_data()
model, scaler, prep = load_model_artifacts()

st.title("💳 CrediTrust Scoring")
st.caption("Outil d'aide à la décision pour l'octroi de prêts, basé sur le modèle de l'Activité 3.")

tab_analyse, tab_simulateur = st.tabs(["📊 Analyse de données", "🧮 Simulateur de demande"])


# ============================================================
# Onglet 1 : Analyse de données
# ============================================================
with tab_analyse:
    st.header("Analyse exploratoire du portefeuille de prêts")

    # --- KPIs essentiels ---
    n_dossiers = len(df)
    taux_refus = (df["Loan_Status"] == "N").mean() * 100
    revenu_median = df["ApplicantIncome"].median()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Dossiers analysés", n_dossiers)
    col2.metric("Taux de refus", f"{taux_refus:.1f} %")
    col3.metric("Revenu médian du demandeur", f"{revenu_median:,.0f}")
    col4.metric("Rappel du modèle (classe risque)", f"{prep['test_recall'] * 100:.1f} %")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Répartition des décisions")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x="Loan_Status", order=["Y", "N"], ax=ax)
        ax.set_xlabel("Loan_Status (Y = accordé, N = refusé)")
        ax.set_ylabel("Nombre de dossiers")
        st.pyplot(fig)

    with col_right:
        st.subheader("Taux de refus selon l'historique de crédit")
        credit_ct = pd.crosstab(df["Credit_History"], df["Loan_Status"], normalize="index") * 100
        st.dataframe(credit_ct.round(1))


# ============================================================
# Onglet 2 : Simulateur
# ============================================================
with tab_simulateur:
    st.header("Simuler une nouvelle demande de prêt")
    st.write("Remplis le formulaire ci-dessous pour obtenir une décision instantanée du modèle.")

    with st.form("loan_form"):
        c1, c2, c3 = st.columns(3)

        with c1:
            gender = st.selectbox("Genre", ["Male", "Female"])
            married = st.selectbox("Marié(e)", ["Yes", "No"])
            dependents = st.selectbox("Nombre de personnes à charge", ["0", "1", "2", "3+"])
            education = st.selectbox("Niveau d'études", ["Graduate", "Not Graduate"])

        with c2:
            self_employed = st.selectbox("Indépendant", ["Yes", "No"])
            property_area = st.selectbox("Zone géographique", ["Urban", "Semiurban", "Rural"])
            credit_history = st.selectbox(
                "A déjà bien remboursé un crédit par le passé ?", ["Oui", "Non"]
            )
            loan_amount_term = st.selectbox(
                "Durée du prêt (mois)", [360.0, 180.0, 480.0, 300.0, 240.0, 120.0, 84.0, 60.0, 36.0, 12.0, 6.0]
            )

        with c3:
            applicant_income = st.number_input("Revenu du demandeur", min_value=0, value=5000, step=100)
            coapplicant_income = st.number_input("Revenu du co-demandeur", min_value=0, value=0, step=100)
            loan_amount = st.number_input("Montant du prêt demandé (en milliers)", min_value=1, value=150, step=10)

        submitted = st.form_submit_button("Évaluer la demande")

    if submitted:
        # Construire une ligne avec les mêmes colonnes que celles utilisées à l'entraînement
        new_request = pd.DataFrame([{
            "Gender": gender,
            "Married": married,
            "Dependents": dependents,
            "Education": education,
            "Self_Employed": self_employed,
            "ApplicantIncome": applicant_income,
            "CoapplicantIncome": coapplicant_income,
            "LoanAmount": loan_amount,
            "Loan_Amount_Term": loan_amount_term,
            "Credit_History": 1.0 if credit_history == "Oui" else 0.0,
            "Property_Area": property_area,
        }])

        # --- Même prétraitement que l'entraînement (nb_03 / train_model.py) ---
        # 1) Encodage des variables catégorielles
        new_encoded = pd.get_dummies(
            new_request, columns=prep["categorical_cols"]
        )
        # 2) Alignement sur les colonnes vues à l'entraînement (les catégories absentes -> 0)
        new_encoded = new_encoded.reindex(columns=prep["encoded_columns"], fill_value=0)
        # 3) Standardisation des variables numériques avec le scaler entraîné
        new_scaled = new_encoded.copy()
        new_scaled[prep["numeric_cols"]] = scaler.transform(new_encoded[prep["numeric_cols"]])

        prediction = model.predict(new_scaled)[0]
        proba_risque = model.predict_proba(new_scaled)[0][1]

        st.divider()
        if prediction == 1:
            st.error(f"❌ Demande jugée **risquée** — probabilité de risque : {proba_risque * 100:.1f} %")
        else:
            st.success(f"✅ Demande jugée **sûre** — probabilité de risque : {proba_risque * 100:.1f} %")

        st.caption(
            "Rappel : ce modèle reproduit les critères d'une décision historique "
            "(accordé/refusé), pas un vrai indicateur de défaut de paiement constaté."
        )
