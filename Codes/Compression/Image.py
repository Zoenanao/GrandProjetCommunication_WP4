import os
import numpy as np
from PIL import Image


def convert_to_ppm(file, out=None):
    """Convertit n'importe quelle image (jpg, png, webp, bmp, gif...) en PPM binaire (P6).
    Pillow ne sert QU'À ça. Le PPM est le format le plus simple à lire à la main :
    un petit en-tête texte puis les pixels en clair, R G B, ligne par ligne, de haut en bas."""
    if file.lower().endswith(".ppm"):
        return file                                   # déjà au bon format
    if out is None:
        out = os.path.splitext(file)[0] + ".ppm"      # même nom, extension .ppm
    Image.open(file).convert("RGB").save(out, format="PPM")
    return out


def ppm_to_matrice(file):
    """Lit un PPM P6 SANS Pillow et renvoie M, une matrice NumPy 2D de forme (height, length).
    Chaque case est une liste Python : M[i, j] = [r, g, b] pour le pixel ligne i, colonne j."""
    with open(file, "rb") as f:
        data = f.read()

    # --- En-tête : "P6"  largeur  hauteur  valeur_max  (séparés par des espaces / retours ligne)
    champs = []
    pos = 0
    while len(champs) < 4:
        while data[pos:pos + 1].isspace():            # saute les espaces
            pos += 1
        if data[pos:pos + 1] == b"#":                 # saute les commentaires
            while data[pos:pos + 1] not in (b"\n", b""):
                pos += 1
            continue
        debut = pos
        while not data[pos:pos + 1].isspace():
            pos += 1
        champs.append(data[debut:pos])
    pos += 1                                          # un seul blanc avant les pixels

    if champs[0] != b"P6":
        raise ValueError("Ce n'est pas un PPM binaire (P6)")
    length, height, maxval = int(champs[1]), int(champs[2]), int(champs[3])
    if maxval > 255:
        raise ValueError("PPM 16 bits non géré")

    # --- Pixels : 3 octets par pixel (R, G, B), aucune marge en fin de ligne
    M = np.empty((height, length), dtype=object)      # matrice 2D, chaque case peut contenir un objet Python
    for i in range(height):
        for j in range(length):
            p = pos + 3 * (i * length + j)
            M[i, j] = [data[p], data[p + 1], data[p + 2]]   # la case reçoit une liste [r, g, b]
    return M


def image_to_matrice(file):
    """Image de n'importe quel format -> matrice 2D M, avec M[i, j] = [r, g, b] (liste Python)."""
    return ppm_to_matrice(convert_to_ppm(file))

def reduce_color_span(Matrice, compression_rate):
    height, length = Matrice.shape
    for i in range(height):
        for j in range(length):
            L = Matrice[i, j] 
            for e in L:
                X=[]
                e=
                
if __name__ == "__main__":
    file = input("Saisir File : ")
    M = image_to_matrice(file)
