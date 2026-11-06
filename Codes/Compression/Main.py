#%%
def dic_letters_sorted(file, DEBUG=False):
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

def huffman_codes(dics, DEBUG=False):
    # Un groupe = [poids, {lettre: code}]
    # Au debut, chaque lettre est seule dans son groupe, avec un code vide
    groups = []
    for key, value in dics.items():
        groups.append([value, {key: ""}])

    # On fusionne les 2 groupes les plus legers jusqu'a n'en avoir plus qu'un
    while len(groups) > 1:
        groups = sorted(groups, key=lambda item: item[0])
        left = groups.pop(0)    # le plus leger
        right = groups.pop(0)   # le 2e plus leger

        new_codes = {}
        # "0" devant le code de toutes les lettres du groupe de gauche
        for letter in left[1]:
            new_codes[letter] = "0" + left[1][letter]
        # "1" devant le code de toutes les lettres du groupe de droite
        for letter in right[1]:
            new_codes[letter] = "1" + right[1][letter]

        # On remet le nouveau groupe dans la liste
        groups.append([left[0] + right[0], new_codes])
        if DEBUG:
            print("fusion", left[0], "+", right[0], "=", left[0] + right[0])

    # Il ne reste qu'un groupe : son dictionnaire contient tous les codes
    codes = groups[0][1]
    if DEBUG:
        for key, value in codes.items():
            print(repr(key), dics[key], value)
    return codes
def Encode_dic(code, Debug=False):
    for key value 
# %%
file = "/Users/aleksi/Desktop/Projet/GrandProjetCommunication_WP4/INPUT/La_Peste_CAMUS"
dics = dic_letters_sorted(file)
codes = huffman_codes(dics, DEBUG=True)
print(codes)
# %%
