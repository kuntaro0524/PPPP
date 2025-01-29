import sys,os,math
from numpy import *

# Before 141117
#a=-2.487
#b=8862

# 141117
#a= -2.51989   
#b= 8068.95   

# 160613
#a= -2.3167   
#b= 7471.4

# 171115 (pulse .vs. thickness) function thickness=a*pulse+b
a=-2.51157
b=8059.04

# 160613 added
thick_list=[100,150,200,250,300,350,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,2000,2500,3000,3500,4000,4500,5000,5500]

# 160613 added Mauro
thick_list=[100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000,1100,1200,1300,1400,1500,1600,1700,1800,2000,2500,3000,3500,4000,4500,5000,5500]

idx=1
for thick in thick_list:
	p=int((thick-b)/a)
	print "Attenuator1_%d: Al %dum %d"%(idx,thick,p)
	idx+=1

idx=1
for thick in thick_list:
	p=int((thick-b)/a)
	print "Attenuator_Menu_Label_%d: [Al %dum] { %d}"%(idx,thick,idx)
	idx+=1

# self.attPullDown = wx.ComboBox(self.notebook_1_pane_4, -1, choices=["none", "100", "150", "200", "250","300","350", "400", "500", "600", "700", "800", "900", "1000", "1100", "1200", "1300", "1400", "1500", "1600", "1700", "1800","2000", "2500", "3000", "3500", "4000", "5000", "5500"], style=wx.CB_DROPDOWN)
