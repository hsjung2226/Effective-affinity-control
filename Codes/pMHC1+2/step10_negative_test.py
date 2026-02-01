import pandas as pd
import numpy as np

def negative_test(coef, combination, MHC_type):
    correct_binder = pd.read_csv(f"correct_binder_MHC{MHC_type}.csv")
    correct_binder = correct_binder[~correct_binder["PDB_ID"].isin(["6DFS"])]

    non_binder = pd.read_csv(f"non_binder_MHC{MHC_type}.csv")

    CBEs=[]
    for _, info in correct_binder.iterrows() :
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
