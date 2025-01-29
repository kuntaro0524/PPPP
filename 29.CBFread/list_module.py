from yamtbx.dataproc import cbf

print type(obj)
for x in inspect.getmembers(obj, inspect.ismethod):
  print x[0]
