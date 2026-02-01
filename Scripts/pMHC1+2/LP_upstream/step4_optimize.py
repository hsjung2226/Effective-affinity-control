import sys
import subprocess
import pandas as pd
import os, sys
from Functions import Check_task, e_compare, iter_optimize

input_csv = sys.argv[1]
input_csv = os.path.splitext(input_csv)

f = pd.read_csv(input_csv)
PDBs = f["PDB_ID"]

num=int(sys.argv[2])
pdb=PDBs[num]

print(pdb)
Path="/data2/2226jhs/foldx_20251231"

iter_optimize(pdb, epoch=1000)

generated = check_task(pdb, task="Mutation")
print(f"{generateg} Mutations are made for {pdb}")
