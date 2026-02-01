import pandas as pd

binder= pd.read_csv("pMHC1_positive.csv")
non_binder= pd.read_csv("pMHC1_negative.csv")

merged = pd.concat([binder,non_binder], axis=0).drop(columns=['Unnamed: 0'], errors='ignore')
merged = merged.sort_index()

finish = merged.to_csv("pMHC1_merged.csv")
