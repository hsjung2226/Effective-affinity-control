import pandas as pd
import numpy as np
import subprocess
import re
import os, sys
import glob, shutil
import json
from collections import defaultdict
from Functions import fetch_sequence, make_mutation_list

input_object = sys.argv[1]

input_csv = sys.argv[2]
input_csv = os.path.splitext(input_csv)

pd.set_option('mode.chained_assignment',  None)

def Ab_preprocess(text):
    pattern = re.compile(r'[a-z]')
    result = pattern.sub("", text)

def Ab_mutate(string_):
    muts = string_.split(",")
    result = []
    for mut in muts :
        mut = list(mut)
        mut[0], mut[2] = mut[2], mut[0]
        mut = "".join(mut)
        mut=mut.replace(":", "")
        result.append(mut)
    return ",".join(result)

def MHC1_random_mutate(file_path, pdb, pep_chain="B"):
    
    json_path = glob.glob(file_path+f"/{pdb}*json")
    
    with open(json_path[0], "r") as f:
        json_out= json.load(f)
        json_out_shuffled = np.random.permutation(list(json_out["pep_seq"]))
    
    pdb_dic[pdb].append(pep_chain)
    pdb_dic[pdb].append(json_out["pep_seq"])
    pdb_dic[pdb].append("".join(json_out_shuffled))

def MHC2_mutate1(input_csv1_name, input_csv2_name):

    input_csv2 = fetch_sequence(input_csv2_name)[["Chain", "PEPTIDE(pdb)"]]

    input_csv1 = pd.read_csv(input_csv1_name)
    input_csv1["IMGT entry ID"] = input_csv1["IMGT entry ID"].str.upper()
    input_csv1 = input_csv.iloc[:,1:]

    merged_df = input_csv.join(peb_seq)
    
    def find_subsequence(A, B):
        result=(None, None)
        for i in range(len(A) - len(B) + 1):
            if A[i:i+len(B)] == B:
                result = (i, i+len(B)-1)
                
        return result

    ref_seqs = merged_df["PEPTIDE(ref)"]
    pdb_seqs = merged_df["PEPTIDE(pdb)"]
    
    answer_indexes=[]
    for num in range(len(ref_seqs)) :
        try:
            result = find_subsequence(ref_seqs[num], pdb_seqs[num])
            answer_indexes.append(result)
        except:
            answer_indexes.append((None, None))


    merged_df["Answer_indexes"]=answer_indexes

    return merged_df

def MHC2_mutate2(merged_df) :
    
    ref_trimmed = []
    mut_trimmed = []
    for num in range(len(merged_df)) :
        ref = merged.iloc[num,2]
        mut = merged.iloc[num,3]
        start = merged.iloc[num,-1][0]
        end = merged.iloc[num,-1][1]

        ref_ = ref[start: end+1]
        mut_ = mut[start: end+1]

        ref_trimmed.append(ref_)
        mut_trimmed.append(mut_)

    merged_df["ref_trimmed"] = ref_trimmed
    merged_df["mut_trimmed"] = mut_trimmed
    merged_df_out = merged_df[["Chain", "ref_trimmed", "mut_trimmed", "IMGT entry ID"]]
    merged_df_out.columns = ["pep_chain", "ref_seq", "mut_seq", "PDB_ID"]

    return merged_df_out

#----------------------------------------------------------------------------------------------------------------------------------------------------------#




def Ab_mutation(input_csv_name):
    Ab_csv = pd.read_csv(input_csv_name)
    Ab_csv["Mutation"] = Ab_csv["Mutation"].apply(Ab_preprocess)

    PDBs = list(dict.fromkeys(Ab_csv["PDB_ID"]))
    
    for pdb in PDBs :
        target = data.query("PDB == @pdb")
        target["Mutation"] = target["Mutation"].apply(Ab_mutate)

        m = open(f"individual_list_{pdb}.txt", "a")
        for mut in target_["Mutation"] :
            m.write(mut + ";\n")
        m.close()

def MHC1_mutation():
    Path=os.getcwd()
    file_path = os.path.join(Path, "pmhc1")
    pdb_path = glob.glob(file_path+"/*.pdb")

    pdb_dic=defaultdict(list)
    pdbs = [ele.split('\\')[-1].split(".")[0] for ele in pdb_path]

    for pdb in pdbs :
        MHC1_random_mutate(file_path, pdb)

    merged_MHC1 = pd.DataFrame(pdb_dic).T
    merged_MHC1.columns = ["pep_chain", "ref_seq", "mut_seq"]
    merged_MHC1["PDB_ID"] = merged_MHC1.index
    merged_MHC1.index = range(1, len(merged_MHC1)+1)
    
    make_mutation_list(merged_MHC1)

def MHC2_mutation(input_csv1_name, input_csv2_name):
    merged_df = MHC2_mutate1(input_csv1_name, input_csv2_name)
    assert (None, None) not in merged_df["Answer_indexes"].tolist(), "Do manual inspection!!"
    merged_MHC2 = MHC2_mutate2(merged_df)
    
    make_mutation_list(merged_MHC1)


#----------------------------------------------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":

    if input_object == "Ab" :
        Ab_mutation(input_csv_name)

    elif input_object == "MHC1" :
        MHC1_mutation()

    elif input_object == "MHC2" :
        MHC2_mutation(input_csv1_name, input_csv2_name)


