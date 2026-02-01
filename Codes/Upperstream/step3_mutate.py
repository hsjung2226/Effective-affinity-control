import pandas as pd
import subprocess
import sys
pd.set_option('mode.chained_assignment',  None)


f = pd.read_csv("pMHC1_TCR_mut2.csv",encoding='ISO-8859-1')
PDBs = f["PDB_ID"]

num=int(sys.argv[1])
pdb=PDBs[num]
print(pdb)

Path="/data2/2226jhs/foldx_20251231"
subprocess.call(f"{Path} --command=BuildModel --pdb={pdb}.pdb --mutant-file=individual_list_{pdb}.txt", shell=True)
