import os,sys,math
import datetime
import calendar

class Calendar():
    def __init__(self):
        print "test"

    def getToday(self):
        tod=datetime.datetime.now()
        print tod

    def test(self):
        c = calendar.TextCalendar(calendar.SUNDAY)
        c.prmonth(2007, 7)

    def divDate(self,daystr):
        cols=daystr.split('-')
        year=cols[0]
        month=cols[1]
        day=cols[2]
    
        return year,month,day

    # start_day: ex) 2016-10-01
    # end_day  : ex) 2016-12-01
    def makeDateList(self,start_day,end_day):
        self.datelist=[]
        # divide date
        day1=self.divDate(start_day)
        return day1

    def getDayOfTheWeek(self,date):
        if date==0:
            return "MON"
        elif date==1:
            return "TUE"
        elif date==2:
            return "WED"
        elif date==3:
            return "THU"
        elif date==4:
            return "FRI"
        elif date==5:
            return "SAT"
        elif date==6:
            return "SUN"

    def getMonthList(self,year,month):
        try:
            year=int(year)
            month=int(month)
        except:
            print "OK"
        c1=calendar.Calendar()
        date_list=[]
        for day in c1.itermonthdays2(year, month):
            dw=self.getDayOfTheWeek(day[1])
            if day[0]==0:
                continue
            date_list.append((day[0],dw))
        return date_list

    def putDameDates(self,user,dame_date_list,day_list):
        for dame_date in dame_date_list:
            tyear,tmonth,tday=self.divDate(dame_date)
            for sday,syoubi in day_list:
                print sday,syoubi
                print sday,tday,user
                if sday==tday:
                    #print sday,user,"DAME"
                    break

if __name__=="__main__":
    cal=Calendar()
    cal.getToday()
    #print cal.makeDateList("2016-10-01","2016-12-01")
    octd=cal.getMonthList(2016,10)
    dame_date_list=["2016-10-15","2016-10-16"]
    cal.putDameDates("Hirata",dame_date_list,octd)
