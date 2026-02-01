import pandas as pd
import subprocess
import os, sys

input_csv = sys.argv[1]
input_csv = os.path.splitext(input_csv)

f = pd.read_csv(input_csv)


prev = f.columns.tolist()
prev[0] = "PDB"
f.columns = prev

PDBs = f["PDB"]
PDBs = set(PDBs.tolist())

for pdb in PDBs :
    print(subprocess.call([f"python3 getpdb.py {pdb}"], shell=True)) 
