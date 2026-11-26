# TD - La carte du Parc national des Pyrénées avec MapLibre

Réalisation du TD de la séance 3 de l'UE 902-1 (Webmapping - Master 2 SIGMA) : reconstruction de la carte du Parc national des Pyrénées avec **MapLibre GL JS**, en huit étapes progressives.

## Contenu du dépôt

- `index.html` : page d'accueil listant les liens vers toutes les étapes du TD.
- `etape-0.html` à `etape-8.html` : progression étape par étape :
  1. Carte sur le fond vectoriel Plan IGN cadrée sur le parc (`fitBounds`, contrôles de navigation et d'échelle).
  2. Modification de deux couches du style Plan IGN (surfaces en eau et masquage des forêts fermées).
  3. Chargement des couches GeoJSON du parc (`coeur`, `secteurs`, `aire`, `lacs`, `sentiers`, `refuges`) insérées sous les écritures du Plan IGN.
  4. Expressions de style (`step`, `interpolate`, `match`) et ajout des maisons du parc (`icones/maison.png`).
  5. Fenêtre au clic sur les secteurs.
  6. Info-bulle et mise en évidence au survol (`feature-state`).
  7. Panneau repliable des couches et de la légende, photographies aériennes (WMTS) et BD Forêt v2 (WMS).
  8. Filtre interactif des refuges par type (`setFilter`).
- `donnees/` : fichiers GeoJSON du Parc national des Pyrénées et fichier `LISEZMOI.txt`.
- `icones/maison.png` : pictogramme des maisons du parc.
- `comparaison.md` : comparaison entre la carte Folium (séance 2) et la carte MapLibre (étape 8).
- `serveur.py` : serveur web local fourni dans le TD.

## Ouvrir la carte en local

Les pages MapLibre ne doivent pas être ouvertes directement en `file://` (double clic). Il faut lancer le serveur web depuis ce dossier :

```bash
python3 serveur.py 5000
```

Puis ouvrir `http://localhost:5000/` (ou l'adresse du port 5000 sur le SSP Cloud).

## Sources et mentions de crédit

- Fond cartographique et couches raster : **IGN** (Plan IGN, Photographies aériennes, BD Forêt v2)
- Cœur, aire d'adhésion et secteurs : **DREAL Nouvelle-Aquitaine**
- Lacs : **IGN, BD TOPO** ; altitude : **IGN, RGE ALTI**
- Sentiers, refuges et maisons du parc : **Parc national des Pyrénées**
