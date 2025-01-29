import pycbf, sys, time, numpy as np

start = time.time()
o = pycbf.cbf_handle_struct()
o.read_file(sys.argv[1],pycbf.MSG_NODIGEST)
o.select_category(0)
o.rewind_column()
while 1:
     o.next_column()
     if o.column_name() == "data":
         s=o.get_integerarray_as_string()
         break

data = np.fromstring( s , np.int32)
print "Max",data.max(), "Min",data.min(), "Mean",data.mean()
print "Time",time.time()-start

# modify the data and write out
data = data + 10

# This is somewhat cryptic:
comp, id, elsiz, elsign, elunsign, elem, mine, maxe = \
       o.get_integerarrayparameters()
o.set_integerarray( comp, id, data.tostring(), elsiz, elsign, elem )
o.write_file(sys.argv[2], # filename
              pycbf.CBF,
              pycbf.MIME_HEADERS,
              pycbf.ENC_BASE64 )
