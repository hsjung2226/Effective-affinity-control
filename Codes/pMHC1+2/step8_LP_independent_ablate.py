import pandas as pd
import numpy as np
import sys
from step0_Dependent_Trial import *
from step9_final_csv import final_csv
from step10_negative_test import negative_test
from step11_positive_test import positive_test
import itertools
from itertools import combinations
from collections import defaultdict

merged_csv = sys.argv[1]
binder_csv = sys.argv[2]
non_binder_csv = sys.argv[3]
MHC_type = sys.argv[4]

Raw_data = pd.read_csv(f"{merged_csv}.csv")
omega_data = Raw_data.drop(columns="Total_energy", axis=1)

def test(combination, binder_csv, non_binder_csv, MHC_type) :
    target_filt=[]
    All_results = Dependent_Trial(Meta_data, combination)
    for dic in All_results :
        if dic["min_value"] != 0 and dic["min_value"] < -1e-3 :
            target_filt.append(dic)

    coef=[]
    for num in range(1, len(combination)+1) :
        coef.append(target_filt[-1][f"x{num}"])

    makecsv = final_csv(combination, binder_csv, non_binder_csv, MHC_type)
    CBEs, NBEs, negative = negative_test(coef, combination, MHC_type)
    
    if not int(MHC_type) == 1 :
        CBEs, WBEs, positive = positive_test(coef, combination, MHC_type)

        return CBEs, NBEs, WBEs, coef, negative, positive
    
    else :
        return CBEs, NBEs, coef, negative

result={}
for cnt in range(100):
    combination = [5,7,9,20]
    PDBs = list(dict.fromkeys(omega_data["PDB_ID"].tolist()))

    shuffled = np.random.permutation(PDBs)
    Ablated = shuffled[:int(len(shuffled)/5)]
    Meta_data = omega_data[~omega_data["PDB_ID"].isin(Ablated)]

    _,_,coef, negative = test(list(combination), binder_csv, non_binder_csv, MHC_type)
    result[cnt]=[coef, negative]

print (result)
