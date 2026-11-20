#%%
import math

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

def encode_dic(codes, DEBUG=False):
    # Format :
    # [nombre d'entrees : 16 bits]
    # puis pour chaque lettre :
    #   [lettre en UTF-8 : 8 a 32 bits] [longueur du code : 8 bits] [code]
    bits = format(len(codes),  "016b")   # entier > binaire sur 16 bits

    for key, value in codes.items():
        # La lettre en UTF-8 : chaque octet ecrit sur 8 bits
        letter_bits = ""
        for byte in key.encode("utf-8"):
            letter_bits = letter_bits + format(byte, "08b")

        # La longueur du code sur 8 bits, puis le code lui-meme
        length_bits = format(len(value), "08b")

        bits = bits + letter_bits + length_bits + value
        if DEBUG:
            print(key, letter_bits, length_bits, value)

    return bits

def encode_text(file, codes, DEBUG=False):
    # On remplace chaque lettre du texte par son code Huffman
    bits = ""
    with open(file,"r",encoding="utf-8") as f:
        for l in f:
            for c in l:
                bits = bits + codes[c]
    if DEBUG:
        print(len(bits), "bits pour le texte")
    return bits

def stats(file, DEBUG=False):
    # On fait tourner toute la chaine de compression
    dics = dic_letters_sorted(file)
    codes = huffman_codes(dics)
    dic_bits = encode_dic(codes)
    text_bits = encode_text(file, codes)

    # Taille du fichier original : chaque lettre en UTF-8 (1 a 4 octets)
    nb_letters = sum(dics.values())
    original_bits = 0
    for key, value in dics.items():
        original_bits = original_bits + len(key.encode("utf-8")) * 8 * value

    compressed_bits = len(dic_bits) + len(text_bits)

    # Entropie de Shannon : le minimum theorique de bits par lettre
    entropy = 0
    for value in dics.values():
        p = value / nb_letters
        entropy = entropy - p * math.log2(p)

    # Longueur moyenne d'un code Huffman (pondere par la frequence)
    avg_bits = len(text_bits) / nb_letters

    # Code a longueur fixe : toutes les lettres ont le meme nombre de bits,
    # juste assez pour numeroter les lettres differentes (ex : 100 lettres -> 7 bits)
    fixed_len = math.ceil(math.log2(len(dics)))
    fixed_bits = fixed_len * nb_letters

    s = {
        "utf8_avg": original_bits / nb_letters,
        "fixed_len": fixed_len,
        "fixed_bits": fixed_bits,
        "nb_letters": nb_letters,
        "nb_distinct": len(dics),
        "original_bits": original_bits,
        "dic_bits": len(dic_bits),
        "text_bits": len(text_bits),
        "compressed_bits": compressed_bits,
        "ratio": compressed_bits / original_bits,
        "gain": 1 - compressed_bits / original_bits,
        "entropy": entropy,
        "avg_bits": avg_bits,
        "efficiency": entropy / avg_bits,
    }

    if DEBUG:
        # Les 10 lettres les plus frequentes avec leur code
        print("Top 10 des lettres :")
        for key in list(dics)[:10]:
            print(f"  {key!r:6} {dics[key]:8} fois  {dics[key] / nb_letters:6.2%}  code = {codes[key]}")
    return s

def print_stats(s):
    print(f"Lettres dans le texte    : {s['nb_letters']}")
    print(f"Lettres differentes      : {s['nb_distinct']}")
    print()
    print(f"Taille originale         : {s['original_bits']:>10} bits  ({s['original_bits'] / 8 / 1024:.1f} Ko)")
    print(f"Taille dictionnaire      : {s['dic_bits']:>10} bits  ({s['dic_bits'] / 8 / 1024:.1f} Ko)")
    print(f"Taille texte compresse   : {s['text_bits']:>10} bits  ({s['text_bits'] / 8 / 1024:.1f} Ko)")
    print(f"Taille totale compressee : {s['compressed_bits']:>10} bits  ({s['compressed_bits'] / 8 / 1024:.1f} Ko)")
    print()
    print(f"Taux de compression      : {s['ratio']:.2%} de la taille originale")
    print(f"Gain                     : {s['gain']:.2%}")
    print()
    print(f"Entropie (minimum theo.) : {s['entropy']:.4f} bits/lettre")
    print(f"Longueur moyenne Huffman : {s['avg_bits']:.4f} bits/lettre")
    print(f"Efficacite du code       : {s['efficiency']:.2%}")
    print()
    print("------Comparaison------")
    print(f"{'Codage':<26}{'bits/lettre':>12}{'Taille (Ko)':>13}{'vs UTF-8':>10}")
    lines = [
        ("UTF-8", s["utf8_avg"], s["original_bits"]),
        (f"Longueur fixe ({s['fixed_len']} bits)", s["fixed_len"], s["fixed_bits"]),
        ("Huffman (texte seul)", s["avg_bits"], s["text_bits"]),
        ("Huffman (+ dictionnaire)", s["compressed_bits"] / s["nb_letters"], s["compressed_bits"]),
        ("Entropie (limite theo.)", s["entropy"], s["entropy"] * s["nb_letters"]),
    ]
    for name, per_letter, total in lines:
        print(f"{name:<26}{per_letter:>12.4f}{total / 8 / 1024:>13.1f}{total / s['original_bits']:>10.2%}")

# %%
if __name__ == "__main__":
    print("------Stats------")
    file = input("Saisir File: ")
    print_stats(stats(file, DEBUG=True))
    # %%
