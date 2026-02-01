import sys

@cmd.extend
def fetchseq(Chain):

    cmd.select("target", f"chain {Chain}")
    seq = cmd.get_fastastr("target")
    
    print(seq)

