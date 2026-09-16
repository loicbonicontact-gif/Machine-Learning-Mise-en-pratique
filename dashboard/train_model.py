# Ce script reproduit exactement le prétraitement et l'entraînement de nb_03
# (Activité 3), puis sauvegarde tout ce qu'il faut pour que l'application
# Streamlit (app.py) puisse transformer une nouvelle demande de prêt de la
# même façon et faire une prédiction.

import joblib
import pandas as pd
from sklearn.metrics import precision_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

NUMERIC_COLS = ["ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term"]
CATEGORICAL_COLS = ["Gender", "Married", "Dependents", "Education", "Self_Employed", "Property_Area"]

# --- 1. Chargement et nettoyage (identique à nb_03) ---
df = pd.read_csv("../data/loan_data.csv")
df = df.dropna(subset=["Loan_Status"]).drop(columns=["Loan_ID"]).reset_index(drop=True)

# Cible : 1 = prêt risqué/refusé, 0 = prêt sûr/accordé
y = (df["Loan_Status"] == "N").astype(int)
X = df.drop(columns=["Loan_Status"])

# --- 2. Split train/test (avant tout calcul, pour éviter la fuite de données) ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- 3. Valeurs manquantes : médiane/mode appris sur le train uniquement ---
numeric_medians = {col: X_train[col].median() for col in NUMERIC_COLS}
credit_history_mode = X_train["Credit_History"].mode()[0]
categorical_modes = {col: X_train[col].mode()[0] for col in CATEGORICAL_COLS}

for col, value in numeric_medians.items():
    X_train[col] = X_train[col].fillna(value)
    X_test[col] = X_test[col].fillna(value)

X_train["Credit_History"] = X_train["Credit_History"].fillna(credit_history_mode)
X_test["Credit_History"] = X_test["Credit_History"].fillna(credit_history_mode)

for col, value in categorical_modes.items():
    X_train[col] = X_train[col].fillna(value)
    X_test[col] = X_test[col].fillna(value)

# --- 4. Encodage des variables catégorielles (get_dummies + alignement des colonnes) ---
X_train_encoded = pd.get_dummies(X_train, columns=CATEGORICAL_COLS)
X_test_encoded = pd.get_dummies(X_test, columns=CATEGORICAL_COLS)
X_test_encoded = X_test_encoded.reindex(columns=X_train_encoded.columns, fill_value=0)

encoded_columns = X_train_encoded.columns.tolist()

# --- 5. Standardisation des variables numériques (fit sur train, transform sur test) ---
scaler = StandardScaler()
X_train_scaled = X_train_encoded.copy()
X_test_scaled = X_test_encoded.copy()
X_train_scaled[NUMERIC_COLS] = scaler.fit_transform(X_train_encoded[NUMERIC_COLS])
X_test_scaled[NUMERIC_COLS] = scaler.transform(X_test_encoded[NUMERIC_COLS])

# --- 6. Entraînement du modèle retenu dans nb_03 : le SVM (linéaire) ---
# (choisi car meilleure précision sur la classe "risque" parmi les 5 modèles
# comparés dans l'activité 3 : 0.895, devant Régression Logistique 0.857)
# probability=True est ajouté (absent de nb_03) car l'app a besoin de
# predict_proba pour afficher un pourcentage de risque, pas seulement une
# décision accordé/refusé.
model = SVC(kernel="linear", probability=True, random_state=42)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
test_precision = precision_score(y_test, y_pred, pos_label=1)
print(f"Précision sur la classe risque (jeu de test) : {test_precision:.3f}")

# --- 7. Sauvegarde du modèle et de tout le nécessaire pour reproduire le prétraitement ---
joblib.dump(model, "models/model.joblib")
joblib.dump(scaler, "models/scaler.joblib")
joblib.dump(
    {
        "numeric_cols": NUMERIC_COLS,
        "categorical_cols": CATEGORICAL_COLS,
        "numeric_medians": numeric_medians,
        "credit_history_mode": credit_history_mode,
        "categorical_modes": categorical_modes,
        "encoded_columns": encoded_columns,
        "test_precision": test_precision,
    },
    "models/preprocessing.joblib",
)

print("Modèle et prétraitement sauvegardés dans models/.")
