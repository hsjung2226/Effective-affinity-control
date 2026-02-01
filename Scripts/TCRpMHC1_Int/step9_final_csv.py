import pandas as pd

def final_csv(combination, binder_csv, non_binder_csv, MHC_type):
    binder = pd.read_csv(f"{binder_csv}.csv")

    correct_binder = binder[binder["Is_Answer"] == 1]
    wrong_binder = binder[binder["Is_Answer"] == 0]

    correct_binder_result = correct_binder.iloc[:, [1]+combination]
    wrong_binder_result = wrong_binder.iloc[:, [1]+combination]

    non_binder = pd.read_csv(f"{non_binder_csv}.csv")

    non_binder_result = non_binder.iloc[:, [1]+combination]

    out1 = correct_binder_result.to_csv(f"correct_binder_MHC{MHC_type}.csv")
    out2 = wrong_binder_result.to_csv(f"wrong_binder_MHC{MHC_type}.csv")

    out3 = non_binder_result.to_csv(f"non_binder_MHC{MHC_type}.csv")

