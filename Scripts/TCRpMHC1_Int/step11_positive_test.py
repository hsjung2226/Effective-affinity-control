import pandas as pd
import numpy as np

def positive_test(coef, combination, MHC_type):
    correct_binder = pd.read_csv(f"correct_binder_MHC{MHC_type}.csv")
    wrong_binder = pd.read_csv(f"wrong_binder_MHC{MHC_type}.csv")


    CBEs=[]
    for _, info in correct_binder.iterrows() :
        E=0
        for num in range(len(combination)):
            E += coef[num]*int(info[2+num]) 
        CBEs.append(E)


    PDBs = correct_binder["PDB_ID"].tolist()
    WBEs=[]

    for pdb in PDBs:
        temp=10000000000000000000
        target_data = wrong_binder.query(f"PDB_ID == '{pdb}'")
        for _, info in target_data.iterrows() :
            E += coef[num]*int(info[2+num]) 
 
            if E < temp :
                temp=E
        WBEs.append(temp)

    CBEs = np.array(CBEs)
    WBEs = np.array(WBEs)


    return CBEs, WBEs, np.count_nonzero(CBEs < WBEs)
