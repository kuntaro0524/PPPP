import sys,os,math


class ColspotInfo():
    def __init__(self, colspot_path):
        self.colspot_path = colspot_path
        self.isRead = False
        self.strong_dict = {}
        self.min_image = 9999
        self.max_image = -9999

    def read(self):
        if self.isRead == True:
            return

        self.lines = open(self.colspot_path, "r").readlines()
        # Reading
        read_flag = False

        for line in self.lines:
            cols = line.split()
            if len(cols) < 1:
                continue
            if line.rfind("FRAME #") != -1:
                read_flag = True
                continue
            if read_flag == True and line.rfind("NUMBER OF STRONG") != -1:
                read_flag = False
            if read_flag == True:
                imgnum = int(cols[0])
                strongpix = int(cols[2])
                self.strong_dict[imgnum] = strongpix
                if self.min_image > imgnum:
                    self.min_image = imgnum
                if self.max_image < imgnum:
                    self.max_image = imgnum
            if line.rfind("NUMBER OF DIFFRACTION SPOTS ACCEPTED") != -1:
                self.n_spots = int(cols[5])
        self.isRead = True

    def getStrongSpots(self):
        self.read()
        return self.strong_dict

if __name__ == "__main__":
    cols = ColspotInfo(sys.argv[1])
    cols.getStrongSpots()
    print cols.n_spots