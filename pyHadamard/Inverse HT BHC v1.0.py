from numpy import *
from PRS_Generator import *
from Simple_IMS_Plot import *
from Simple_IMS_Plot import get_IMS_ascii

def Generate_Inverse_Sequence(prs):##prs=pseudo random sequence
    ##sl=sequence length of the PRS
    sl=len(prs)
    inv_prs=zeros(sl*2, float)
    ##wf=weighting factor for inverse transform
    wf=2/(float(sl)+1)
    print wf
    for i in range(sl):
        if(prs[i]==0):
            inv_prs[i]=-1*wf
            inv_prs[i+sl]=-1*wf
        elif(prs[i]>0):
            inv_prs[i]=1*wf
            inv_prs[i+sl]=1*wf

    return inv_prs


'''Samples an oversampled data set and places the individual sets in
the appropriate column for future transformation'''

def Sample_OS_Data_Vector(sl,os,os_raw_data):##sl=prs length, os=oversampling
    parsed_raw_data=zeros((os,sl), float)##creates a 20 by 31 array
    for i in range(sl):
        for n in range(os):
            parsed_raw_data[n,i]=os_raw_data[((i*os)+n)]

    return parsed_raw_data



def Inverse_Transform_1D(raw_data, bit_shift, os):
    sl=(2**bit_shift)-1
    HT_result=zeros(sl*os, float)
    temp_inv_vector=zeros(sl, float)
    parsed_raw_data=Sample_OS_Data_Vector(sl,os,raw_data)
    inv_prs=Generate_Inverse_Sequence(Sequence_Generator(bit_shift))
    for i in range(os):
        temp_raw_data=parsed_raw_data[i,:]##selects just a single column of the parsed array
        for j in range(sl):
            start_point=sl-j
            for k in range(sl):
                temp_inv_vector[k]=inv_prs[start_point+k]

            HT_result[((j*os)+i)]=dot(temp_inv_vector,temp_raw_data)
                
    return HT_result
