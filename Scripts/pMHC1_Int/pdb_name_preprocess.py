import pandas as pd

f1 = pd.read_csv("pMHC1_Int_merged.csv")
f2 = pd.read_csv("pMHC1_Int_positive.csv")
f3 = pd.read_csv("pMHC1_Int_negative.csv")

def trim (name):
    name = name.split("/")[1].split("_")[0]
    return name

f1["Pdb"] = f1["Pdb"].apply(trim)
f2["Pdb"] = f2["Pdb"].apply(trim)
f3["Pdb"] = f3["Pdb"].apply(trim)

f1 = f1.loc[:, ~f1.columns.str.contains('^Unnamed: 0')]
f2 = f2.loc[:, ~f2.columns.str.contains('^Unnamed: 0')]
f3 = f3.loc[:, ~f3.columns.str.contains('^Unnamed: 0')]

out1=f1.to_csv("pMHC1_merged.csv")
out2=f2.to_csv("pMHC1_positive.csv")
out3=f3.to_csv("pMHC1_negative.csv")

