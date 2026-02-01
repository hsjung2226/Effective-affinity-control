import sys
from pymol import stored, cmd

name = sys.argv[1].split(".")[0]

cmd.alter("chain B", "resv+=180")
cmd.alter("chain B", "chain='A'")

cmd.alter("chain D", "chain='C'")
cmd.sort()


cmd.save(f"{name}_trimmed.pdb", "all")

