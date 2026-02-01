import numpy as np
import pandas as pd
import pulp

def LinearProblem(Meta_data, random_combination, pdb_id, All_results) :

    target_data = Meta_data[Meta_data['Pdb'] == pdb_id]
    print(target_data)
    answer_data = target_data[target_data["Is_Answer"] == 1]
    other_data = target_data[target_data["Is_Answer"] == 0]

    print("--------------------",answer_data, other_data)
    energy_columns = np.array(answer_data.columns)
    energy_columns = energy_columns[random_combination]
    answer_values = answer_data[energy_columns].iloc[0].astype(float)

    n = len(energy_columns)
    idxlist = [i + 1 for i in range(n)]
    x = pulp.LpVariable.dicts('x', idxlist, lowBound=None, upBound=1, cat="Continuous")


    linearProblem = pulp.LpProblem(f"pdb_{pdb_id}_opt", pulp.LpMinimize)

    # 목적 함수 설정
    objective_function = sum(answer_values[i] * x[i + 1] for i in range(n))
    linearProblem += objective_function

    # 제약 조건 추가: 다른 모드들과 비교하여 N개의 에너지 텀을 포함
    constraints=[]
    for _, other_row in other_data.iterrows():
        other_values = other_row[energy_columns].astype(float)
        constraint = sum((answer_values[i] - other_values[i]) * x[i + 1] for i in range(n))
        constraints.append([answer_values[i] - other_values[i] for i in range(n)])

        linearProblem += constraint <= 0

    # 제약 조건 추가: 다른 PDB들과 비교하여 N개의 에너지 텀을 포함
    if All_results == [] :
            pass
    else :
        p_constraints = pd.DataFrame(All_results)["constraints"].explode().tolist()

        for p_constraint in p_constraints :
            constraint = sum(p_constraint[i] * x[i + 1] for i in range(n))

            linearProblem += constraint <=0


    solution = linearProblem.solve()

    # 결과 저장
    result_entry = {'pdb_id': pdb_id, 'min_value': pulp.value(linearProblem.objective), 'job_status' : pulp.LpStatus[solution] }
    for i in range(n):
        result_entry[f'x{i + 1}'] = pulp.value(x[i + 1])
        result_entry[f'energy_{i + 1}'] = answer_values[i]
    
    Error = False

    if result_entry["min_value"] > -1e-3 :
        result_entry["constraints"] = np.zeros_like(constraints)
        Error = True
    else :
        result_entry["constraints"] = constraints


    return result_entry, Error



def Dependent_Trial(Meta_data, random_combination) :

    pdb_ids = Meta_data["Pdb"].tolist() 
    pdb_ids = list(dict.fromkeys(pdb_ids))
    All_results = []
    
    Errors=[]
    for pdb_id in pdb_ids:
        result_entry, Error = LinearProblem(Meta_data, random_combination, pdb_id, All_results)
        All_results.append(result_entry)
        if Error :
            Errors.append(pdb_id)

    for pdb_id in Errors :
        result_entry, Trash = LinearProblem(Meta_data, random_combination, pdb_id, All_results)
        All_results.append(result_entry)
        
        
    return All_results



