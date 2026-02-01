import pandas as pd

def pMHC1_final_csv(combination):
    binder = pd.read_csv("pMHC1_positive.csv")
    binder_result = binder.iloc[:, [1]+combination]

    non_binder = pd.read_csv("pMHC1_negative.csv")
    non_binder_result = non_binder.iloc[:, [1]+combination]

    out1 = binder_result.to_csv("pMHC1_binder.csv")
    out2 = non_binder_result.to_csv("pMHC1_non_binder.csv")

