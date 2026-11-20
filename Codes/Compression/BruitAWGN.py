# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 17:32:23 2026

@author: denad
"""

import numpy as np
import matplotlib.pyplot as plt
from statistics import NormalDist

class erreur:
    def canal_awgn(bits, ber_cible=1e-3, rng=None):  #pas bpsk
        
        """BER cible avant correction ;  +1/-1."""
        
        bits = np.asarray(bits)
        
        if bits.ndim != 1 or bits.size == 0:
            raise ValueError("Fournir un tableau 1D non vide.")
            
        if not np.all((bits == 0) | (bits == 1)):
            raise ValueError("Les bits doivent valoir 0 ou 1.")
            
        if not 0 < ber_cible < 0.5:
            raise ValueError("BER cible entre 0 et 0.5 exclus.")
            
    #rng = liste d'erreurs 
        rng = np.random.default_rng() if rng is None else rng
    
    
    # Calibrage du bruit selon le BER theorique souhaite.
    
        q = -NormalDist().inv_cdf(ber_cible)  #NormalDist :  loi normale moyenne = 0 avec 1er ecart type = 1
                                              # inv_cdf : renvoie le nb x tel que la proba d'obtenir une valeur infé à x soit p=10e-3 
        sigma = 1.0 / q                       # q=3.09 pour proba de 10e-3
        
        symboles = 1.0 - 2.0 * bits.astype(float)  # transforme 0 en +1, 1 en -1   
       
        bruit = rng.normal(0.0, sigma, size=bits.size)  #0,0 = moyenne, sigma = taux d'erreur
        signal_recu = symboles + bruit
        bits_recus = (signal_recu < 0).astype(np.uint8)  #astype(np.uint8) : transforme en binaire
        llr = 2.0 * signal_recu / sigma**2    #pour etre sur de ce qu'on trouve x2 
    
        return {
            "bits_recus": bits_recus,
            "signal_recu": signal_recu,
            "bruit": bruit,
            "sigma": sigma,
            "ebn0_db": 10.0 * np.log10(q**2 / 2.0),
            "llr": llr,
        }


# Initialiser une seule fois pour toute la simulation.
rng = np.random.default_rng(42)   #liste d'erreur, faudra enlever !!!!!
ber_cible = 1e-3
bits_emis = rng.integers(0, 2, 1_000_000, dtype=np.uint8)  #liste de 1million de bits de 0 ou 1

#bits_emis = np.array([1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1], dtype=np.uint8)

resultat = erreur.canal_awgn(bits_emis, ber_cible, rng)  
bits_recus = resultat["bits_recus"]

erreurs = np.flatnonzero(bits_emis != bits_recus)

ber_mesure = erreurs.size / bits_emis.size


print(f"Sigma : {resultat['sigma']:.6f}")
print(f"Eb/N0 : {resultat['ebn0_db']:.2f} dB")
print(f"Nombre d'erreurs : {erreurs.size}")
print(f"BER mesure : {ber_mesure:.6f}")

# Zoom sur 60 bits autour de la premiere erreur.
largeur = min(60, bits_emis.size)
centre = int(erreurs[0]) if erreurs.size else 0
debut = max(0, min(centre - largeur // 2,
                   bits_emis.size - largeur))
fin = debut + largeur
erreurs_visibles = erreurs[
    (erreurs >= debut) & (erreurs < fin)
]
fig, axes = plt.subplots(
    2, 1, figsize=(12, 5), sharex=True, layout="constrained"
)
for ax, bits, titre, couleur in zip(
    axes,
    [bits_emis, bits_recus],
    ["Avant : bits emis", "Apres : bits demodules"],
    ["#2063a6", "#16806a"]
):
    ax.stairs(
        bits[debut:fin], np.arange(debut, fin + 1),
        baseline=None, color=couleur, linewidth=2
    )
    for i in erreurs_visibles:
        ax.axvspan(i, i + 1, color="red", alpha=0.15)
    ax.set(title=titre, ylabel="Bit", yticks=[0, 1],
           ylim=(-0.2, 1.2), xlim=(debut, fin))
    ax.grid(axis="y", alpha=0.2)

axes[-1].set_xlabel("Indice du bit - rouge : bit errone")
zoom = ("Zoom autour de la premiere erreur" if erreurs.size
        else "Aucune erreur observee")
fig.suptitle(
    f"AWGN | BER cible : {ber_cible:.3g} | "
    f"BER global mesure : {ber_mesure:.6f}\n{zoom}"
)
plt.savefig("comparaison_binaire_awgn.png", dpi=170)
plt.show()