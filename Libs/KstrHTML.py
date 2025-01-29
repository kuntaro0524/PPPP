import os,sys

class KstrHTML:

    def __init__(self):
        self.isPrep = True

    def makeOnMouse(self, imgindex, picture, height, button):
        string = ""
        string += "<a href=%s " % picture
        string += "onmouseover=\"document.getElementById('ph-%ds').style.display='block';\" " % imgindex
        string += "onmouseout=\"document.getElementById('ph-%ds').style.display='none'; \"> %s </a> " % (imgindex, button)
        #string += "<div style=\"position:absolute;\"> "
        string += "<img src=\"%s\" height=\"%d\" id=\"ph-%ds\"" % (picture, height, imgindex)
        #string += " style=\"zindex: 10; position: absolute; top: 50px; display:none;\" /></td></div>"
        string += " style=\"zindex: 10; position: absolute; top: 100px; right:800px; display:none;\" />"

        return string

if __name__ == "__main__":
    kstr = KstrHTML()
    print kstr.makeOnMouse(0,"/Users/kuntaro/test.png", 500, "O")
