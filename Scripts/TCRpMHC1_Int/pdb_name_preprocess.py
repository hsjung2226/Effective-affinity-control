import pandas as pd

f1 = pd.read_csv("TCRpMHC1_Int.csv")
f3 = pd.read_csv("TCRpMHC1_negative.csv")

def trim (name):
    name = name.split("/")[1].split("_")[0]
    return name

f1["Pdb"] = f1["Pdb"].apply(trim)
f3["Pdb"] = f3["Pdb"].apply(trim)

f1 = f1.loc[:, ~f1.columns.str.contains('^Unnamed: 0')]
f3 = f3.loc[:, ~f3.columns.str.contains('^Unnamed: 0')]

out1=f1.to_csv("TCRpMHC1_Int.csv")
out3=f3.to_csv("TCRpMHC1_negative.csv")

