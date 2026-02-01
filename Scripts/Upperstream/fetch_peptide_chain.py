import sys


seq1 = sys.argv[1]
all_chains=cmd.get_chains("all")

answer="kk"
for chain in all_chains:
    cmd.select("target", f"chain {chain}")
    seq2 = cmd.get_fastastr("target")
    seq2 = seq2.split("\n")[1]
    if seq2 in seq1 :
        answer=chain
    
print(answer)
