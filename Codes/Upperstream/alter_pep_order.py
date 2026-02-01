from pymol import cmd, stored
import sys

name = sys.argv[1]
name = name.split(".")[0]

chain = sys.argv[2]

print(name, chain)
stored.resi = []

cmd.iterate_state(1, f"chain {chain} and name ca", "stored.resi.append(resi)")
origin = sorted(list(map(int,stored.resi)))[0]

cmd.alter('chain B', 'resi=str(int(resi)-(origin-1))')
cmd.sort()


#stored.after=[]
#cmd.iterate_state(1, "chain B and name ca", "stored.after.append(resi)")
#print(stored.after)



cmd.save(f"{name}.pdb", "all")
