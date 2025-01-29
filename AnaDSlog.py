"""
 Beam shape = rectangle, Beam size = 15.0[um] x 2.0[um] (h x w)
  scan_from = 0.000[deg], scan_to = 180.000[deg], scan_step = 0.500[deg]
  sampling_interval = 1, number_of_images = 360 x 1
  delay_time = 100.0[msec], cameralength = 145.0[mm], attenuator = Al 700um
  ver. offset = 0.0[mm], hor. offset = 0.0[mm]
  inverse_beam = no
  wavelength = 1.00000, expose_time = 0.050[sec]

 Advanced Centering Parameters
  mode = vector_centering, type = auto_step
  adv_npoint = 180, adv_step = 0.0008[mm], adv_interval = 2
  center #1: -0.0323 -10.5321  0.2125
  center #2: -0.0865 -10.6601  0.2144
"""

import sys,os,math,numpy
import AttFactor

class AnaDSlog:
	def __init__(self,logfile):
		self.logfile=logfile

	def prep(self,phosec,half_nds):
		lines=open(self.logfile,"r").readlines()
		attfac=AttFactor.AttFactor()

		logstr=[]

		for line in lines:
			cols=line.split()
			if len(cols)==0:
				continue
			if line.rfind("Beam shape")!=-1:
				vbeam=float(cols[7].replace(",","").replace("[um]",""))
				hbeam=float(cols[9].replace(",","").replace("[um]",""))
			if line.rfind("scan_from")!=-1:
				scan_from=float(cols[2].replace("[deg],",""))
				scan_to=float(cols[5].replace("[deg],",""))
				scan_step=float(cols[8].replace("[deg]",""))
			if line.rfind("attenuator")!=-1:
				if line.rfind("um")!=-1:
					att_thick=float(cols[9].replace("um",""))
				else:
					att_thick=0.0
			if line.rfind("wavelength")!=-1:
				wavelength=float(cols[2].replace(",",""))
				exp_time=float(cols[5].replace("[sec]",""))
			if line.rfind("adv_npoint")!=-1:
				n_irrad=int(cols[2].replace(",",""))
				astep=float(cols[5].replace("[mm],",""))
				aint=int(cols[8])
				print n_irrad,astep,aint
			if line.rfind("center #1")!=-1:
				gx1=float(cols[2])
				gy1=float(cols[3])
				gz1=float(cols[4])
				print gx1,gy1,gz1
			if line.rfind("center #2")!=-1:
				gx2=float(cols[2])
				gy2=float(cols[3])
				gz2=float(cols[4])
				print gx2,gy2,gz2

		vec1=numpy.array((gx1,gy1,gz1))
		vec2=numpy.array((gx2,gy2,gz2))
		helical_vec=numpy.linalg.norm(vec1-vec2)*1000.0
		logstr.append("helical vector length=%8.3f um\n"%helical_vec)

		att_al=attfac.calcAttFac(wavelength,att_thick)
		logstr.append("wavelength= %12.5f\n"%wavelength)
		logstr.append("Attenuator= %8.1f um Transmission= %8.4f\n"%(att_thick,att_al))
		logstr.append("Flux rate=%6.1e photons/sec\n"%(phosec*att_al))
		
		total_nframe=(scan_to-scan_from)/scan_step
		total_exp=exp_time*total_nframe
		total_photons=total_exp*att_al*phosec
		
		logstr.append("total n frames= %5d\n"%int(total_nframe))
		logstr.append("Exptime= %8.3f sec/frame Total exp time= %8.3f\n"%(exp_time,total_exp))
		logstr.append("Total photons/dataset= %6.1e photons\n"%total_photons)
		
		logstr.append("photons/um(along gonio-Y)= %5.2e\n"%(total_photons/helical_vec))
		logstr.append("Beam size %5.1f(V)x%5.1f(H)um\n"%(vbeam,hbeam))
		photon_density=total_photons/helical_vec/vbeam
		logstr.append("Density = %6.1e phs/um^2\n"%photon_density)
		logstr.append("number of datasets at the half intensity=%5.1f\n"%half_nds)
		limit_density=photon_density*half_nds
		logstr.append("Total density to (1/2) = %6.1e phs/um^2\n"%(limit_density))

		return logstr,limit_density

	def getBeamsize(self):
                lines=open(self.logfile,"r").readlines()
                attfac=AttFactor.AttFactor()

                logstr=[]

                for line in lines:
                        cols=line.split()
                        if len(cols)==0:
                                continue
                        if line.rfind("Beam shape")!=-1:
                                vbeam=float(cols[7].replace(",","").replace("[um]",""))
                                hbeam=float(cols[9].replace(",","").replace("[um]",""))
				return vbeam,hbeam

	def prepSimple(self,phosec):
		lines=open(self.logfile,"r").readlines()
		attfac=AttFactor.AttFactor()

		logstr=[]

		for line in lines:
			cols=line.split()
			if len(cols)==0:
				continue
			if line.rfind("Beam shape")!=-1:
				vbeam=float(cols[7].replace(",","").replace("[um]",""))
				hbeam=float(cols[9].replace(",","").replace("[um]",""))
			if line.rfind("scan_from")!=-1:
				scan_from=float(cols[2].replace("[deg],",""))
				scan_to=float(cols[5].replace("[deg],",""))
				scan_step=float(cols[8].replace("[deg]",""))
			if line.rfind("attenuator")!=-1:
				if line.rfind("um")!=-1:
					att_thick=float(cols[9].replace("um",""))
				else:
					att_thick=0.0
			if line.rfind("wavelength")!=-1:
				wavelength=float(cols[2].replace(",",""))
				exp_time=float(cols[5].replace("[sec]",""))
			if line.rfind("center #1")!=-1:
				gx1=float(cols[2])
				gy1=float(cols[3])
				gz1=float(cols[4])
			if line.rfind("center #2")!=-1:
				gx2=float(cols[2])
				gy2=float(cols[3])
				gz2=float(cols[4])

		vec1=numpy.array((gx1,gy1,gz1))
		vec2=numpy.array((gx2,gy2,gz2))
		logstr.append("XYZ1= %9.5f %9.5f %9.5f"%(gx1,gy1,gz1))
		#logstr.append("XYZ2= %9.5f %9.5f %9.5f"%(gx2,gy2,gz2))

		att_al=attfac.calcAttFac(wavelength,att_thick)
		logstr.append("wavelength= %12.5f"%wavelength)
		logstr.append("Attenuator= %8.1f um Transmission= %9.5f"%(att_thick,att_al))
		logstr.append("Flux rate=%6.1e photons/sec"%(phosec*att_al))
		
		total_nframe=(scan_to-scan_from)/scan_step
		total_exp=exp_time*total_nframe
		total_photons=total_exp*att_al*phosec
		
		logstr.append("total n frames= %5d"%int(total_nframe))
		logstr.append("Exptime= %8.3f sec/frame Total exp time= %8.3f"%(exp_time,total_exp))
		logstr.append("Total photons/dataset= %8.3e photons"%total_photons)
		logstr.append("Beam size  %5.1f(V)x%5.1f(H)um"%(vbeam,hbeam))

		return logstr

if __name__ == "__main__":
	analog=AnaDSlog(sys.argv[1])
	phosec=1E12
	half_nds=50
	#analog.prep(phosec,half_nds)
	print analog.prepSimple(phosec)
