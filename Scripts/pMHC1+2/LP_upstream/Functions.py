import re
import pandas as pd
import numpy as np
from collections import defaultdict
import subprocess
import os, sys, shutil
from Pymol_functions import fetchseq

def fetch_sequence(input_csv):

    f = pd.read_csv(input_csv)
    data = f[["IMGT entry ID", "Chain Peptide ID"]]

    items=[]
    for _, item in data.iterrows() :
        items.append(item.tolist())

    dd_item = defaultdict(list)
    for item in items :
        PDB = item[0].upper()
        Chain = item[1]
        dd_item[PDB].append(Chain)

        out = subprocess.check_output(["pymol2", f"{PDB}.pdb", "-cq" , "PymolScript_fetchseq.py",  "--", f" {Chain}"], universal_newlines=True)
        seq = out.strip().split("\n")[-1]


        dd_item[PDB].append(seq)
        


    df_out = pd.DataFrame(dd_item).T
    df_out.columns = ["Chain", "PEPTIDE(pdb)"]

    return df_out

def make_mutation_list(f):

    pd.set_option('mode.chained_assignment',  None)

    def find_mismatch(Ref, Mut, chain):
        mismatches=[]
        for index, (m, n) in enumerate(list(zip(Ref,Mut))):
            if m != n :
                mismatches.append(f"{m}{chain}{index+1}{n}")

        return mismatches

    def mutate(data):
        chain = data.iloc[0,1]
        Ref = data.iloc[0,2]
        Mut = data.iloc[0,3]
        
        mismatches = find_mismatch(Ref, Mut, chain)

        return ",".join(mismatches)


    PDBs = list(dict.fromkeys(f["PDB_ID"]))

    for pdb in PDBs :
        target = f[f["PDB_ID"] == pdb]
        mismatches = mutate(target)
        
        m = open(f"individual_list_{pdb}.txt", "a")
        m.write(mismatches + ";\n")
        m.close()

def e_compare(f, n):
    e_cut = 0.05
    content = open(f).readlines()
    after_e = float(content[-1].split()[0])
    before_e = float(content[-3].split()[0])
    diff = before_e - after_e
    print(f"Iteration:: {n}, Before: {before_e}, After: {after_e}, Diff: {diff}")
    if diff < e_cut:
        return True
    else:
        return False



def iter_optimize(pdb, epoch=True):
    
    path="/data2/2226jhs/foldx_20251231"

    foldx_cmd = f"{path} --command=Optimize --pdb={pdb}"

    basename = os.path.splitext(pdb)[0]
    output_pdb = "Optimized_%s.pdb"%basename
    fxout = "OP_%s.fxout"%basename

    c = 1
    while epoch:
        os.popen(foldx_cmd).read()
        stop_condition = e_compare(fxout, c)
        shutil.move(output_pdb, pdb)
        #os.remove(output_pdb)
        os.remove(fxout)
        if stop_condition:
            print("Stopped!")
            break
        else:
            c += 1

    foldx_stability = f"{path} --command=Stability --pdb={pdb}"
    os.system(foldx_stability)


def Check(pdb, task) :

    if task == "Optimization" :
        out=subprocess.call(f"find . -name 'OP_{pdb.upper()}.fxout' | wc -l > optimized_{pdb}.txt", shell=True)    
    if task == "Mutation" :
        out = subprocess.check_output(f"find . -name '{pdb.upper()}_*.pdb' | wc -l > mutated_{pdb}.txt", shell=True)
    

    return out


