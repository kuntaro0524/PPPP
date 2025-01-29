score_list=[]
for xa in input_xds_list:
        filepath="../%s"%xa
        xdsas=XDSascii.XDSascii(filepath)
        sumi=xdsas.calcDP()
        score_list.append((filepath,sumi))

score_list.sort(key=lambda x:x[1])
score_list.sort(key=lambda x:int(x[1]))

