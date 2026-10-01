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
        dec[key]="1"
    
# %%
