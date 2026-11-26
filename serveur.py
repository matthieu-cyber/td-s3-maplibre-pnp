"""Petit serveur web de TD : sert le dossier courant et honore les requêtes par plage HTTP.

Le serveur de base de Python (python -m http.server) renvoie toujours le fichier entier, même
quand le navigateur n'en demande qu'un morceau. Les PMTiles et les COG lisent un fichier par
morceaux : ils refusent ce serveur. Celui-ci ne dépend que de la bibliothèque standard.

Sur Onyxia, l'adresse du port est publique : ce serveur n'affiche pas la liste des dossiers et
refuse les fichiers cachés (.env, .git...). Il publie tout de même le dossier depuis lequel on le
lance, sous-dossiers compris : le lancer depuis le dossier du TD, jamais depuis ~ ou ~/work.

Usage : python3 serveur.py 5000      (5000 = port ouvert dans la configuration du service Onyxia)
"""
import errno
import os
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlsplit

PLAGE = re.compile(r"bytes=(\d*)-(\d*)$")


class Gestionnaire(SimpleHTTPRequestHandler):
    extensions_map = SimpleHTTPRequestHandler.extensions_map.copy()
    extensions_map.update({
        ".mjs": "text/javascript",
        ".js": "text/javascript",
        ".json": "application/json",
        ".geojson": "application/geo+json",
        ".pmtiles": "application/octet-stream",
        ".tif": "image/tiff",
    })

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")  # annonce le service par plage
        self.send_header("Cache-Control", "no-store")  # en TD, toujours la dernière version du fichier
        super().end_headers()

    def list_directory(self, path):
        self.send_error(404, "Pas de liste de dossier",
                        "Ce serveur n'affiche pas le contenu des dossiers : ouvrir un fichier, par exemple index.html.")
        return None

    def send_head(self):
        for partie in unquote(urlsplit(self.path).path).split("/"):
            if partie.startswith("."):  # fichier ou dossier caché : .env, .git...
                self.send_error(404, "Fichier cache refuse")
                return None

        demande = self.headers.get("Range")
        chemin = self.translate_path(self.path)
        if not demande or not os.path.isfile(chemin):
            return super().send_head()  # pas de plage demandée : comportement normal

        taille = os.path.getsize(chemin)
        trouve = PLAGE.match(demande.strip())
        if not trouve or trouve.groups() == ("", ""):
            return super().send_head()  # plage illisible ou multiple : fichier entier, comme le prévoit HTTP
        debut, fin = trouve.groups()
        if debut == "":  # forme bytes=-N : les N derniers octets
            debut, fin = max(0, taille - int(fin)), taille - 1
        else:
            debut = int(debut)
            fin = min(int(fin), taille - 1) if fin else taille - 1
        if debut >= taille or debut > fin:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{taille}")
            self.end_headers()
            return None

        fichier = open(chemin, "rb")
        fichier.seek(debut)
        self.longueur = fin - debut + 1
        self.send_response(206)  # 206 = contenu partiel
        self.send_header("Content-Type", self.guess_type(chemin))
        self.send_header("Content-Range", f"bytes {debut}-{fin}/{taille}")
        self.send_header("Content-Length", str(self.longueur))
        self.end_headers()
        return fichier

    def copyfile(self, source, destination):
        longueur = getattr(self, "longueur", None)
        if longueur is None:
            return super().copyfile(source, destination)
        self.longueur = None
        destination.write(source.read(longueur))  # n'envoie que la plage demandée


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    try:
        serveur = ThreadingHTTPServer(("0.0.0.0", port), Gestionnaire)
    except OSError as erreur:
        if erreur.errno != errno.EADDRINUSE:
            raise
        print(f"Le port {port} est déjà pris : un serveur tourne sans doute dans un autre terminal.")
        print("L'arrêter (Ctrl+C dans son terminal, ou : pkill -f serveur.py ; pkill -f http.server), puis relancer.")
        sys.exit(1)

    print(f"Dossier servi : {os.getcwd()}")
    if not os.path.isfile("index.html"):
        print("Attention : pas d'index.html dans ce dossier. Vérifier le dossier de lancement (cd).")
    print(f"Serveur lancé sur le port {port} (Ctrl+C pour l'arrêter)")
    serveur.serve_forever()
