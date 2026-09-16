# Application Streamlit du projet CrediTrust Scoring (Activité 4).
# Deux sections :
#   1. Analyse de données : graphiques interactifs et KPIs sur loan_data.csv.
#   2. Simulateur : formulaire connecté au modèle entraîné (train_model.py)
#      pour accorder ou refuser un prêt en temps réel, avec probabilité.
#
# Design : palette et bonnes pratiques générées via le skill ui-ux-pro-max
# (style "Data-Dense Dashboard", palette fintech bleu marine). Les icônes
# sont du SVG (Heroicons, licence MIT), pas des emojis, pour un rendu pro
# cohérent sur toutes les plateformes.

from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="CrediTrust Scoring", page_icon="💳", layout="wide")

# Chemins construits à partir de l'emplacement de ce fichier (et non du dossier
# courant) : ça fonctionne aussi bien en local que sur Streamlit Community
# Cloud, où l'app est lancée depuis la racine du dépôt.
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / "data" / "loan_data.csv"
MODELS_DIR = BASE_DIR / "models"

# --- Palette (issue du design system fintech / dashboard) ---
COLOR_PRIMARY = "#1E40AF"     # bleu marine — couleur principale
COLOR_SECONDARY = "#3B82F6"   # bleu clair
COLOR_ACCENT = "#D97706"      # ambre — accent
COLOR_BACKGROUND = "#F8FAFC"
COLOR_MUTED = "#E9EEF6"
COLOR_BORDER = "#DBEAFE"
COLOR_SUR = "#15803D"         # vert foncé — dossier sûr (contraste AA sur fond clair)
COLOR_SUR_BG = "#DCFCE7"
COLOR_RISQUE = "#DC2626"      # rouge — dossier risqué
COLOR_RISQUE_BG = "#FEE2E2"


# --- Icônes SVG (Heroicons outline, 24x24, licence MIT) ---
ICONS = {
    "credit-card": '<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3M3.75 6h16.5a1.5 1.5 0 0 1 1.5 1.5v9a1.5 1.5 0 0 1-1.5 1.5H3.75a1.5 1.5 0 0 1-1.5-1.5v-9a1.5 1.5 0 0 1 1.5-1.5Z" />',
    "folder": '<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-19.5 0v6a2.25 2.25 0 0 0 2.25 2.25h15a2.25 2.25 0 0 0 2.25-2.25v-6m-19.5 0a2.25 2.25 0 0 1 2.25-2.25h15a2.25 2.25 0 0 1 2.25 2.25m-19.5 0v-.75A2.25 2.25 0 0 1 4.5 7.5h4.379a1.5 1.5 0 0 1 1.06.44l1.122 1.12a1.5 1.5 0 0 0 1.06.44H19.5a2.25 2.25 0 0 1 2.25 2.25v.75" />',
    "x-circle": '<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />',
    "banknotes": '<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18.75a60.07 60.07 0 0 1 15.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 0 1 3 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 0 0-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 0 1-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 0 0 3 15h-.75M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm3 0h.008v.008H18V10.5Zm-12 0h.008v.008H6V10.5Z" />',
    "target": '<path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z" /><path stroke-linecap="round" stroke-linejoin="round" d="M12 16.5a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9Z" /><path stroke-linecap="round" stroke-linejoin="round" d="M12 13.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z" />',
    "check-circle": '<path stroke-linecap="round" stroke-linejoin="round" d="m9 12.75 2.25 2.25 4.5-4.5m5.25 2.25a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />',
    "chart-bar": '<path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z" />',
}


def icon(name: str, size: int = 20, color: str = "currentColor") -> str:
    """Retourne le HTML d'une icône SVG inline (pas d'emoji)."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" '
        f'style="vertical-align:-4px;flex-shrink:0">{ICONS[name]}</svg>'
    )


def kpi_card(icon_name: str, label: str, value: str) -> str:
    """Carte KPI en HTML : n'écrase jamais le texte (contrairement à st.metric)."""
    return f"""
    <div style="background:{COLOR_MUTED};border:1px solid {COLOR_BORDER};border-radius:10px;
                padding:14px 16px;height:100%;">
      <div style="display:flex;align-items:center;gap:8px;color:{COLOR_PRIMARY};
                  font-size:0.82rem;font-weight:600;margin-bottom:6px;">
        {icon(icon_name, 18, COLOR_PRIMARY)}<span>{label}</span>
      </div>
      <div style="font-size:1.5rem;font-weight:700;color:#0F172A;line-height:1.25;
                  word-wrap:break-word;">{value}</div>
    </div>
    """


def verdict_badge(is_risky: bool) -> str:
    bg, fg, icon_name, text = (
        (COLOR_RISQUE_BG, COLOR_RISQUE, "x-circle", "Demande jugée risquée")
        if is_risky
        else (COLOR_SUR_BG, COLOR_SUR, "check-circle", "Demande jugée sûre")
    )
    return f"""
    <div style="background:{bg};color:{fg};border-radius:10px;padding:14px 16px;
                display:flex;align-items:center;gap:10px;font-weight:700;font-size:1.1rem;">
      {icon(icon_name, 24, fg)}<span>{text}</span>
    </div>
    """


st.markdown(
    f"""
    <style>
      .stApp {{ background-color: {COLOR_BACKGROUND}; }}
    </style>
    """,
    unsafe_allow_html=True,
)


# --- Chargement des données et du modèle (mis en cache pour ne pas recharger à chaque clic) ---
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df.dropna(subset=["Loan_Status"]).drop(columns=["Loan_ID"]).reset_index(drop=True)


@st.cache_resource
def load_model_artifacts():
    model = joblib.load(MODELS_DIR / "model.joblib")
    scaler = joblib.load(MODELS_DIR / "scaler.joblib")
    prep = joblib.load(MODELS_DIR / "preprocessing.joblib")
    return model, scaler, prep


df = load_data()
model, scaler, prep = load_model_artifacts()


# ============================================================
# Barre latérale : présentation du projet
# ============================================================
with st.sidebar:
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:8px;">
          {icon("credit-card", 26, COLOR_PRIMARY)}
          <span style="font-size:1.4rem;font-weight:700;color:{COLOR_PRIMARY}">CrediTrust</span>
        </div>
        <div style="color:#64748B;margin-top:2px;">Scoring de risque crédit</div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown(
        """
        **À propos**

        Cet outil aide à décider s'il faut accorder ou refuser une demande
        de prêt, à partir d'un modèle entraîné sur l'historique des
        décisions de CrediTrust.
        """
    )

    # Cartes en HTML (pas st.metric) : le texte "Random Forest (max_depth=7)" ne se
    # tronque jamais, même dans la barre latérale, étroite.
    st.markdown(
        f"""
        <div style="background:{COLOR_MUTED};border:1px solid {COLOR_BORDER};
                    border-radius:10px;padding:12px 14px;margin-bottom:10px;">
          <div style="font-size:0.8rem;color:{COLOR_PRIMARY};font-weight:600;">Modèle utilisé</div>
          <div style="font-size:1.1rem;font-weight:700;color:#0F172A;">Random Forest (max_depth=7)</div>
        </div>
        <div style="background:{COLOR_MUTED};border:1px solid {COLOR_BORDER};
                    border-radius:10px;padding:12px 14px;">
          <div style="font-size:0.8rem;color:{COLOR_PRIMARY};font-weight:600;">Rappel sur la classe risque</div>
          <div style="font-size:1.1rem;font-weight:700;color:#0F172A;">{prep['test_recall'] * 100:.1f} %</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(
        "Le rappel mesure la capacité du modèle à détecter les dossiers "
        "réellement risqués — la priorité métier pour CrediTrust (éviter les "
        "mauvais payeurs non détectés)."
    )


st.markdown(
    f"""
    <div style="display:flex;align-items:center;gap:10px;">
      {icon("credit-card", 32, COLOR_PRIMARY)}
      <span style="font-size:2rem;font-weight:700;color:#0F172A;">CrediTrust Scoring</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("Outil d'aide à la décision pour l'octroi de prêts.")

tab_analyse, tab_simulateur = st.tabs(["Analyse de données", "Simulateur de demande"])


# ============================================================
# Onglet 1 : Analyse de données
# ============================================================
with tab_analyse:
    st.subheader("Vue d'ensemble du portefeuille")

    n_dossiers = len(df)
    taux_refus = (df["Loan_Status"] == "N").mean() * 100
    revenu_median = df["ApplicantIncome"].median()

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(kpi_card("folder", "Dossiers analysés", f"{n_dossiers:,}"), unsafe_allow_html=True)
    col2.markdown(kpi_card("x-circle", "Taux de refus", f"{taux_refus:.1f} %"), unsafe_allow_html=True)
    col3.markdown(kpi_card("banknotes", "Revenu médian", f"{revenu_median:,.0f}"), unsafe_allow_html=True)
    col4.markdown(kpi_card("target", "Rappel du modèle", f"{prep['test_recall'] * 100:.1f} %"), unsafe_allow_html=True)

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
        "le plus déterminant dans les décisions du modèle."
    )


# ============================================================
# Onglet 2 : Simulateur
# ============================================================
with tab_simulateur:
    st.subheader("Simuler une nouvelle demande de prêt")
    st.write("Remplis le formulaire ci-dessous pour obtenir une décision instantanée du modèle.")

    # Les valeurs brutes du jeu de données sont en anglais (Male, Yes, Urban...) car
    # c'est ce que le modèle attend. On affiche des libellés français à l'utilisateur
    # via `format_func`, tout en gardant la vraie valeur anglaise en interne.
    GENDER_LABELS = {"Male": "Homme", "Female": "Femme"}
    YES_NO_LABELS = {"Yes": "Oui", "No": "Non"}
    EDUCATION_LABELS = {"Graduate": "Diplômé", "Not Graduate": "Non diplômé"}
    PROPERTY_AREA_LABELS = {"Urban": "Urbaine", "Semiurban": "Semi-urbaine", "Rural": "Rurale"}
    TERM_LABELS = {
        360.0: "30 ans (360 mois)", 300.0: "25 ans (300 mois)", 240.0: "20 ans (240 mois)",
        180.0: "15 ans (180 mois)", 120.0: "10 ans (120 mois)", 84.0: "7 ans (84 mois)",
        60.0: "5 ans (60 mois)", 36.0: "3 ans (36 mois)", 12.0: "1 an (12 mois)",
        6.0: "6 mois", 480.0: "40 ans (480 mois)",
    }

    with st.form("loan_form"):
        c1, c2, c3 = st.columns(3)

        with c1:
            gender = st.selectbox("Genre", list(GENDER_LABELS), format_func=lambda v: GENDER_LABELS[v])
            married = st.selectbox("Marié(e)", list(YES_NO_LABELS), format_func=lambda v: YES_NO_LABELS[v])
            dependents = st.selectbox("Nombre de personnes à charge", ["0", "1", "2", "3+"])
            education = st.selectbox(
                "Niveau d'études", list(EDUCATION_LABELS), format_func=lambda v: EDUCATION_LABELS[v]
            )

        with c2:
            self_employed = st.selectbox(
                "Indépendant", list(YES_NO_LABELS), format_func=lambda v: YES_NO_LABELS[v]
            )
            property_area = st.selectbox(
                "Zone géographique", list(PROPERTY_AREA_LABELS), format_func=lambda v: PROPERTY_AREA_LABELS[v]
            )
            credit_history = st.selectbox(
                "A déjà bien remboursé un crédit par le passé ?", ["Oui", "Non"]
            )
            loan_amount_term = st.selectbox(
                "Durée du prêt", list(TERM_LABELS), format_func=lambda v: TERM_LABELS[v]
            )

        with c3:
            applicant_income = st.number_input("Revenu du demandeur", min_value=0, value=5000, step=100)
            coapplicant_income = st.number_input("Revenu du co-demandeur", min_value=0, value=0, step=100)
            loan_amount = st.number_input("Montant du prêt demandé (en milliers)", min_value=1, value=150, step=10)

        submitted = st.form_submit_button("Évaluer la demande", width="stretch")

    if submitted:
        # Construire une ligne avec les mêmes colonnes que celles utilisées à l'entraînement
        # (les valeurs restent en anglais ici : ce sont celles que le modèle connaît)
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
        proba_risque = model.predict_proba(new_scaled)[0, 1] * 100

        st.divider()

        col_result, col_gauge = st.columns([1, 1])

        with col_result:
            st.markdown(verdict_badge(is_risky=(prediction == 1)), unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                kpi_card("target", "Chance de risque estimée", f"{proba_risque:.1f} %"),
                unsafe_allow_html=True,
            )
            st.caption(
                f"Selon le modèle utilisé (Random Forest (max_depth=7), {prep['test_recall'] * 100:.1f} % "
                f"de rappel sur la classe risque — la priorité de CrediTrust pour détecter les "
                f"mauvais payeurs), le crédit pourra ou non être accordé, avec une chance de "
                f"risque estimée à {proba_risque:.1f} %. Pour rappel : ce modèle reproduit les "
                f"critères d'une décision historique (accordé/refusé), pas un vrai indicateur de "
                f"défaut de paiement constaté."
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
                        {"range": [0, 50], "color": COLOR_SUR_BG},
                        {"range": [50, 100], "color": COLOR_RISQUE_BG},
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
