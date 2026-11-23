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
# we are using Hamming method also known as forward error correction (FEC for short)
# it is important to note that Hamming's method can only correct up to 1 error. Because of this 
# we will test other methods such as the LDPC method

# this sequence of codes takes a list of 4 bits as argument.
def get_parity_bits(bit):
    bit0=(bit[2]+bit[1]+bit[0])%2
    bit1=(bit[3]+bit[1]+bit[0])%2
    bit2=(bit[3]+bit[2]+bit[0])%2
    return [bit2,bit1,bit0]
# from the sequence of 4 bits we can generate parity bits ( they are basically the control bits 
# for our sequence of 4 bits in order to locate the error)

def matrix_builder(bit_list, N=4): #has to be 4 bits
    if len(bit_list)!=N:
        raise ValueError("bit_list must be equal to 4")
    parity_bits=get_parity_bits((bit_list[3],bit_list[2],bit_list[1],bit_list[0]))
    codeword=list(bit_list)+parity_bits
    return np.array(codeword).reshape(1,7)

def generator_matrix():
    identity_matrix=np.identity(4)
    rows=[list(row)+get_parity_bits(row) for row in identity_matrix]
    return np.array(rows)
# the generator matrix is a universal matrix used to encode any sequence of four bits

def code_word(generator_matrix, codeword):
    return (codeword@generator_matrix)%2
# in order to generate the codeword, all we have to do is multiply the original sequence of 4 bits
# with the generator matrix


# the following is a blueprint on how you can test the codes and were used to debug 
u=matrix_builder((1,1,0,1),4)
print(u)
G=generator_matrix()
G_T=G.T
print(G_T)
t= code_word(G_T,u)
print(t)

###DECODER HAMMING
# this part will need the coded message to be provided as a list of 7 characters
import numpy as np
def solver_matrix():
    l=[1,1,0,1,1,0,0,
     1,0,1,1,0,1,0,
     0,1,1,1,0,0,1]
    return np.array(l).reshape(3,7)
# you need to give as an argument the transposed matrix since 
# the previous function only gives you H that is not transposed
# this function computes the symptom, the symptom is used to locate and detect the errors in our received message
def symptom_calculator(c,H_transposed):
    print(H_transposed)
    return (c@H_transposed)%2 
# from the symptom, we can find which bit is wrong by multiplying the received message of 7 bits with the transposed matrix H
# if the syndrome is zero, all three parity equations are satisfied, and therefore means there is no error
# when the symprom is different to zero, an error has occured. Because this is a linear code, the syndrome 
# only depends on the error vector. Thus, we are able to locate the error.
def error_detector(s,c):
    error_pos=None
    if s[0]==0:
        if s[1]==0:
            if s[2]==0:
                error_pos=None
            else:
                error_pos=0
        else:
            if s[2]==0:
                error_pos=1
            else:
                error_pos=4
    else:
        if s[1]==0:
            if s[2]==0:
                error_pos=2
            else:
                error_pos=5
        else:
            if s[2]==0:
                error_pos=6
            else:
                error_pos=3
    if error_pos!=None:
        for i in range(len(c)):
            if i ==error_pos:
                value=c.pop(i)
                if value==1:
                    c.insert(i,0)
                else:
                    c.insert(i,1)
    return c
# the corrector function is only used if there is an actual error that needs to be corrected
def corrector(pos_error,c):
    newlist=[]
    for i in range(len(c)-3):
        if i==pos_error:
            if c[i]==0:
                newlist.append(1)
            else:
                newlist.append(0)
        else:
            newlist.append(c[i])
    return newlist
# this function is only used if there is no error to correct 
def stripper(codeword):
    newl=[]
    for i in range(len(codeword)-3):
        newl.append(codeword[i])
    return newl
# blueprint to test code (was also used to debug)
c=[1,1,0,1,1,0,0]
H=solver_matrix()
#print(H)
#print(H.T)
symptom=symptom_calculator(c, H.T)
print(symptom)
error_position=error_detector(symptom, c)
print(error_position)
if type(error_position)==int:
    corrected_message=corrector(error_position,c)
else:
    corrected_message=stripper(c)     
print(corrected_message)

