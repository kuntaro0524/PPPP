"""
Usage:
python mydaq2.py "2014/05/30 10:00:00.000000" "2014/06/01 10:00:00.000000"
"""

import sys
import optparse
import urllib
import urllib2
import re

re_title = re.compile("<h1>(.*)</h1>")
#re_data = re.compile("<textarea.*>(.*)</textarea>", re.MULTILINE)

def get_data(bdate, edate, sig, col):
    url = "http://okutsu3.spring8.or.jp/cgi-bin/MyDAQ2/mydaq2_data.py?"
    query = [("sig", sig),
             ("col", col),
             ("b", bdate),
             ("e", edate),
             ("bel", "be"),
             ("format", "text"),
             ("s", "submit")
             ]
    url += urllib.urlencode(dict(query))
    response = urllib2.urlopen(url)

    html = response.read()
    #print "SIG=", sig
    #print "COL=", col
    l = html.splitlines()
    m = filter(lambda s: "textarea" in s[1], enumerate(l))
    if len(m) != 2:
        return None, None

    title = re_title.search(html).group(1)
    return title, map(lambda s:s.replace("None","nan"), l[m[0][0]+1:m[1][0]])

def run(bdate, edate, opts):
    if opts.r_style:
        print "date sig col value"

    for sig in "BL32XU_MX100", "BL32XU_EXP2":
        for col in xrange(1, 42):
            title, data = get_data(bdate, edate, sig, "c%d"%col)
            if data is None:
                continue

            print "#", title
            print "# begin:", bdate
            print "# end:", edate
            print "# sig, col:", sig, col
            if opts.r_style:
                if not opts.only_last:
                    for l in reversed(data):
                        sp = l.strip().split()
                        print '"%s %s" %s %d %s'%(sp[0].replace("/","-"), sp[1], sig, col, sp[2])
                else:
                    sp = data[-1].strip().split()
                    print '"%s %s" %s %d %s'%(sp[0].replace("/","-"), sp[1], sig, col, sp[2])
            else:
                if opts.only_last:
                    print data[-1]
                else:
                    print "\n".join(data)

            print
  

    #print html

if __name__ == "__main__":
    parser = optparse.OptionParser(usage="usage: %prog [options] start_date end_date")

    parser.add_option("--only-last","-l", action="store_true", dest="only_last")
    parser.add_option("--r-style","-r", action="store_true", dest="r_style")

    (opts, args) = parser.parse_args(sys.argv)
    bdate, edate = args[1:3]
    run(bdate, edate, opts)
