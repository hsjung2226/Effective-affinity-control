import pandas as pd
import numpy as np


f = pd.read_csv("TCRpMHC1_merged.csv",index_col=0)
f = f[f["Is_Answer"] == 0]
f = f.reset_index(drop=True)
out = f.to_csv("TCRpMHC1_negative.csv")
