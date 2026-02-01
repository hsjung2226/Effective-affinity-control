import sys
import subprocess
import pandas as pd
import numpy as np

PDBs=['1oga', '5brz', '4ms8', '5jzi', '5sws', '1qse', '5bs0', '3mv8', '5jhd', '3ffc', '3o4l', '6am5', '6eqa', '4mnq', '5hho', '6avg', '6rsy', '4mji', '5eu6', '1mwa', '7jwi', '5c08', '3hg1', '4nhu', '3rgv', '1qrn', '2vlj', '4prh', '6vqo', '6rpa', '5m00', '5nmf', '5m02', '5tje', '5c07', '3uts', '5e6i', '2p5e', '2f54', '3d3v', '2f53', '6g9q', '6l9l', '2j8u', '5hyj', '6vrn', '2e7l', '2p5w', '6uon', '4ftv', '5tez', '5euo', '5til', '3qdj', '3tpu', '5wkh', '7n1f', '5hhm', '3utt', '3mv9', '2ol3', '3qdm', '3vxm', '4n0c', '4eup', '5nht', '4mvb', '5nqk', '5wlg', '1bd2', '4g9f', '5c0c', '3qeq', '6avf', '2uwe', '3vxr', '7jwj', '2pye', '2oi9', '5c0b', '6mtm', '2bnq', '7n1e', '4qok', '4pri', '2gj6', '1lp9', '1nam', '2vlr', '6bj2', '2vlk', '5e9d', '1mi5', '6d78', '4jry', '5isz', '5c09', '3qdg', '4l3e', '5men', '5yxn', '4prp', '6vrm', '1kj2', '3pqy', '3pwp', '1g6r', '3kpr', '5d2l', '1ao7', '2ypl', '3gsn', '5nme', '5nmg', '3dxa', '6rp9', '3kxf', '1fo0', '3tjh', '5ivx', '4mxq', '6dkp', '3sjv', '4n5e', '5d2n', '5c0a', '3qfj', '5wkf', '3tfk', '6rpb', '6q3s', '4qrp', '3mv7', '2ak4', '3tf7', '7n6e', '3d39', '2bnr', '3e2h', '6amu', '3h9s', '4g8g', '6tro', '2jcc', '5yxu', '6vmx', '5m01', '1qsf', '3kps', '3vxs', '2ckb', '3e3q', '4jrx']


f = open(f"Interaction_6d78_1_trimmed_AC.fxout", "r").readlines()
columns=f[-2].replace("\n", "").split("\t")
columns+=["Is_Answer"]


def tocsv(PDBs, columns):
    df = pd.DataFrame(np.arange(len(columns)))
    df = df.T
    df.columns = columns

    for pdb in PDBs :

        f = open(f"Interaction_{pdb}_trimmed_AC.fxout").readlines()
        result1 = f[-1].replace("\n", "").split("\t") + [1] 


        f = open(f"Interaction_{pdb}_1_trimmed_AC.fxout").readlines()
        result2 = f[-1].replace("\n", "").split("\t") + [0] 
        
        df.loc[len(df)] = result1
        df.loc[len(df)] = result2

    return df.iloc[1:,:]



result = tocsv(PDBs,columns)
Finish = result.to_csv("TCRpMHC1_Int.csv")

