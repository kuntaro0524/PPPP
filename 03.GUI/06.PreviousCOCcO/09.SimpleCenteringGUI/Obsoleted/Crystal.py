import os,sys,math
from numpy import *
from Matrix import *
from Plane import *

class Crystal:

	# grid_step: [um] for virtual crystal
	def __init__(self):
		self.thick=100
		self.planes=[]
		self.nf=0
		self.psi=0.0
		self.phi=0.0
		self.isInit=False

		self.vstep=20.0
		self.hstep=20.0
	
		self.exp_radius=1.0
		self.rad_radius=1.0

	def prepVecs(self,vecA,vecB,vecD,vecG):
		self.vecA=vecA
		self.vecB=vecB
		self.vecD=vecD
		self.vecG=vecG

		# Preparation of other vectors which determine crystal shape
		self.vecAB=self.vecB-self.vecA
		self.vecAD=self.vecD-self.vecA
		#print "AD",self.vecAD
		self.vecC=self.vecA+self.vecAB+self.vecAD
		self.vecAC=self.vecC-self.vecA
		self.vecCG=self.vecG-self.vecC
		self.vecE=self.vecA+self.vecCG
		self.vecH=self.vecD+self.vecCG
		self.vecF=self.vecB+self.vecCG

		# Axis vectors
		self.vecAE=self.vecE-self.vecA
		self.vecEF=self.vecF-self.vecE
		self.vecDC=self.vecC-self.vecD
		self.vecHG=self.vecG-self.vecH

		# unit vector required later
		self.vecABu=self.vecAB/linalg.norm(self.vecAB)
		self.vecEFu=self.vecEF/linalg.norm(self.vecEF)
		self.vecDCu=self.vecDC/linalg.norm(self.vecDC)
		self.vecHGu=self.vecHG/linalg.norm(self.vecHG)

		# Crystal length (rough)
		self.cryLy=linalg.norm(self.vecAB)
		self.cryLx=linalg.norm(self.vecCG)
		self.cryLz=linalg.norm(self.vecAD)

		#print "Crystal vectors:",self.vecA,self.vecB,self.vecC,self.vecD
		for vec in [self.vecA,self.vecB,self.vecC,self.vecD]:
			tmp=vec.reshape(3,1)
			print "CRYVEC: %s"%self.printVec(tmp),

		print "Crystal size = %8.3f %8.3f %8.3f\n"%(self.cryLx,self.cryLy,self.cryLz)

	def findYrange(self):
		vec_list=[self.vecA,self.vecB,self.vecC,self.vecD,self.vecE,self.vecF,self.vecG,self.vecH]
		
		self.ymin=9999.999
		self.ymax=-9999.0
		idx=0
		for vec in vec_list:
			if vec[1] < self.ymin:
				self.ymin=vec[1]
				self.ymin_vec=vec
			if vec[1] > self.ymax:
				self.ymax=vec[1]
				self.ymax_vec=vec
			idx+=1

		return self.ymin,self.ymax

	def isCrossed(self,ys,orivec,movevec):
		y_target=orivec[1]
		ey=movevec[1]
		t=ys-y_target

		#print "isCrossed %8.3f\n"%t,
		if t>0.0:
			return True
		else:
			return False

	# XZ plane and vector cross points
	def getCrossPoints(self,ys,orivec,movevec):
		# unit vector of Y axis
		unit_y=array([0.0,1.0,0.0])

		y_target=orivec[1]
		ey=unit_y[1]
		t=ys-y_target
	
		if t<0.0:
			print "Something wrong. Check self.defineYrange"
			sys.exit(1)

		# generate cross point vector
		cross_vec=orivec+t*movevec
		return cross_vec

	def defineYrange(self,ymin,ymax):
		vec_list=[(self.vecA,self.vecABu),
			(self.vecE,self.vecEFu),
			(self.vecD,self.vecDCu),
			(self.vecH,self.vecHGu)]

		scan_step=0.5 #[um]
		nscan=int((ymax-ymin)/scan_step)+1

		plane_flag=False
		ymax_efec=0.0
		for idx in range(0,nscan):
			yscan=ymin+float(idx)*scan_step
			nplane=0
			plane_vec=[]
			for idx in range(0,len(vec_list)):
				orivec,movevec=vec_list[idx]
				if self.isCrossed(yscan,orivec,movevec):
					nplane+=1
			#print "NPLANE:%5d"%nplane
			if nplane==4 and plane_flag==False:
				ymin_efec=yscan
				plane_flag=True
			elif plane_flag==True and nplane<4:
				ymax_efec=yscan-scan_step
				break
				#return ymin_efec,ymax_efec
		if ymax_efec==0.0:
			ymax_efec=ymax

		self.ystart=ymin_efec
		self.yend=ymax_efec
		self.ny=int((ymax_efec-ymin_efec)/self.hstep)
		#print self.ny
		#for i in range(0,self.ny+1):
			#print self.ystart+i*self.hstep

	def makeXZplanes(self):
		ymin=self.ystart
		ymax=self.yend

		vec_list=[(self.vecA,self.vecABu),
			(self.vecD,self.vecDCu),
			(self.vecH,self.vecHGu),
			(self.vecE,self.vecEFu)]

		# Cross points of XZ plane and vectors (AB,EF,DC,HG)
		self.XZplanes=[]
		for idx in range(0,self.ny+1):
			y=ymin+float(idx)*self.hstep
			tmp_plane=[]
			for vecs in vec_list:
				orivec,movevec=vecs
				newvec=self.getCrossPoints(y,orivec,movevec)
				#print vecs,"NEW:",newvec
				tmp_plane.append(newvec)
				
			self.XZplanes.append(tmp_plane)

		#for plane in self.XZplanes:
			#a,b,c,d=plane
			#print "AB %8.3f %8.3f %8.3f"%(a[0],a[1],a[2])
			#print "DC %8.3f %8.3f %8.3f"%(b[0],b[1],b[2])
			#print "HG %8.3f %8.3f %8.3f"%(c[0],c[1],c[2])
			#print "EF %8.3f %8.3f %8.3f"%(d[0],d[1],d[2])
			#print type(plane)

	def printVec(self,vec):
		# Shape (3,1)
		string="%8.3f %8.3f %8.3f\n"%(vec[0,0],vec[1,0],vec[2,0])
		return string

	def findMinMaxZvecs(self,a,b,c,d):
		veclist=[a,b,c,d]
		za=a[2,0]
		zb=b[2,0]
		zc=c[2,0]
		zd=d[2,0]
		zlist=[za,zb,zc,zd]
		tmplist=array(zlist)
		imin=tmplist.argmin()
		imax=tmplist.argmax()

		print "MIN: ",self.printVec(veclist[imin]),
		print "MAX: ",self.printVec(veclist[imax]),
		
		return veclist[imin],veclist[imax]
			
	def makeExpVectors(self,plane_vecs,phi,dphi,safety_gap=0.0):
		# plane_vecs is components of self.XZplanes
		print "# ROTATION %5.2f"%phi
		a,b,c,d=plane_vecs

		# rotation
		a_=self.rotate(a.reshape(3,1),phi)
		b_=self.rotate(b.reshape(3,1),phi)
		c_=self.rotate(c.reshape(3,1),phi)
		d_=self.rotate(d.reshape(3,1),phi)

		print "========== PLANE START =========="
		print "ORIG: %s"%self.printVec(a.reshape(3,1)),
		print "ORIG: %s"%self.printVec(b.reshape(3,1)),
		print "ORIG: %s"%self.printVec(c.reshape(3,1)),
		print "ORIG: %s"%self.printVec(d.reshape(3,1)),
		print "AFTE: %s"%self.printVec(a_),
		print "AFTE: %s"%self.printVec(b_),
		print "AFTE: %s"%self.printVec(c_),
		print "AFTE: %s"%self.printVec(d_),
		print "========== PLANE END =========="

		minvec,maxvec=self.findMinMaxZvecs(a_,b_,c_,d_)
		#print minvec,maxvec
		max2minvec=minvec-maxvec
		Ldash=fabs(max2minvec[2,0])
		
		print "# Crystal size viewed from X-ray:%8.2f[um] "%Ldash
		print "# Safety length from MAX/MIN    :%8.2f[um] "%safety_gap

		startvec=maxvec+(safety_gap/Ldash)*max2minvec
		endvec=minvec-(safety_gap/Ldash)*max2minvec
		# New vector for determining irradiation points
		newvec=endvec-startvec
		lenvec=linalg.norm(newvec)

		print "Length of scan vector from X-ray: %8.3f [um]"%fabs(newvec[2,0])

		nf=int(Ldash/self.vstep)
		lenstep=lenvec/float(nf)
		move_vec=newvec/float(nf)

		print "# of points in Fast axis %5d"%nf

		for i in range(0,nf+1):
			work=startvec+i*move_vec
			print "IRRADIATION: %s"%self.printVec(work),

		#startvec=maxvec
		#endvec=minvec
		#print "STARTV: %s"%self.printVec(startvec)
		#print "ENDV: %s"%self.printVec(endvec)

		phistart=phi
		phiend=phi+float(nf)*dphi

		print "PHI RANGE %5.1f - %5.1f"%(phistart,phiend)

		tpl=[startvec,endvec,nf,phistart,phiend,lenvec,lenstep]
		return tpl

	def makeInitialVecs(self,phistart,dphi):
		idx=0
		phi=phistart
		for plane_vecs in self.XZplanes:
			tpl=self.makeExpVectors(plane_vecs,phi,dphi)
			self.exp_list.append(tpl)
			phi_end=tpl[4]
			phi=phi_end+dphi
			idx+=1
		print "###############################"
		print "From this crystal range Nplanes:%5d (%5.1f - %5.1f)[deg.]\n"%(len(self.XZplanes),phistart,phi_end)
		print "###############################"
		return phi_end

	def init(self,vecA,vecB,vecD,vecG,vstep,hstep):
		self.vstep=vstep
		self.hstep=hstep
		self.prepVecs(vecA,vecB,vecD,vecG)
		ymin,ymax=self.findYrange()
		self.defineYrange(ymin,ymax)
		self.makeXZplanes()
		self.exp_list=[]

	def trans(self,vec,trans):
		return vec-trans

	def rotate(self,vec,phi):
                phirad=radians(phi)
                rotmat=matrix( (
                        ( cos(phirad), 0.,sin(phirad)),
                        (     0., 1.,     0.),
                        ( -sin(phirad), 0., cos(phirad))
                ) )

		rotated=dot(rotmat,vec)
		return rotated

	def writeDiv(self,prefix):
		oname1="%s_exposed.dat"%prefix
		oname2="%s_damaged.dat"%prefix
		oname3="%s_bad.dat"%prefix

		exp_file=open(oname1,"w")
		dmg_file=open(oname2,"w")
		bad_file=open(oname3,"w")

		for i in range(0,len(self.vcry)):
			tmp=self.vcry[i]
			x,y,iburn,idamaged,ibad=float(tmp[0][0]),float(tmp[0][1]),int(tmp[1]),int(tmp[2]),int(tmp[3])
			if iburn !=0:
				exp_file.write("%8.3f %8.3f %5d %5d %5d\n"%(x,y,iburn,idamaged,ibad))
			if idamaged!=0:
				dmg_file.write("%8.3f %8.3f %5d %5d %5d\n"%(x,y,iburn,idamaged,ibad))
			if ibad!=0:
				bad_file.write("%8.3f %8.3f %5d %5d %5d\n"%(x,y,iburn,idamaged,ibad))
		exp_file.close()
		dmg_file.close()
		bad_file.close()

	def displayExp(self):
		#tpl=[startvec,endvec,nf,phistart,phiend]
		idx=0
		for tpl in self.exp_list:
			startvec,endvec,nf,phistart,phiend,lenvec,lenstep=tpl
			# startvec to xyz
			sx=startvec[0,0]
			sy=startvec[1,0]
			sz=startvec[2,0]
			ex=endvec[0,0]
			ey=endvec[1,0]
			ez=endvec[2,0]
			print "%5d %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %5.1f %5.1f\n"%(idx,sx,sy,sz,ex,ey,ez,phistart,phiend),
			idx+=1

	def getNplanes(self):
		return self.ny

	def getAllConditions(self):
		return self.exp_list

	def getConditionAt(self,idx):
		#tpl=[startvec,endvec,nf,phistart,phiend]
		tpl=self.exp_list[idx]
		startvec,endvec,nf,phistart,phiend,lenvec,lenstep=tpl
		# startvec to xyz
		sx=startvec[0,0]
		sy=startvec[1,0]
		sz=startvec[2,0]
		ex=endvec[0,0]
		ey=endvec[1,0]
		ez=endvec[2,0]
		return idx,nf,sx,sy,sz,ex,ey,ez,phistart,phiend,lenvec,lenstep

	def modConditionAt(self,idx,phi,dphi,safety_gap=0.0):
		plane_vecs=self.XZplanes[idx]
		#print "BEFORE",self.exp_list[idx]
		#print plane_vecs
		tpl=self.makeExpVectors(plane_vecs,phi,dphi,safety_gap)
		startvec,endvec,nf,phistart,phiend,lenvec,lenstep=tpl
		self.exp_list[idx]=tpl

		return True

	def simulateCrystal(self,startphi,dphi,phi_goal,vstep,hstep):
		startphi=0.0
		icry=0
		while(1):
			icry+=1
			self.init(self.vecA,self.vecB,self.vecD,self.vecG,vstep,hstep)
			endphi=self.makeInitialVecs(startphi,0.1)
			if endphi > phi_goal:
				break
			startphi=endphi+dphi
		print "N crystals = %5d\n"%icry

if __name__=="__main__":

	#if len(sys.argv)!=6 :
		#print "Usage program HEIGHT THICK VSTEP STARTPHI ENDPHI"
		#sys.exit(1)

	#clen=float(sys.argv[1])
	#thick=float(sys.argv[2])
	#vstep=float(sys.argv[3])
	#startphi=float(sys.argv[4])
	#endphi=float(sys.argv[5])

        #vecA=array([ 0,0,0])
        #vecB=array([ 0,500,0])
        #vecD=array([ 0,0,-500])
        #vecG=array([50,500,-500])

    	#vecA=array([335.8,  -12915.4,    258.8])
    	#vecB=array([240.8,  -13278.3,    490.1])
    	#vecD=array([465.8,  -12696.4,    620.9])
    	#vecG=array([325.8,  -13037.5,    867.1])

    	#vecA=array([335.8,  -12915.4,    -258.8])
    	#vecB=array([240.8,  -13278.3,    -490.1])
    	#vecD=array([325.8,  -13037.5,    -867.1])
    	#vecG=array([465.8,  -12696.4,    -620.9])

    	vecA=array([-50,-250,250])
    	vecB=array([0,250,250])
    	vecD=array([-50,-250,-250])
    	vecG=array([-50,250,-250])

	phistart=90.0
	dphi=0.1
	vstep=20.0
	hstep=20.0

	cry=Crystal()
	cry.init(vecA,vecB,vecD,vecG,vstep,hstep)
	cry.makeInitialVecs(phistart,dphi)

	print cry.getAllConditions()
	#cry.displayExp()
	#print "##############################################"
	#print "##############################################"
	while (1):
		print "##############################################"
		print "##############################################"
		print "# No. frames  phistart phiend ################"
		for i in range(0,cry.getNplanes()+1):
			tpl=cry.getConditionAt(i)
			idx,nf,sx,sy,sz,ex,ey,ez,phistart,phiend,lenvec,lenstep=tpl
			#print tpl
			print "%5d %5d %8.2f %8.2f %8.3f %8.3f\n"%(idx,nf,phistart,phiend,lenvec,lenstep),
		print "Enter the number of vector: ['end' for finish] "
		cha=raw_input()
		if cha=="end":
			break
		idx=int(cha)
		tpl=cry.getConditionAt(idx)
		idx,nf,sx,sy,sz,ex,ey,ez,phistart,phiend,lenvec,lenstep=tpl
		print "%5d %5d %8.2f %8.2f\n"%(idx,nf,phistart,phiend),
		print "Input aimed phi for this plane:"
		cha=raw_input()
		print "INPUT:",cha
		cols=cha.split()
		phi=float(cols[0])
		cry.modConditionAt(idx,phi,dphi,safety_gap=0.0)
		tpl=cry.getConditionAt(idx)
		idx,nf,sx,sy,sz,ex,ey,ez,phistart,phiend,lenvec,lenstep=tpl
		print "MOD: %5d %5d %8.2f %8.2f\n"%(idx,nf,phistart,phiend),
		print "Finished?"
		cha=raw_input()
	
		if cha=="y":
			break

	print "##############################################"
	print "##############################################"
	print "# No. frames  phistart phiend ################"
	for i in range(0,cry.getNplanes()+1):
		tpl=cry.getConditionAt(i)
		idx,nf,sx,sy,sz,ex,ey,ez,phistart,phiend,lenvec,lenstep=tpl
		print "%5d %5d %8.2f %8.2f\n"%(idx,nf,phistart,phiend),

	#print cry.modConditionAt(3,7.8,dphi,50)
	#cry.simulateCrystal(startphi,dphi,135.0,vstep,hstep)
