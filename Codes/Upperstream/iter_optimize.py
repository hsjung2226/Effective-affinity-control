import sys, os, shutil

def e_compare(f, n):
    e_cut = 0.05
    content = open(f).readlines()
    after_e = float(content[-1].split()[0])
    before_e = float(content[-3].split()[0])
    diff = before_e - after_e
    print(f"Iteration:: {n}, Before: {before_e}, After: {after_e}, Diff: {diff}")
    if diff < e_cut:
        return True
    else:
        return False

pdb = sys.argv[1]
path="/data2/2226jhs/foldx_20251231"

foldx_cmd = f"{path} --command=Optimize --pdb={pdb}"

basename = os.path.splitext(pdb)[0]
output_pdb = "Optimized_%s.pdb"%basename
fxout = "OP_%s.fxout"%basename

c = 1
while c<101:
    os.popen(foldx_cmd).read()
    stop_condition = e_compare(fxout, c)
    shutil.move(output_pdb, pdb)
    #os.remove(output_pdb)
    os.remove(fxout)
    if stop_condition:
        print("Stopped!")
        break
    else:
        c += 1

foldx_stability = f"{path} --command=Stability --pdb={pdb}"
os.system(foldx_stability)
