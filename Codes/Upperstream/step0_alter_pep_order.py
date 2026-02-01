import pandas as pd
from collections import defaultdict
import subprocess

f = pd.read_csv("pMHC1_TCR_mut2.csv")
data = f[["PDB_ID", "ref_seq", "Chain"]]

items=[]
for _, item in data.iterrows() :
    items.append(item.tolist())

for item in items :
    PDB = item[0]
    ref_seq = item[1]
    Chain = item[2]


    subprocess.call(["pymol2", f"{PDB}.pdb.pdb", "-cq" , "alter_pep_order.py",  "--", f"{PDB}", f"{Chain}"], universal_newlines=True)


    

