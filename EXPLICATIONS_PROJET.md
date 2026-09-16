# CrediTrust Scoring — Explications du projet

Ce document résume simplement ce qui a été fait sur le projet "CrediTrust
Finance" et pourquoi, en reprenant les 4 attendus du brief client.

## 1. Analyse exploratoire (EDA)

**Fait dans** `notebooks/nb_01_...` (prise en main) et surtout
`notebooks/nb_03_Modélisation_CrediTrust_Scoring.ipynb` (section EDA).

On a regardé quels facteurs sont liés au risque (prêt refusé) : revenu,
montant du prêt, historique de crédit, zone géographique, etc.

**Résultat principal** : `Credit_History` (le client a-t-il déjà bien
remboursé un crédit par le passé ?) est de très loin le facteur le plus
déterminant. Les clients sans bon historique de crédit ont un taux de refus
beaucoup plus élevé que les autres.

## 2. Déséquilibre des classes et préparation des variables

**Déséquilibre observé** : 422 prêts accordés (Y) contre 192 refusés (N),
soit environ 31 % de refus. C'est un déséquilibre modéré (pas extrême comme
1 %).

**Traitement testé** : `class_weight="balanced"` (donne plus de poids aux
erreurs sur la classe minoritaire "risque" pendant l'entraînement), essayé
sur Régression Logistique, Arbre de Décision, Random Forest et SVM. Ça
améliore un peu le rappel (ex. Random Forest : 0,50 → 0,55), mais au prix
d'une précision et d'une accuracy nettement plus faibles (0,86 → 0,64 et
0,82 → 0,76), et parfois plus de sur-apprentissage. **Pas retenu** pour le
modèle final : le compromis n'était pas favorable.

**Préparation des variables (prétraitement)**, toujours split train/test
fait *avant* pour éviter toute fuite de données :
- Valeurs manquantes : remplies avec la médiane (colonnes numériques) ou le
  mode (colonnes catégorielles), calculés uniquement sur le jeu
  d'entraînement.
- Variables catégorielles (genre, statut marital, zone...) : encodées en
  colonnes 0/1 (`pd.get_dummies`).
- Variables numériques (revenus, montant du prêt...) : standardisées
  (`StandardScaler`, ajusté sur le train uniquement).

## 3. Comparaison de modèles et choix du modèle final

5 modèles de classification ont été entraînés et comparés sur le jeu de
test : Régression Logistique, Arbre de Décision, Random Forest, KNN, SVM
(linéaire).

Le brief demande de **minimiser les Faux Négatifs** (un client réellement
risqué que le modèle prédit "sûr" à tort — un mauvais payeur qui passe entre
les mailles du filet). Minimiser les Faux Négatifs = maximiser le **rappel**
sur la classe "risque". C'est donc le rappel qui a guidé le choix final, pas
la précision ni l'accuracy seules.

Tableau des résultats (jeu de test, classe "risque"), sans limite de
profondeur :

| Modèle | Accuracy | Précision | Rappel | Sur-apprentissage ? |
|---|---|---|---|---|
| Arbre de Décision | 0.650 | 0.444 | **0.526** | Oui, fort (100 % train vs 65 % test) |
| Random Forest | 0.780 | 0.704 | 0.500 | Oui (100 % train vs 78 % test) |
| Régression Logistique | 0.813 | 0.857 | 0.474 | Non (81,3 % train vs 81,3 % test) |
| SVM (linéaire) | 0.813 | 0.895 | 0.447 | Non (80,9 % train vs 81,3 % test) |
| KNN | 0.707 | 0.556 | 0.263 | Léger écart (81 % train vs 71 % test) |

L'Arbre de Décision et la Random Forest ont le meilleur rappel, mais ils
**sur-apprennent** fortement : ils "récitent" le jeu d'entraînement (100 %
de bonnes réponses) au lieu d'apprendre une vraie règle générale, donc leurs
bons chiffres sur le rappel ne sont pas fiables pour de nouveaux clients.
Un autre problème pratique : un Arbre de Décision seul ne peut prédire que
des probabilités très proches de 0 % ou 100 % (chaque feuille de l'arbre
contient presque toujours un seul type de client).

**Limiter la profondeur (`max_depth`) pour corriger le sur-apprentissage** :
en testant plusieurs profondeurs (2 à 10) pour l'Arbre de Décision et la
Random Forest, **Random Forest avec `max_depth=7`** ressort comme le
meilleur compromis :

| Modèle | Accuracy | Précision | Rappel | Écart train/test |
|---|---|---|---|---|
| **Random Forest (`max_depth=7`)** | **0.821** | **0.864** | 0.500 | ~4 points (contre 22 sans limite) |

C'est la meilleure accuracy et précision de tous les modèles essayés (avec
ou sans limite de profondeur), un rappel aussi bon que l'Arbre de Décision
d'origine, sans son sur-apprentissage. La Random Forest moyenne les votes de
plusieurs arbres, donc ses probabilités sont bien réparties (testé entre 7 %
et 85 % sur le jeu de test) au lieu d'être bloquées à 0 %/100 %.

**Modèle retenu : Random Forest (`max_depth=7`).**

*Remarque : deux essais précédents avaient été faits — SVM linéaire
(meilleure précision brute, 89,5 %, mais moins bon rappel) puis Régression
Logistique (meilleur rappel parmi les modèles "simples" sans réglage de
profondeur). Random Forest avec `max_depth=7` fait mieux que les deux sur
quasiment tous les critères.*

## 4. Dashboard Streamlit

**Fait dans** `dashboard/` (`app.py` + `train_model.py`).

- `train_model.py` réentraîne le modèle retenu (Random Forest,
  `max_depth=7`) avec exactement le même prétraitement que le notebook, et
  sauvegarde le modèle + les informations nécessaires (médianes, modes,
  colonnes) dans `dashboard/models/`.
- `app.py` a 2 onglets :
  - **Analyse de données** : indicateurs clés du portefeuille (nombre de
    dossiers, taux de refus, revenu médian, rappel du modèle) + graphiques
    (répartition accordé/refusé, taux de refus selon l'historique de
    crédit).
  - **Simulateur** : un analyste remplit un formulaire (revenu, montant du
    prêt, historique de crédit...) et obtient instantanément une décision
    (accordé/refusé) avec une estimation de la chance de risque, ainsi que
    les facteurs qui ont le plus pesé dans la décision.

## Limites connues (honnêtes, pour info)

- Le jeu de données n'a pas de vraie colonne "défaut de paiement" : la
  cible utilisée est "prêt accordé ou refusé", qui sert de proxy imparfait
  pour le risque réel.
- `class_weight="balanced"` a été testé pour mieux traiter le déséquilibre
  des classes, mais écarté du modèle final (compromis défavorable, voir
  point 2).
- Le rappel du modèle retenu reste modéré (50,0 %) : environ un client
  réellement risqué sur deux passe encore inaperçu. Un modèle plus
  performant nécessiterait plus de données ou des techniques plus
  avancées.
