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
###CODAGE HAMMING 

import numpy as np
def get_parity_bits(bit):
    bit0=(bit[2]+bit[1]+bit[0])%2
    bit1=(bit[3]+bit[1]+bit[0])%2
    bit2=(bit[3]+bit[2]+bit[0])%2
    return [bit2,bit1,bit0]

def matrix_builder(bit_list, N=4): #has to be 4 bits
    if len(bit_list)!=N:
        raise ValueError("bit_list must be equal to 4")
    parity_bits=get_parity_bits((bit_list[0],bit_list[1],bit_list[2],bit_list[3]))
    codeword=list(bit_list)+parity_bits
    return np.array(codeword).reshape(1,7)

def generator_matrix():
    identity_matrix=np.identity(4)
    rows=[list(row)+get_parity_bits(row) for row in identity_matrix]
    return np.array(rows)

def code_word(generator_matrix, codeword):
    return (codeword@generator_matrix)%2

