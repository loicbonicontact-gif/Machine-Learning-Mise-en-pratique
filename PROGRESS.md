# Suivi du projet

## Où on en est (2026-09-09)
- Le dossier "Machine Learning" est maintenant un dépôt git relié à
  https://github.com/loicbonicontact-gif/Machine-Learning-Mise-en-pratique
  (remote `origin`, branche `main`).
- Structure du repo alignée sur GitHub : `notebooks/`, `data/`, `assets/`,
  `README.md` directement à la racine (au lieu d'un dossier par module).
- Le notebook `nb_01_Intro_ML_Prétraitement_Données.ipynb` (dernière version
  locale) a été copié dans `notebooks/` et poussé sur GitHub.

## Décisions prises
- Racine du repo = dossier "Machine Learning" (pas un sous-dossier par module),
  pour matcher la structure déjà présente sur GitHub.
- Les anciens dossiers "Introduction au Machine Learning et Prétraitement des
  Données" et "Apprentissage Supervisé - Classification" sont conservés en
  local (pas supprimés) mais ignorés par git (ajoutés au `.gitignore`) car
  leur contenu est dupliqué dans `notebooks/` et `data/` à la racine.

## Où on en est (suite, 2026-09-09)
- nb_02 (Apprentissage Supervisé - Classification) a été exécuté entièrement
  (29 cellules de code, aucune erreur). Il n'avait jamais été lancé avant.
  ⚠️ À ce stade, les 20 cellules d'exercice étaient encore vides (juste un
  commentaire), donc l'exécution "sans erreur" ne prouvait rien.

## Où on en est (suite 2, 2026-09-09)
- Le notebook `Apprentissage Supervisé - Classification/notebooks/nb_02_...`
  (dossier local, ignoré par git) a été complété : les 29 cellules de code
  contiennent maintenant du vrai code (chargement Iris, EDA, prétraitement,
  split train/test + standardisation, entraînement de 5 modèles — KNN,
  Régression Logistique, SVM linéaire, Arbre de Décision, Random Forest —,
  prédictions, interprétation des coefficients/importances, et évaluation
  complète avec matrices de confusion + accuracy/precision/recall/F1).
- Exécuté de bout en bout avec `jupyter nbconvert --execute` : 0 erreur sur
  les 29 cellules. Scores obtenus : SVM 96.7%, les autres modèles ~93.3%
  d'accuracy sur le jeu de test.

## Où on en est (suite 3, 2026-09-09)
- Le nb_02 complété a été copié vers `notebooks/nb_02_Apprentissage_Supervisé_Classification.ipynb`
  (racine du repo, suivi par git) et commité. Reste à pousser sur GitHub
  (`git push`).

## Où on en est (suite 4, 2026-09-11)
- Répondu à TOUTES les questions du nb_02 (quiz 10 scénarios + 23 cellules
  "Question") directement dans les cellules markdown, en français, avec les
  vraies valeurs observées. Code non modifié (il était correct).
- Notebook ré-exécuté de bout en bout : 29 cellules de code, 0 erreur.
  Fichier édité : dossier local `Apprentissage Supervisé - Classification/
  notebooks/` (ignoré par git). ⚠️ Pas encore copié vers `notebooks/` racine
  ni commité/poussé.

## Où on en est (suite 5, 2026-09-15)
- Activité 3 (projet CrediTrust Scoring) réalisée et **validée par Loïc** :
  nouveau notebook `nb_03_Modélisation_CrediTrust_Scoring.ipynb`, basé sur
  `data/loan_data.csv`.
  Contenu : EDA (facteurs de risque, `Credit_History` ressort comme facteur
  dominant), prétraitement sans fuite de données (split train/test avant
  imputation/encodage/scaling), entraînement de 5 modèles de classification
  binaire (Logistique, Arbre de Décision, Random Forest, KNN, SVM linéaire),
  cible encodée comme "risque" (1 = prêt refusé, seul proxy disponible dans
  ce jeu de données car il n'y a pas de vraie colonne "défaut de paiement")
  pour que le rappel corresponde bien à la réduction des Faux Négatifs
  métier, comparaison des modèles avec priorité au rappel, interprétation
  (coefficients de la régression logistique + importances de l'arbre et de
  la random forest).
- Techniques volontairement limitées à celles déjà vues dans nb_01
  (`pd.get_dummies`, `fillna` médiane/mode) et nb_02 (entraînement modèle par
  modèle, `StandardScaler` fit/transform, dictionnaires prédictions/métriques)
  — pas de `Pipeline`/`ColumnTransformer` (jamais vu avant, retiré après
  relecture de Loïc).
- Sur demande de Loïc : les 5 modèles sont entraînés et comparés, mais seuls
  les **3 meilleurs sur le rappel** sont gardés pour l'analyse détaillée
  (matrices de confusion, interprétabilité) et le choix du modèle optimal —
  au lieu d'analyser les 5. Les 3 retenus : Arbre de Décision, Random
  Forest, Régression Logistique (KNN et SVM écartés, rappel plus faible).
- Exécuté de bout en bout (`jupyter nbconvert --execute`) : 35 cellules de
  code, 0 erreur. Meilleur rappel sur la classe risque : Arbre de Décision
  (rappel 0.53, accuracy 0.65).
- Fichier de travail : dossier local `Modélisation - CrediTrust Scoring/`
  (ignoré par git, comme les modules précédents). Copié vers
  `notebooks/nb_03_Modélisation_CrediTrust_Scoring.ipynb` à la racine
  (suivi par git) et commité (3 commits : ajout initial, réécriture avec les
  techniques nb_01/nb_02, puis sélection top 3 modèles).
- ⚠️ Demande de réorganisation du dossier (fusionner/supprimer les anciens
  dossiers de module 1 et 2) mise de côté pour l'instant à la demande de
  Loïc : on ne touche pas à `notebooks/nb_01` ni `nb_02` tant que ce n'est
  pas redemandé explicitement.

## Où on en est (suite 6, 2026-09-15)
- Activité 4 (Dashboard Streamlit) réalisée : dossier `dashboard/` à la
  racine (suivi par git) avec `app.py`, `train_model.py` et `models/`
  (modèle + prétraitement sauvegardés).
- `train_model.py` reproduit exactement le prétraitement/entraînement de
  `nb_03` (nettoyage, split, remplissage médiane/mode appris sur le train,
  encodage `get_dummies`, `StandardScaler`) et entraîne le modèle retenu
  dans l'Activité 3 (Arbre de Décision, choix confirmé par Loïc). Sauvegarde
  le modèle, le scaler et les infos de prétraitement (médianes, modes,
  colonnes encodées) avec `joblib` dans `models/`.
- `app.py` a 2 onglets :
  - **Analyse de données** : KPIs (nb dossiers, taux de refus, revenu médian,
    rappel du modèle) + graphiques interactifs (répartition des décisions,
    revenu vs décision, taux de refus par historique de crédit, filtre par
    zone géographique).
  - **Simulateur** : formulaire (revenu, montant du prêt, historique de
    crédit, etc.) qui applique le même prétraitement que l'entraînement et
    affiche la décision (accordé/refusé) + probabilité de risque.
- Testé avec `streamlit.testing.v1.AppTest` (exécution du script + simulation
  de 2 soumissions de formulaire : un profil sûr → "sûr" 0% risque, un profil
  sans historique de crédit → "risqué" 100% risque) : aucune exception.
- `streamlit` installé (gratuit, package Python).
- Fichier de travail : dossier local `Dashboard CrediTrust Scoring/` (ignoré
  par git, comme les modules précédents).

## Où on en est (suite 7, 2026-09-15)
- Dashboard amélioré suite aux retours de Loïc :
  - Onglet "Analyse de données" gardé (requis par la consigne) mais allégé
    à l'essentiel (4 KPIs + 2 graphiques).
  - Design "pro" appliqué via le skill `ui-ux-pro-max` : palette fintech
    bleu marine validée WCAG AA, icônes SVG (Heroicons) à la place des
    emojis, cartes KPI en HTML personnalisées (corrige un vrai bug :
    `st.metric` tronquait le texte "Arbre de Décision" dans la barre
    latérale).
  - Chemins de fichiers rendus robustes (`Path(__file__)` au lieu de
    chemins relatifs `../data/...`) pour fonctionner aussi bien en local
    que sur Streamlit Community Cloud (qui lance l'app depuis la racine du
    dépôt, pas depuis `dashboard/`).
  - `dashboard/requirements.txt` ajouté (streamlit, pandas, scikit-learn,
    plotly, joblib, versions figées) pour que Streamlit Cloud installe le
    bon environnement.
- **Poussé sur GitHub** (`git push`, avec l'accord de Loïc car il voulait
  publier l'app en ligne) : 13 commits (nb_03 complet + dashboard complet).

## Reste à faire
- Connecter le dépôt GitHub à Streamlit Community Cloud pour obtenir un
  lien public (étape à faire par Loïc lui-même : il doit se connecter avec
  son compte GitHub sur share.streamlit.io et choisir le fichier
  `dashboard/app.py`).
- Tester manuellement l'app dans un vrai navigateur en local — déjà fait
  par Loïc, quelques retours de design déjà traités (troncature du texte,
  emojis, allègement de l'onglet analyse).
- Copier le nb_02 complété avec réponses (dossier local) vers `notebooks/`
  à la racine, commiter et pousser (si Loïc le souhaite un jour).
- Vérifier sur GitHub que le notebook nb_01 affiche bien le bon contenu.
- Décider si on supprime un jour les anciens dossiers de module (mis en
  pause pour l'instant, voir ci-dessus).
- Décider quoi faire de `Aide_Memoire_Machine_Learning.html` (non suivi
  par git actuellement).
