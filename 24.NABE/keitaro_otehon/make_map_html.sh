out=omit_maps_3.5a.html
cat <<+ > $out
<html>
<head></head>
<body>
<table>
+

#for d in */cluster_*/run_03/ccp4/refine0
#for d in *3.4*/cluster_*/run_03/ccp4/refine0
for d in *3.5*/cluster_*/run_03/ccp4/refine0
do
 log=$d/xscale_KAMO_cluster55_refmac9_omitside_refine_001.log
 r_wf=`grep "^Final R" $log`
 bave=`awk '/end: /{print $8}' $log`
 cc12ou=`grep "STATISTICS OF INPUT DATA SET" -B4 $d/../../XSCALE.LP | head -n1 | awk '{print $11}'`
 name=`echo $d | sed -e "s,/run.*,,"`
 cat <<+ >> $out
<tr>
 <td>$name<br>$r_wf<br>&lt;B&gt;=$bave<br>CC1/2.ou=$cc12ou</td>
 <td><img src="$d/FCS_2.5s_e.png" width=320></td>
 <td><img src="$d/FCS_2.5s_f.png" width=320></td>
 <td><img src="$d/FCS_2.5s_g.png" width=320></td>
 <td><img src="$d/FCS_2.5s_h.png" width=320></td>
</tr>
+
done

cat <<+ >> $out
</table>
</body>
+
