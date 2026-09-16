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

## Où on en est (suite 8, 2026-09-16)
- Vérification de l'organisation du dossier : structure conforme aux
  décisions déjà prises (racine = `notebooks/`, `data/`, `assets/`,
  `dashboard/`, `README.md` ; anciens dossiers par module gardés en local,
  ignorés par git). Le dossier local `Dashboard CrediTrust Scoring/`
  (ignoré) est identique à `dashboard/` (suivi), donc pas de divergence de
  contenu.
- `Aide_Memoire_Machine_Learning.html` ajouté au `.gitignore` (décision de
  Loïc : fichier personnel, pas lié au repo GitHub).
- Modification mineure de métadonnée (nom du kernel Jupyter) sur
  `notebooks/nb_03_Modélisation_CrediTrust_Scoring.ipynb` commitée (sans
  impact sur le contenu, sur demande de Loïc).

## Où on en est (suite 9, 2026-09-16)
- Rangement local demandé par Loïc :
  - `notebooks/nb_02_Apprentissage_Supervisé_Classification.ipynb` (racine,
    suivi par git) remplacé par la version complète avec les 24 cellules
    de réponses (celle du dossier local) — vérifié cellule par cellule
    avant copie, aucune perte. Commité et poussé.
  - Les 4 anciens dossiers par module ("Introduction au Machine Learning et
    Prétraitement des Données", "Apprentissage Supervisé - Classification",
    "Modélisation - CrediTrust Scoring", "Dashboard CrediTrust Scoring")
    regroupés dans un nouveau dossier local `archive/` (toujours ignoré par
    git en bloc via `/archive/` dans `.gitignore`, plus simple qu'une
    entrée par dossier). Décision de Loïc : gardés, pas supprimés.
  - Racine du projet maintenant : `notebooks/`, `data/`, `assets/`,
    `dashboard/`, `archive/` (local, ignoré), `README.md`, `PROGRESS.md`.

## Où on en est (suite 10, 2026-09-16)
- Sur demande de Loïc : ajout d'une cellule d'observation après l'entraînement
  de chacun des 5 modèles de `nb_03` (section 4). Après chaque `.fit()`, une
  cellule de code calcule le score (accuracy) sur le jeu d'entraînement, puis
  une cellule markdown compare ce score à l'accuracy test (calculée plus loin,
  section 5) pour repérer le sur-apprentissage.
  - KNN : train 81 % vs test 71 % — écart net, cohérent avec son
    fonctionnement (mémorisation des points, pas de vraie généralisation).
  - Régression Logistique : train 81,3 % vs test 81,3 % — pas d'écart, bonne
    généralisation (frontière linéaire simple).
  - SVM linéaire : train 80,9 % vs test 81,3 % — idem, pas de sur-apprentissage.
  - Arbre de Décision : train 100 % vs test 65 % — sur-apprentissage flagrant
    (arbre non limité en profondeur, mémorise le train).
  - Random Forest : train 100 % vs test 78 % — sur-apprentissage aussi, mais
    atténué par le moyennage de plusieurs arbres.
  - Notebook réexécuté de bout en bout (`jupyter nbconvert --execute`) :
    60 cellules, 0 erreur. Commité et poussé. Copie locale dans
    `archive/Modélisation - CrediTrust Scoring/` resynchronisée.

## Où on en est (suite 11, 2026-09-16)
- Sur demande de Loïc : changement du critère de choix du modèle du dashboard,
  du rappel vers la **précision (classe risque)**. Tableau nb_03 (jeu de
  test) : SVM linéaire 0.895, Régression Logistique 0.857, Random Forest
  0.704, KNN 0.556, Arbre de Décision 0.444 (le pire — cohérent avec son
  sur-apprentissage déjà observé).
- `dashboard/train_model.py` : modèle changé pour `SVC(kernel='linear',
  probability=True)` (le `probability=True` est ajouté par rapport à nb_03,
  nécessaire pour que l'app affiche un pourcentage de risque). Modèle
  réentraîné, `models/` mis à jour (précision test 0.895, conforme à nb_03).
- `dashboard/app.py` mis à jour : libellé "Arbre de Décision" → "SVM
  (linéaire)", "Rappel" → "Précision" (barre latérale + KPI).
- 2 bugs corrigés dans `app.py` (repérés en testant le simulateur) :
  - `proba_risque` était un tableau numpy au lieu d'un nombre → plantage au
    formatage (`f"{proba_risque:.1f}"`). Corrigé avec `[0, 1]` au lieu de
    `[:, 1]`.
  - `model.feature_importances_` n'existe que pour les modèles à base
    d'arbres (Decision Tree/Random Forest) ; le SVM linéaire utilise
    `model.coef_` à la place (valeur absolue, variables standardisées donc
    comparables).
- Sur demande de Loïc : texte du résultat du simulateur reformulé pour éviter
  le terme "probabilité" (qui donnait l'impression que le modèle sortait
  souvent 0 %/100 % avec l'ancien Arbre de Décision, un artefact de son
  sur-apprentissage). Nouveau message : "Selon la précision du modèle
  utilisé (SVM linéaire, X % de précision...), le crédit pourra ou non être
  accordé, avec une chance de risque estimée à Y %." Vérifié que le SVM ne
  sature plus à 0/100 (ex. testé : 21,2 % et 92,3 % sur deux profils).
- Testé avec `streamlit.testing.v1.AppTest` (chargement + soumission du
  formulaire) : aucune exception.
- ⚠️ Pas encore commité/poussé (à faire si Loïc valide le résultat en local).

## Où on en est (suite 12, 2026-09-16)
- Loïc a partagé le brief officiel du projet client CrediTrust Finance. En le
  comparant à nos changements, on a trouvé un problème : le brief demande
  explicitement de **minimiser les Faux Négatifs** (mauvais payeurs non
  détectés), ce qui veut dire prioriser le **rappel**, pas la précision. Le
  choix du SVM linéaire (suite 11, sur demande de Loïc) allait donc à
  l'encontre de la consigne.
- Discuté avec Loïc : il ne veut pas d'un modèle qui sur-apprend (donc
  Arbre de Décision et Random Forest écartés, malgré leur meilleur rappel,
  car 100 % en train). Parmi les modèles restants (Régression Logistique,
  SVM linéaire, KNN), Loïc a choisi la **Régression Logistique**
  (recommandation) : meilleur rappel (0.474) des modèles sans
  sur-apprentissage, bonne précision (0.857), accuracy 0.813.
- `dashboard/train_model.py` et `dashboard/app.py` remis à jour pour la
  Régression Logistique (au lieu du SVM) : libellés "Rappel"/"Régression
  Logistique", modèle réentraîné et sauvegardé dans `models/`. Message du
  simulateur reformulé pour mentionner le rappel (priorité métier) tout en
  gardant le langage "chance de risque" demandé par Loïc. Testé avec
  `streamlit.testing.v1.AppTest` : aucune exception.
- Création de `EXPLICATIONS_PROJET.md` (racine du repo) : résumé pédagogique
  simple des 4 attendus du brief (EDA, déséquilibre des classes/prétraitement,
  comparaison de modèles avec tableau des métriques, dashboard), avec les
  raisons des choix faits et une section "Limites connues" honnête
  (déséquilibre des classes non traité activement, rappel encore modéré à
  47,4 %, cible = proxy "prêt refusé" et non un vrai défaut de paiement).

## Où on en est (suite 13, 2026-09-16)
- Sur demande de Loïc : essayé de limiter le sur-apprentissage de l'Arbre de
  Décision et de la Random Forest avec `max_depth`, et testé
  `class_weight="balanced"` pour traiter le déséquilibre des classes (31 %
  de refus) — objectif : plus jamais de probabilité bloquée à 0 %/100 %.
- Nouvelle **section 8** ajoutée dans `nb_03` ("Aller plus loin : limiter la
  profondeur et traiter le déséquilibre des classes") :
  - Boucle sur `max_depth` (2 à 10, + aucune limite) pour l'Arbre de
    Décision et la Random Forest, tableau comparatif accuracy train/test +
    précision + rappel à chaque profondeur.
  - `max_depth=7` pour la Random Forest ressort comme le meilleur
    compromis : accuracy test 82,1 % (la meilleure de tous les modèles
    essayés), précision 86,4 % (la meilleure aussi), rappel 50,0 % (aussi
    bon que l'Arbre de Décision d'origine), écart train/test réduit à ~4
    points (au lieu de 22 points sans limite de profondeur, 35 points pour
    l'Arbre de Décision seul).
  - `class_weight="balanced"` testé sur Régression Logistique, Arbre de
    Décision, Random Forest, SVM : améliore un peu le rappel (ex. Random
    Forest depth=7 : 0,50 → 0,55) mais dégrade nettement la précision et
    l'accuracy (0,86 → 0,64 et 0,82 → 0,76), et augmente parfois le
    sur-apprentissage. **Pas retenu** pour le modèle final — documenté
    comme piste explorée mais écartée.
  - Vérifié que les probabilités prédites par la Random Forest
    (`max_depth=7`) ne sont plus bloquées à 0 %/100 % : distribution
    étalée entre 7 % et 85 % sur le jeu de test (histogramme ajouté),
    contrairement à l'Arbre de Décision seul qui ne peut prédire que des
    probabilités quasi pures (chaque feuille contient un seul type de
    client).
  - Conclusion du notebook (partie 9, ex-partie 7) mise à jour pour refléter
    ce nouveau modèle final.
  - Une cellule cassée trouvée dans nb_03 lors d'une session précédente
    (`classification_report` sur des variables pas encore définies à cet
    endroit, gardée telle quelle sur demande de Loïc) bloquait l'exécution
    complète du notebook — supprimée avec l'accord de Loïc (faisait
    doublon avec la partie 5 qui fait déjà ce calcul proprement).
  - Notebook réexécuté de bout en bout (`jupyter nbconvert --execute`) :
    0 erreur, 81 cellules.
- `dashboard/train_model.py` et `dashboard/app.py` mis à jour pour utiliser
  Random Forest (`max_depth=7`) au lieu de la Régression Logistique.
  Réentraîné, testé avec `streamlit.testing.v1.AppTest` (chargement +
  soumission du formulaire) : aucune exception. Vérifié manuellement que
  deux profils différents donnent des probabilités non saturées (19,3 % et
  80,8 %).
- `EXPLICATIONS_PROJET.md` mis à jour avec le nouveau modèle final et les
  résultats de l'exploration `max_depth`/`class_weight`.
- ⚠️ Pas encore commité/poussé (à faire si Loïc valide le résultat en local).

## Reste à faire (mis à jour)
- Loïc valide le dashboard en local (`streamlit run dashboard/app.py`) avant
  commit/push.
- Connecter le dépôt GitHub à Streamlit Community Cloud (à faire par Loïc).
- Vérifier sur GitHub que le notebook nb_01 affiche bien le bon contenu.
- Décider un jour si on supprime définitivement `archive/` (pour l'instant
  gardé en local, pas suivi par git).
