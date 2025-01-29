import sys,os,math,glob

dimple_logs = open(sys.argv[1],"r").readlines()

def ana_dimple_log(dimple_log):
    save_line = ""
    lines = open(dimple_log,"r").readlines()
    for line in lines:
        #print line
        if line.rfind("free_r") != -1:
            save_line = line.strip()

    if save_line == "":
        raise Exception("ana_dimple_log cannot get Free-R from dimple.log")

    # Convertion
    free_f = float(save_line.split()[1])

    return free_f

logfile = open("summary.txt","w")
arccom = open("make_archive.com","w")

arccom.write("tar cvfz arc.tgz ")

arc_files = []

for dimple_log in dimple_logs:
    #dimple_log = os.path.join(proc_path.strip(),"dimple.log")
    #print dimple_log, os.path.exists(dimple_log)
    dimple_log = dimple_log.strip()
    try:
        print dimple_log.strip(),ana_dimple_log(dimple_log)
    except Exception as e:
        print e.args
