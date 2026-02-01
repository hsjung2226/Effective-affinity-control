import pandas as pd
from collections import defaultdict
import subprocess

f = pd.read_csv("pMHC1_TCR_mut.csv")
data = f[["PDB_ID", "ref_seq", "mut_seq"]]

items=[]
for _, item in data.iterrows() :
    items.append(item.tolist())

dd_item = defaultdict(list)
for item in items :
    PDB = item[0]
    ref_seq = item[1]
    mut_seq = item[2]
    
    dd_item[PDB].append(ref_seq)
    dd_item[PDB].append(mut_seq)

    out = subprocess.check_output(["pymol2", f"{PDB}.pdb.pdb", "-cq" , "fetch_peptide_chain.py",  "--", f"{ref_seq}"], universal_newlines=True)
    print(ref_seq, out)
    chain = out.strip().split("\n")[-1]


    dd_item[PDB].append(chain)
    

print(dd_item)

PEP_pdb = pd.DataFrame(dd_item).T
PEP_pdb["PDB_ID"] = PEP_pdb.index
PEP_pdb.columns = ["ref_seq", "mut_seq", "Chain", "PDB_ID"]
PEP_pdb = PEP_pdb[["Chain", "ref_seq", "mut_seq", "PDB_ID"]]

out=PEP_pdb.to_csv("pMHC1_TCR_mut2.csv")


