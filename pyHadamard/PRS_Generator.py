from numpy import *
import operator

'''Maximal Length Psuedo Random Sequence Generator
Brian H. Clowers, August 16, 2007
Description:  This script returns an array consisting of 0's and 1's in a
pseudo random sequence (prs) as defined by Harwitt and Sloane.
Each sequence is determined by using a primitive binary polynomial.
For additional detail see their book entitled: Hadamard Transform Optics,
Academic Press, NY, 1979.  The appendix contains an in depth discussion
of the topic.
'''

def Sequence_Generator(bit_shift):
    sequence_length=2**bit_shift - 1
    prs_1D=zeros(sequence_length, dtype=int)
    prs_1D[bit_shift-1]=1 ## initialize the correct element
    
    for i in range(bit_shift, sequence_length,1):

        prs_1D[i]= {
            
            3:  lambda: operator.xor(prs_1D[i-bit_shift],prs_1D[i - bit_shift + 1]),
            
            4:  lambda: operator.xor(prs_1D[i-bit_shift],prs_1D[i - bit_shift + 1]),
            
            5:  lambda: operator.xor(prs_1D[i-bit_shift],prs_1D[i - bit_shift + 2]),
            
            6:  lambda: operator.xor(prs_1D[i-bit_shift],prs_1D[i - bit_shift + 1]),
            
            7:  lambda: operator.xor(prs_1D[i-bit_shift],prs_1D[i - bit_shift + 1]),
            
            8:  lambda: operator.xor(prs_1D[i-bit_shift],operator.xor(prs_1D[i - bit_shift + 1],
                       operator.xor(prs_1D[i - bit_shift + 5],prs_1D[i - bit_shift + 6]))),
            
            9:  lambda: operator.xor(prs_1D[i-bit_shift],prs_1D[i - bit_shift + 4]),
            
            10: lambda: operator.xor(prs_1D[i-bit_shift],prs_1D[i - bit_shift + 3]),
            
            11: lambda: operator.xor(prs_1D[i-bit_shift],prs_1D[i - bit_shift + 2]),
            
            12: lambda: operator.xor(prs_1D[i-bit_shift],operator.xor(prs_1D[i - bit_shift + 3],
                        operator.xor(prs_1D[i - bit_shift + 4],prs_1D[i - bit_shift + 7]))),
            
            13: lambda: operator.xor(prs_1D[i - bit_shift], operator.xor(prs_1D[i - bit_shift + 1],
                        operator.xor(prs_1D[i - bit_shift + 3],prs_1D[i - bit_shift + 4]))),
            
            14: lambda: operator.xor(prs_1D[i - bit_shift], operator.xor(prs_1D[i - bit_shift +1],
                        operator.xor(prs_1D[i - bit_shift + 11], prs_1D[i - bit_shift + 12]))),
            
            15: lambda: operator.xor(prs_1D[i-bit_shift],prs_1D[i - bit_shift + 1]),
            
            16: lambda: operator.xor(prs_1D[i - bit_shift], operator.xor(prs_1D[i - bit_shift + 2],
                        operator.xor(prs_1D[i - bit_shift + 3], prs_1D[i - bit_shift + 5]))),
            
            17: lambda: operator.xor(prs_1D[i-bit_shift],prs_1D[i - bit_shift + 3]),
            
            18: lambda: operator.xor(prs_1D[i-bit_shift],prs_1D[i - bit_shift + 7]),
            
            19: lambda: operator.xor(prs_1D[i - bit_shift], operator.xor(prs_1D[i - bit_shift + 1],
                        operator.xor(prs_1D[i - bit_shift + 5], prs_1D[i - bit_shift + 6]))),
            
            20: lambda: operator.xor(prs_1D[i-bit_shift],prs_1D[i - bit_shift + 3]),

        } [bit_shift]()

    return prs_1D
        

'''Generates and oversampled data prs according to the method described by
Clowers and Belov.'''

def Generate_Oversampled_PRS(bit_shift, oversampling):
    sl=2**bit_shift-1 ##sl=sequence length
    osl=sl*oversampling ##osl=oversampling length
    prs_os=zeros(osl, dtype=int)
    prs=Sequence_Generator(bit_shift)
    n=0
    for i in range(0,osl-1,1):
        if(i%(oversampling)==0):
            prs_os[i+(oversampling-1)]=prs[n]
            n+=1
    #print n
    return prs_os


