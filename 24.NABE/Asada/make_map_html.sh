out=omit_maps_3.5a.html
cat <<+ > $out
<html>
<head></head>
<body>
<table>
+

for d in Data*
do
echo $d

 log=refine_001.log
 r_wf=`grep "^Final R" $log`
 bave=`awk '/end: /{print $8}' $log`
 cc12ou=`grep "STATISTICS OF INPUT DATA SET" -B4 ../../XSCALE.LP | head -n1 | awk '{print $11}'`
 name=`echo $d | sed -e "s,/run.*,,"`
 cat <<+ >> $out
<tr>
 <td>$name<br>$r_wf<br>&lt;B&gt;=$bave<br>CC1/2.ou=$cc12ou</td>
 <td><img src="$d/test.5s_A.png" width=320></td>
</tr>
+
done

cat <<+ >> $out
</table>
</body>
+
