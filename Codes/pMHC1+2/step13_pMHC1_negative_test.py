import pandas as pd
import numpy as np

def pMHC1_negative_test(coef, combination):
    binder = pd.read_csv("pMHC1_binder.csv")
    non_binder = pd.read_csv("pMHC1_non_binder.csv")

    CBEs=[]
    for _, info in binder.iterrows() :
        E=0
        for num in range(len(combination)):
            E += coef[num]*int(info[2+num]) 
        CBEs.append(E)


    NBEs=[]
    for _, info in non_binder.iterrows() :
        E=0
        for num in range(len(combination)):
            E += coef[num]*int(info[2+num])
        NBEs.append(E)

    CBEs = np.array(CBEs)
    NBEs = np.array(NBEs)

    return CBEs, NBEs, np.count_nonzero(CBEs < NBEs)
