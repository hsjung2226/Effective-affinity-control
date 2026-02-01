import pandas as pd
import numpy as np


f = pd.read_csv("MHC2_negative_result1.csv")
f["Is_Answer"] = np.zeros_like(np.arange(len(f)))

f = f.loc[:, ~f.columns.str.contains('^Unnamed')]

cols = list(f.columns)

if 'Is_Answer' in cols:
    cols.remove('Is_Answer')
    f = f[cols[:2] + ['Is_Answer'] + cols[2:]]
else:
    print("'Is_Answer' 컬럼이 없습니다.")


out = f.to_csv("MHC2_negative.csv")
