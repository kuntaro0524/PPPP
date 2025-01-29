/oys/xtal/cctbx/snapshots/upstream/build/bin/kamo.auto_multi_merge \
csv=./171101-PH.csv \
workdir=$PWD \
prefix=merge_ \
datadir=/isilon/users/target/target/Staff/kuntaro/171101-PH/_kamoproc
postrefine=False \
merge.max_clusters=500 \
merge.d_min_start=1.20 \
merge.clustering=cc \
merge.cc_clustering.min_acmpl=95 \
merge.cc_clustering.min_aredun=6 \
batch.engine=sge \
merge.batch.engine=sge \
merge.batch.par_run=merging \
