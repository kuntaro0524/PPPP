#for d in $PWD/*/cluster_*/run_03/ccp4
#for d in $PWD/cccE_3.6A_framecc_b+B_1batch/cluster_*/run_03/ccp4
for d in $PWD/*3.5*/cluster_*/run_03/ccp4
do
 #mv $d/refine0{,.org}
 mkdir -v $d/refine0
 cat <<+ > $d/refine0/refine0.sh
#copy_free_R_flag.py -r /isilon/users/ktaroyam/ktaroyam/data/tomasan_lipid/_kamoproc_xds20160617/merge_171228-165755/blend_3.6A_framecc_b+B/cluster_0125/run_03/ccp4/refine_test/xscale_free.mtz ../xscale.mtz
copy_free_R_flag.py -r /isilon/users/ktaroyam/ktaroyam/data/tomasan_lipid/from_tomasan/xscale_KAMO_cluster55_refmac9.mtz ../xscale.mtz
phenix.refine \\
 xscale_copy_free.mtz \\
 strategy=rigid_body+individual_sites+individual_adp \\
 /isilon/users/ktaroyam/ktaroyam/data/tomasan_lipid/from_tomasan/xscale_KAMO_cluster55_refmac9_omitside.pdb \\
 /isilon/users/ktaroyam/ktaroyam/data/tomasan_lipid/from_tomasan/FCS_mon_lib.cif \\
 ncs_search.enabled=True write_geo=false
+
 qsub -wd $d/refine0 -j y $d/refine0/refine0.sh
done
