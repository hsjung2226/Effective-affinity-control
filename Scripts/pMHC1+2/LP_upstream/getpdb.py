#!/usr/bin/env python3

#
# Revisions:
#   30 Oct 2007 : Yoonjoo Choi
#   31 Oct 2007 : Sebastian Kelm
#    9 Feb 2008 : Sebastian Kelm
#   13 May 2011 : Yoonjoo Choi
#   18 Feb 2021 : Yoonjoo Choi
#
# Notes:
#   For use on a STATS department server. Put this in your ~/bin directory.
#   The pdb files should be placed in /data/hostname/username/db/pdb/.
#   If nothing found, this code tries to download the query PDB structure from the web.
#

import sys, os, os.path
from urllib.request import urlretrieve

pdb_dir = 
verbose = False
PDBurl = "http://files.rcsb.org/download/"

def get_pdb_path(pdb_code):
  return pdb_dir+pdb_code[1:3]+'/pdb'+pdb_code.lower()+'.ent.gz'

def errormsg():
    print("Type 'getpdb -h' or 'getpdb --help' for more information.")

def help():
    print("This is a programme to retrieve pdb files from a local database.")
    print("It will create pdb files in the current working directory with")
    print("names in the format 'PDBCODE.pdb'.")
    print("")
    print("USAGE:")
    print("   getpdb PDBCODE ...")
    print("")
    print("OPTIONS:")
    print("   -h   --help      Print this message.")
    print("   -v   --verbose   Print error messages to STDERR.")
    print("")

def ProgressBar(count, blockSize, totalSize):
    sys.stdout.write(".")
    sys.stdout.flush()

def parsing(name):
    name = name.lower()
    stringpath = get_pdb_path(name)
    if os.path.isfile(stringpath):
        contents = os.popen("zcat "+stringpath).read()
        if contents:
            output = open(name+".pdb", "w")
            output.write(contents)
            output.close()
            return True
        elif verbose:
            sys.stderr.write("ERROR: Could not read PDB file: "+name+"\n")
    elif verbose:
        sys.stderr.write("ERROR: No corresponding PDB file: "+name+"\n")
    else:
        print("FAILED\nTrying to get %s from http://www.pdb.org"%name.upper())
        print("Connecting to %s%s"%(PDBurl, name.upper()))
        urlretrieve(os.path.join(PDBurl, name.upper()+".pdb"), "%s.pdb"%name, reporthook=ProgressBar)
        if os.path.isfile("%s.pdb"%name):
            Retrieved = open("%s.pdb"%name).read()
            if not Retrieved.count("ATOM"):
                print("\n%s does not exist in PDB."%name)
                os.remove("%s.pdb"%name)
                return False
            else:
                return True
        else:
            return False

if __name__ == "__main__":

  if len(sys.argv) < 2:
      errormsg()
      sys.exit(1)
  else:
      if sys.argv[1] == "--help" or sys.argv[1] == '-h':
          help()
          sys.exit(1)
      else:
          status = len(sys.argv)-1
          for arg in sys.argv[1:]:
              if arg[0] == '-':
                  status -= 1
                  if arg == '-v' or arg == '--verbose':
                      verbose = not verbose
              else:
                  if len(arg) != 4:
                      sys.stderr.write("ERROR: Argument needs to have length 4: "+arg+"\n")
                  else:
                      sys.stderr.write("Getting "+arg+"...")
                      if parsing(arg):
                          status -= 1
                          sys.stderr.write("DONE\n")
                      else:
                          sys.stderr.write("FAILED\n")
  sys.exit(status)
