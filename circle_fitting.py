import sys,os,math,scipy

class FittingForFacing:

    def prep(self):
        self.phi_list=np.array(self.phis)
        self.area_list=np.array(self.areas)

        # Mean value in amplitude
        self.mean=np.mean(self.area_list)

        # Scipy fitting
        import scipy.optimize

        # initial guess for the parameters
        parameter_initial = np.array([0.0, 0.0, self.mean]) #a, b

        param_opt, covariance = scipy.optimize.curve_fit(self.func, self.phi_list, self.area_list, p0=parameter_initial)
        print "parameter =", param_opt

        """ # DEBUGGING PLOT
        phi_tmp = np.linspace(0, 360, 100)
        ny = self.func(phi_tmp,param_opt[0],param_opt[1],param_opt[2])
        plt.plot(self.phi_list, self.area_list, 'o')
        plt.plot(phi_tmp, ny, '-')
        plt.show()
        """

        self.isDone=True
        return param_opt

    def func(self,phi,a,b,c):
        return a*np.cos(np.pi/90.0*(phi+b))+c

    def findFaceAngle(self):
        if self.isDone==False:
            param_opt=self.prep()

        phi_tmp = np.linspace(0, 180, 36)
        ny = self.func(phi_tmp,param_opt[0],param_opt[1],param_opt[2])

        min_value=1000000.0
        for phi,value in zip(phi_tmp,ny):
            if value < min_value:
                min_value=value
                phi_min=phi

        face_angle=phi_min+90.0
        print "findFaceAngle=%5.1f deg."%face_angle
        return face_angle

    def check(self):
        if self.isDone==False:
            self.prep()
        phi_tmp = np.linspace(0, 360, 100)
        print phi_tmp
        plt.figure()
        plt.plot(self.phi_list,self.area_list,'r-')
        plt.plot(phi_tmp, self.p1[0]*np.cos(np.pi/90.0*phi_tmp)+self.p1[1], 'o')
        plt.show()

