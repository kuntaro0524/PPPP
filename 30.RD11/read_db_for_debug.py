import sqlite3, csv, os, sys, numpy
sys.path.append("/isilon/BL45XU/BLsoft/PPPP/10.Zoo/Libs/")
import ESA

if __name__ == "__main__":
    n_meas = 0
    n_collected = 0

    def read_params(cond):
        root_dir = cond['root_dir']
        p_index = cond['p_index']
        mode = cond['mode']
        puckid = cond['puckid']
        pinid = cond['pinid']
        sample_name = cond['sample_name']
        wavelength = cond['wavelength']
        raster_vbeam = cond['raster_vbeam']
        raster_hbeam = cond['raster_hbeam']
        att_raster = cond['att_raster']
        hebi_att = cond['hebi_att']
        exp_raster = cond['exp_raster']
        dist_raster = cond['dist_raster']
        loopsize = cond['loopsize']
        score_min = cond['score_min']
        score_max = cond['score_max']
        maxhits = cond['maxhits']
        total_osc = cond['total_osc']
        osc_width = cond['osc_width']
        ds_vbeam = cond['ds_vbeam']
        ds_hbeam = cond['ds_hbeam']
        exp_ds = cond['exp_ds']
        dist_ds = cond['dist_ds']
        dose_ds = cond['dose_ds']
        offset_angle = cond['offset_angle']
        reduced_fact = cond['reduced_fact']
        ntimes = cond['ntimes']
        meas_name = cond['meas_name']
        cry_min_size_um = cond['cry_min_size_um']
        cry_max_size_um = cond['cry_max_size_um']
        hel_full_osc = cond['hel_full_osc']
        hel_part_osc = cond['hel_part_osc']
        isSkip = cond['isSkip']
        isMount = cond['isMount']
        isLoopCenter = cond['isLoopCenter']
        isRaster = cond['isRaster']
        isDS = cond['isDS']
        scan_height = cond['scan_height']
        scan_width = cond['scan_width']
        n_mount = cond['n_mount']
        nds_multi = cond['nds_multi']
        nds_helical = cond['nds_helical']
        nds_helpart = cond['nds_helpart']
        t_meas_start = cond['t_meas_start']
        t_mount_end = cond['t_mount_end']
        t_cent_start = cond['t_cent_start']
        t_cent_end = cond['t_cent_end']
        t_raster_start = cond['t_raster_start']
        t_raster_end = cond['t_raster_end']
        t_ds_start = cond['t_ds_start']
        t_ds_end = cond['t_ds_end']
        t_dismount_start = cond['t_dismount_start']
        t_dismount_end = cond['t_dismount_end']

        if isDS != 0:
            print "%s/_kamoproc/%s-%02d/,dose_%sMGy,ano "%(root_dir,puckid,pinid,dose_ds)

#topdir,name,anomalous
#/isilon/users/admin45/admin45/200202_BL45XU_baba/_kamoproc/CPS1013-01/,LysBr_multi01_20x20,yes

    esa = ESA.ESA(sys.argv[1])
    #print esa.getTableName()
    #esa.listDB()
    conds_dict = esa.getDict()

    datedata=sys.argv[1].replace("zoo_","").replace("db","").replace(".","").replace("/","")
    progress_file="check_%s.dat"%datedata
    ofile=open(progress_file,"w")

    for cond in conds_dict:
        read_params(cond)
