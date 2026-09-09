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

## Reste à faire
- Pousser les derniers commits sur GitHub (`git push`).
- Vérifier sur GitHub que le notebook nb_01 affiche bien le bon contenu.
- Décider si on supprime les anciens dossiers de module maintenant qu'ils
  sont dupliqués (à faire quand tu seras prêt·e).
