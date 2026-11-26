# Comparaison Folium (séance 2) et MapLibre (séance 3)

## Tableau de mesures

> **Note :** les chiffres de la colonne Folium sont à compléter à partir de votre fichier `carte_pnp.html` et de votre notebook de la séance 2. Pour MapLibre, les valeurs réseau exactes (requêtes et octets transférés totaux) peuvent aussi être vérifiées directement dans l'onglet **Réseau** (`F12`, *Désactiver le cache*, `Ctrl+Maj+R`).

| Mesure | Folium (TP de la séance 2) | MapLibre (étape 8) |
|---|---|---|
| Poids de la page HTML, en octets | *[à compléter : `ls -l carte_pnp.html`]* | 16 092 octets |
| Requêtes au chargement | *[à compléter : onglet Réseau]* | *[à vérifier dans Réseau — environ 23 requêtes, dont les 7 GeoJSON dans `donnees/`]* |
| Octets transférés au chargement | *[à compléter : onglet Réseau]* | *[à vérifier dans Réseau — environ 4,35 Mo au total]* |
| dont les données du parc | *[à compléter : intégrées dans `carte_pnp.html`]* | 3 326 386 octets (somme des 7 fichiers `.geojson` dans `donnees/`) |
| Lignes de code non vides | *[à compléter : cellules du notebook S2]* | 416 lignes (`etape-8.html`) |
| Déplacement et zoom : ce que vous voyez | *[à compléter : zoom par crans entiers, moins fluide]* | Déplacement et zoom continus et très fluides (rendu WebGL2), écritures toujours nettes au-dessus des aplats |

---

## Réponses aux questions

1. **Quelle carte a la page la plus légère, et laquelle transfère le plus d'octets au chargement ? Pourquoi les deux classements ne sont-ils pas les mêmes ?**

   La page HTML la plus légère est largement celle de **MapLibre** (`etape-8.html` pèse 16 092 octets, soit environ 16 Ko), alors que la page Folium est beaucoup plus lourde (plusieurs centaines de kilo-octets même après simplification des géométries). En revanche, au chargement dans le navigateur, la carte **MapLibre** transfère au total davantage d'octets, car les 7 fichiers GeoJSON bruts (non simplifiés, soit 3,33 Mo) sont téléchargés séparément en plus du style, des tuiles vectorielles du Plan IGN et de la bibliothèque MapLibre. Les deux classements ne sont pas les mêmes parce qu'avec Folium les données sont écrites à l'intérieur du fichier HTML, tandis qu'avec MapLibre elles restent dans des fichiers externes chargés par le réseau.

2. **Quelle part des octets transférés par la carte MapLibre revient aux données du parc ? Qu'est-ce qui permettrait de ne transférer que ce que la vue montre ?**

   Les 7 fichiers GeoJSON représentent la majeure partie du volume transféré au chargement : **3 326 386 octets** (~3,33 Mo), soit environ les trois quarts des octets transférés au total (environ 76 % d'après les mesures du cours). Un fichier GeoJSON étant toujours lu en entier avec tous ses objets et tous ses sommets, même hors de la vue courante, il faudrait découper les données en **tuiles vectorielles** (par exemple dans une archive **PMTiles** lue par plages d'octets HTTP, comme vu en séance 4) pour ne télécharger que ce qui correspond à la zone et au niveau de zoom affichés.

3. **L'exigence de poids de la commande est-elle tenue ? Mesure-t-elle encore ce que reçoit le visiteur ?**

   Si l'on regarde uniquement le poids du fichier HTML (`16 092 octets`), l'exigence d'une page de 1 Mo au plus est largement respectée. Toutefois, ce chiffre ne mesure plus réellement ce que reçoit le visiteur : la page HTML est très légère, mais le navigateur télécharge en parallèle plus de 3,3 Mo de fichiers GeoJSON bruts (en plus du fond de carte et de MapLibre).

4. **Qu'est-ce qui a été plus simple avec MapLibre, et qu'est-ce qui a été plus long à écrire ?**

   - **Plus simple avec MapLibre :** personnaliser le fond vectoriel du Plan IGN (changer la couleur de l'eau, masquer les forêts), glisser les couches du parc et les orthophotos sous les écritures pour garder les noms de lieux lisibles, gérer le clic sur les secteurs même sous le cœur sans devoir découper les polygones, filtrer les refuges en direct côté navigateur sans recharger de données, et laisser MapLibre mettre à jour automatiquement les mentions de crédit selon les couches visibles.
   - **Plus long à écrire avec MapLibre :** toute l'interface autour de la carte, notamment le panneau des couches et la légende à coder entièrement en HTML et CSS, ainsi que la gestion complète du survol (écouteurs `mousemove` et `mouseout`, `queryRenderedFeatures`, `feature-state` et mise en forme de l'info-bulle), alors que Folium génère déjà le contrôle de couches et des infobulles simples en quelques lignes de Python.
