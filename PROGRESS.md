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
- Exécuté de bout en bout (`jupyter nbconvert --execute`) : 36 cellules de
  code, 0 erreur. Meilleur rappel sur la classe risque : Arbre de Décision
  (rappel 0.53, accuracy 0.65) ; Régression Logistique/SVM plus précis mais
  moins de rappel.
- Fichier de travail : dossier local `Modélisation - CrediTrust Scoring/`
  (ignoré par git, comme les modules précédents). Copié vers
  `notebooks/nb_03_Modélisation_CrediTrust_Scoring.ipynb` à la racine
  (suivi par git) et commité (2 commits : ajout initial + réécriture avec les
  techniques nb_01/nb_02).
- ⚠️ Demande de réorganisation du dossier (fusionner/supprimer les anciens
  dossiers de module 1 et 2) mise de côté pour l'instant à la demande de
  Loïc : on ne touche pas à `notebooks/nb_01` ni `nb_02` tant que ce n'est
  pas redemandé explicitement.

## Reste à faire
- `nb_03` est commité localement mais **pas encore poussé** sur GitHub —
  demander confirmation avant `git push`.
- Copier le nb_02 complété avec réponses (dossier local) vers `notebooks/`
  à la racine, commiter et pousser (si Loïc le souhaite un jour).
- Vérifier sur GitHub que le notebook nb_01 affiche bien le bon contenu.
- Décider si on supprime un jour les anciens dossiers de module (mis en
  pause pour l'instant, voir ci-dessus).
- Décider quoi faire de `Aide_Memoire_Machine_Learning.html` (non suivi
  par git actuellement).
