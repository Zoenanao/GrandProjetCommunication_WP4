#%%
def dic_letters_sorted(file):
    dic={}
    with open(file,"r",encoding="utf-8") as f:
        for l in f:
            for c in l:
                if c in dic:
                    dic[c]=dic[c]+1
                else:
                    dic[c]=1
    dics = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True))
    return dics 

def tree_generation(dics):
    dec = {}
    for key, value in dics.items():
        dec[key]="1
    
# %%
# taille de la trame :
b = 256

def parseuse(matrix):
    # passage de matrice en liste
    bits = matrix.flatten().tolist()
    
    # nombre de trames (arrondi vers le haut)
    part = len(bits) // b
    if len(bits) % b != 0:
        part += 1
        
    #creation d'un dictionnaire qui contient les trames
    tram = dict()
    for n in range(part):
        # tranche de b bits correspondant à cette trame
        morceau = bits[n * b : (n + 1) * b]

        # on complète avec des 0 si la dernière trame est trop courte
        while len(morceau) < b:
            morceau.append(0)

        tram[n + 1] = morceau

    return tram
