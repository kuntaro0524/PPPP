import json, sys

def main():
    f = open(sys.argv[1],"r")
    json_dict = json.load(f)

    # Important
    print ("{}".format(json.dumps(json_dict,indent=4)))
    return json_dict

def dumpName(json_data):
    name_list = ["honoka", "eri", "kotori", "umi", "rin", "maki", "nozomi", "hanayo", "niko"]
    for name in name_list:
        #print("{0:6s} Shincahou = :{1}cm BWH: ".format(name,json_data[name]["height"]), end ="\t")
        print("{0:6s} Shincahou = :{1}cm BWH: ".format(name,json_data[name]["height"])),

        for i in range(len(json_data[name]["BWH"])):
#            print("{}".format(json_data[name]["BWH"][i]), end="\t")
            print("{}".format(json_data[name]["BWH"][i])),
        print()

def dumpAll(json_dict):
    print json_dict
    for i,j in json_dict.items():
        print i,j["BWH"]

def writeJsonFile(json_dict, outfile):
    ofile = open(outfile, "w")
    json.dump(json_dict, ofile)
    ofile.close()

if __name__ == '__main__':
    json_dict = main()
    dumpName(json_dict)
    print "###################################################"
#    json2dict(json_data)
    writeJsonFile(json_dict, "Bestu.json")
    dumpAll(json_dict)