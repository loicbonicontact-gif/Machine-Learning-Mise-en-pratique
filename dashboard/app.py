# Application Streamlit du projet CrediTrust Scoring (Activité 4).
# Deux sections :
#   1. Analyse de données : graphiques interactifs et KPIs sur loan_data.csv.
#   2. Simulateur : formulaire connecté au modèle entraîné (train_model.py)
#      pour accorder ou refuser un prêt en temps réel, avec probabilité.

import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="CrediTrust Scoring", page_icon="💳", layout="wide")

COLOR_SUR = "#16A34A"   # vert : dossier sûr
COLOR_RISQUE = "#DC2626"  # rouge : dossier risqué
COLOR_PRIMARY = "#2563EB"  # bleu : couleur principale du thème


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


# ============================================================
# Barre latérale : présentation du projet
# ============================================================
with st.sidebar:
    st.markdown("## 💳 CrediTrust")
    st.caption("Scoring de risque crédit")
    st.divider()
    st.markdown(
        """
        **À propos**

        Cet outil aide à décider s'il faut accorder ou refuser une demande
        de prêt, à partir d'un modèle entraîné sur l'historique des
        décisions de CrediTrust.
        """
    )
    st.metric("Modèle utilisé", "Arbre de Décision")
    st.metric("Rappel sur la classe risque", f"{prep['test_recall'] * 100:.1f} %")
    st.caption(
        "Le rappel mesure la capacité du modèle à détecter les dossiers "
        "réellement risqués — la priorité métier pour CrediTrust."
    )
    st.divider()
    st.caption("Projet Machine Learning — Activité 4 (Dashboard Streamlit)")


st.title("💳 CrediTrust Scoring")
st.caption("Outil d'aide à la décision pour l'octroi de prêts, basé sur le modèle de l'Activité 3.")

tab_analyse, tab_simulateur = st.tabs(["📊 Analyse de données", "🧮 Simulateur de demande"])


# ============================================================
# Onglet 1 : Analyse de données
# ============================================================
with tab_analyse:
    st.subheader("Vue d'ensemble du portefeuille")

    n_dossiers = len(df)
    taux_refus = (df["Loan_Status"] == "N").mean() * 100
    revenu_median = df["ApplicantIncome"].median()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📁 Dossiers analysés", f"{n_dossiers:,}")
    col2.metric("🚫 Taux de refus", f"{taux_refus:.1f} %")
    col3.metric("💰 Revenu médian", f"{revenu_median:,.0f}")
    col4.metric("🎯 Rappel du modèle", f"{prep['test_recall'] * 100:.1f} %")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("**Répartition des décisions**")
        status_counts = (
            df["Loan_Status"]
            .map({"Y": "Accordé", "N": "Refusé"})
            .value_counts()
            .reindex(["Accordé", "Refusé"])
            .reset_index()
        )
        status_counts.columns = ["Décision", "Nombre de dossiers"]
        fig_status = px.pie(
            status_counts,
            names="Décision",
            values="Nombre de dossiers",
            hole=0.55,
            color="Décision",
            color_discrete_map={"Accordé": COLOR_SUR, "Refusé": COLOR_RISQUE},
        )
        fig_status.update_traces(textinfo="percent+label")
        fig_status.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_status, width="stretch")

    with col_right:
        st.markdown("**Taux de refus selon l'historique de crédit**")
        credit_ct = (
            pd.crosstab(df["Credit_History"], df["Loan_Status"], normalize="index")["N"] * 100
        ).reset_index()
        credit_ct.columns = ["Historique de crédit", "Taux de refus (%)"]
        credit_ct["Historique de crédit"] = credit_ct["Historique de crédit"].map(
            {1.0: "Bon historique (1)", 0.0: "Pas d'historique (0)"}
        )
        fig_credit = px.bar(
            credit_ct,
            x="Historique de crédit",
            y="Taux de refus (%)",
            color="Historique de crédit",
            color_discrete_sequence=[COLOR_RISQUE, COLOR_SUR],
            text_auto=".1f",
        )
        fig_credit.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_credit, width="stretch")

    st.caption(
        "`Credit_History` (avoir déjà bien remboursé un crédit) est le facteur de risque "
        "le plus déterminant, comme identifié dans l'Activité 3."
    )


# ============================================================
# Onglet 2 : Simulateur
# ============================================================
with tab_simulateur:
    st.subheader("Simuler une nouvelle demande de prêt")
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

        submitted = st.form_submit_button("Évaluer la demande", width="stretch")

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
        new_encoded = pd.get_dummies(new_request, columns=prep["categorical_cols"])
        # 2) Alignement sur les colonnes vues à l'entraînement (les catégories absentes -> 0)
        new_encoded = new_encoded.reindex(columns=prep["encoded_columns"], fill_value=0)
        # 3) Standardisation des variables numériques avec le scaler entraîné
        new_scaled = new_encoded.copy()
        new_scaled[prep["numeric_cols"]] = scaler.transform(new_encoded[prep["numeric_cols"]])

        prediction = model.predict(new_scaled)[0]
        proba_risque = model.predict_proba(new_scaled)[0][1] * 100

        st.divider()

        col_result, col_gauge = st.columns([1, 1])

        with col_result:
            if prediction == 1:
                st.error("❌ Demande jugée **risquée**")
            else:
                st.success("✅ Demande jugée **sûre**")
            st.metric("Probabilité de risque estimée", f"{proba_risque:.1f} %")
            st.caption(
                "Rappel : ce modèle reproduit les critères d'une décision historique "
                "(accordé/refusé), pas un vrai indicateur de défaut de paiement constaté."
            )

        with col_gauge:
            gauge_color = COLOR_RISQUE if prediction == 1 else COLOR_SUR
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=proba_risque,
                number={"suffix": " %"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": gauge_color},
                    "steps": [
                        {"range": [0, 50], "color": "#DCFCE7"},
                        {"range": [50, 100], "color": "#FEE2E2"},
                    ],
                },
            ))
            fig_gauge.update_layout(height=220, margin=dict(t=20, b=10, l=20, r=20))
            st.plotly_chart(fig_gauge, width="stretch")

        with st.expander("Quels facteurs pèsent le plus dans les décisions du modèle ?"):
            importances = pd.Series(
                model.feature_importances_, index=prep["encoded_columns"]
            ).sort_values(ascending=False).head(5).reset_index()
            importances.columns = ["Variable", "Importance"]
            fig_imp = px.bar(
                importances.sort_values("Importance"),
                x="Importance",
                y="Variable",
                orientation="h",
                color_discrete_sequence=[COLOR_PRIMARY],
            )
            fig_imp.update_layout(margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig_imp, width="stretch")
            st.caption(
                "Importance globale du modèle (pas spécifique à ce dossier) : ce sont les "
                "variables qui, en général, influencent le plus ses décisions."
            )
