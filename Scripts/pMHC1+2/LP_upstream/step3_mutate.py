import pandas as pd
import subprocess
import sys
import os, sys
from Functions import Check_task

input_csv = sys.argv[1]
input_csv = os.path.splitext(input_csv)

f = pd.read_csv(input_csv)
pd.set_option('mode.chained_assignment',  None)

PDBs = f["PDB_ID"]

num=int(sys.argv[2])
pdb = PDBs[num]


Path="/data2/2226jhs/foldx_20251231"
subprocess.call(f"{Path} --command=BuildModel --pdb={pdb.upper()}.pdb --mutant-file=individual_list_{pdb}.txt", shell=True)

generated = check_task(pdb, task="Mutation")

print(f"{generateg} Mutations are made for {pdb}")
