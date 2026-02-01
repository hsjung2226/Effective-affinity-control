import sys
import subprocess
import pandas as pd

f = pd.read_csv("TCRpMHC2_mut.csv")
PDBs = f["PDB_ID"]

num=int(sys.argv[1])
pdb=PDBs[num]

print(pdb)
Path="/data2/2226jhs/foldx_20251231"

subprocess.call(f"python3 iter_optimize.py {pdb}_trimmed.pdb", shell=True)
subprocess.call(f"python3 iter_optimize.py {pdb}_1_trimmed.pdb", shell=True)
