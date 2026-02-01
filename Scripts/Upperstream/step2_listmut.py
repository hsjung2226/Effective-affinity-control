import pandas as pd
import subprocess
import re

pd.set_option('mode.chained_assignment',  None)


f = pd.read_csv("pMHC1_TCR_mut2.csv",encoding='ISO-8859-1')

def find_mismatch(Ref, Mut, chain):
    mismatches=[]
    for index, (m, n) in enumerate(list(zip(Ref,Mut))):
        if m != n :
            mismatches.append(f"{m}{chain}{index+1}{n}")

    return mismatches

def mutation(data):
    chain = data.iloc[0,1]
    Ref = data.iloc[0,2]
    Mut = data.iloc[0,3]
    
    mismatches = find_mismatch(Ref, Mut, chain)

    return ",".join(mismatches)


PDBs = f["PDB_ID"]

for pdb in PDBs :
    target = f[f["PDB_ID"] == pdb]
    mismatches = mutation(target)
    print(mismatches)
    m = open(f"individual_list_{pdb}.txt", "a")
    m.write(mismatches + ";\n")
    m.close()


