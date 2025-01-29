from TemplateMatch import *

ofile="./y-000um.ppm"
tm=TemplateMatch("./template.ppm",ofile)

y0=tm.getXY()[0]
tm.show()

ofile="./y+010um.ppm"
tm=TemplateMatch("./template.ppm",ofile)
y1=tm.getXY()[0]
tm.show()

ofile="./y+020um.ppm"
tm=TemplateMatch("./template.ppm",ofile)
y2=tm.getXY()[0]
tm.show()

ofile="./y+040um.ppm"
tm=TemplateMatch("./template.ppm",ofile)
y3=tm.getXY()[0]
tm.show()

print y0,y1,y2,y3

#phi000.ppm  phi000_10um_up.ppm  phi000_5um_up.ppm
