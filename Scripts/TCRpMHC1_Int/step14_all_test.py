import pandas as pd
import numpy as np
from step0_Dependent_Trial import *
from step9_final_csv import final_csv
from step10_negative_test import negative_test
from step11_positive_test import positive_test
import itertools
from itertools import combinations
from collections import defaultdict
from step12_pMHC1_final_csv import pMHC1_final_csv
from step13_pMHC1_negative_test import pMHC1_negative_test 


Raw_data = pd.read_csv("MHC2_merged.csv")
Meta_data = Raw_data[~Raw_data["PDB_ID"].isin(["6DFS"])]
Meta_data = Meta_data.drop("Total_energy", axis=1)

def pMHC2_test(combination) :
    target_filt=[]
    All_results = Dependent_Trial(Meta_data, combination)
    for dic in All_results :
        if dic["min_value"] != 0 and dic["min_value"] < -1e-3 :
            target_filt.append(dic)

    coef=[]
    for num in range(1, len(combination)+1) :
        coef.append(target_filt[-1][f"x{num}"])

    makecsv = final_csv(combination)
    CBEs, NBEs, negative = negative_test(coef, combination)
    CBEs, WBEs, positive = positive_test(coef, combination)

    return CBEs, NBEs, WBEs, coef, negative, positive

def pMHC1_test(coef, combination):
    makecsv = pMHC1_final_csv(combination)
    _,_,pMHC1_negative = pMHC1_negative_test(coef, combination)

    return pMHC1_negative



result={}
for combination in [[6,11],[8,11],[9,11],[6,11,16,21],[7,9,11,23],[6,7,8,11,21],[7,8,11,16,23],[7,9,11,12,21],[8,11,16,21,23]]:
    _,_,_,coef, negative,positive = pMHC2_test(list(combination))
    pMHC1_negative = pMHC1_test(coef, list(combination))

    result[tuple(combination)]=[coef, negative, positive, pMHC1_negative]

for _ in range(100):
    for combination in [[6,11],[8,11],[9,11],[6,11,16,21],[7,9,11,23],[6,7,8,11,21],[7,8,11,16,23],[7,9,11,12,21],[8,11,16,21,23]]:
        _,_,_,coef, negative,positive = pMHC2_test(list(combination))
        pMHC1_negative = pMHC1_test(coef, list(combination))
        if negative > 67 and positive > 62 and pMHC1_negative > result[tuple(combination)][-1] :
            result[tuple(combination)]=[coef, negative, positive, pMHC1_negative]
     
print (result)
