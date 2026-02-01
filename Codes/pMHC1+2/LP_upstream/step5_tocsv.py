import pandas as pd
import subprocess
import numpy as np
import os, sys
from Functions import make_answer_tag

input_csv = sys.argv[1]
input_csv = os.path.splitext(input_csv)

f = pd.read_csv(input_csv)
PDBs = f["PDB_ID"]

columns =  ['PDB_ID', 'Num', 'Total_energy', 'BackHbond', 'SideHbond', 'Energy_vdw', 'Electro', 'Energy_solvP', 'Energy_solvH', 'Energy_vdwclash', 'Entropy_sidec', 'Entropy_mainc', 'Water_bonds', 'UNK', 'Cis_bond', 'Energy_torsion', 'Backbone_vdwclash', 'Helix_dipole', 'Loop_entropy', 'Disulfide','Kn_electrostatic','Partial_covalent_interactions', 'Energy_ionisation', 'Entropy_complex']

df = pd.DataFrame(np.arange(len(columns)))
df = df.T
df.columns = columns

PDBs = [ele for ele in PDBs if ele != "6DFS"] 

for pdb in PDBs :
    num=0
    f = open(f"{pdb}_1_0_ST.fxout").readlines()
    Optimized = f[-1].replace("\n", "")
    Optimized = Optimized.split('\t')
    print(Optimized)
    print(len(Optimized), len(columns)) 
    result = [pdb,num] + Optimized[1:-1]
    df.loc[len(df)] = result

result = df.iloc[1:,:]
Finish = result.to_csv("MHC2_negative_result1.csv")
