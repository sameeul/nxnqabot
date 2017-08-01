# Module for nxnqa commands
import subprocess

# define constants
NXN_VER = 12
NAST = "//plm/cinas/cae_nxn/nastran_tools/bin"

#run a qa command and return stdout
def qa_run_cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    stdout, stderr = p.communicate() 
    return stdout.strip()

# returns a string of test case names associated with the CP
def chase_cp_info(cp_num):
    cb_id = qa_run_cmd(NAST+"/qa_cp2qa "+str(cp_num))
    cmd = NAST+"/qa_results -gb -ver " + str(NXN_VER) + " -b " + cb_id + " -m em64tL -reported"
    test_list = qa_run_cmd(cmd)
    return test_list
