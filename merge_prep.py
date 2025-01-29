import sys,math,os

dmin=float(sys.argv[1])
formerge_list="formerge_goodcell.lst"
if sys.argv[2]=="anoon":
	anoflag="true"
else:
	anoflag="false"

deg_per_batch=1.0
ram_flag="true"

command="Rscript ./filter_cell.R"
os.system(command)

blend_str="""
kamo.multi_merge \
workdir=blend_%3.1fA_framecc_b+B \
lstin=%s d_min=%3.1f anomalous=%s \
space_group=None reference.data=None \
program=xscale xscale.reference=bmin xscale.degrees_per_batch=%3.1f \
reject_method=framecc+lpstats rejection.lpstats.stats=em.b+bfactor \
clustering=blend blend.min_cmpl=90 blend.min_redun=2 blend.max_LCV=None blend.max_aLCV=None \
max_clusters=None xscale.use_tmpdir_if_available=%s \
batch.engine=sge batch.par_run=merging batch.nproc_each=8 nproc=8 batch.sge_pe_name=par
"""%(dmin,formerge_list,dmin,anoflag,deg_per_batch,ram_flag)

ccc_str="""
kamo.multi_merge \
workdir=blend_%3.1fA_framecc_b+B \
lstin=%s d_min=%3.1f anomalous=%s \
space_group=None reference.data=None \
program=xscale xscale.reference=bmin xscale.degrees_per_batch=%3.1f \
reject_method=framecc+lpstats rejection.lpstats.stats=em.b+bfactor \
clustering=blend blend.min_cmpl=90 blend.min_redun=2 blend.max_LCV=None blend.max_aLCV=None \
max_clusters=None xscale.use_tmpdir_if_available=%s \
batch.engine=sge batch.par_run=merging batch.nproc_each=8 nproc=8 batch.sge_pe_name=par
"""

print strstr
