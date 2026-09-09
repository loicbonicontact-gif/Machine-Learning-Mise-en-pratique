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

## Reste à faire
- Vérifier sur GitHub que le notebook nb_01 affiche bien le bon contenu.
- Décider si on supprime les anciens dossiers de module maintenant qu'ils
  sont dupliqués (à faire quand tu seras prêt·e).
- Continuer le travail sur nb_02 (Apprentissage Supervisé / Classification).
