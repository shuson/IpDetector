from tkinter import *
import re
import urllib
import urllib.request
import json
item = ('country','region','province','city','isp')
itemVar = ('Country','Region','Province','City','ISP')
class MWindow(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title('IP Detector')
        self.master.geometry('700x400')
        self.pack(side = TOP,expand = YES,fill = BOTH)
        ioPut = {}
        ioPut['ip_input'] = StringVar()
        ioPut['result_ouput'] = StringVar()
        res = {}
        for vx in item:
            res[vx] = StringVar()
        # top Frame
        topF = self.createFrame(self,TOP)
        inL = self.createLabel(topF,TOP,'Please input the IP address:')
        ipE = self.createEntry(topF,TOP,ioPut['ip_input'])
        resL = self.createLabel(topF,TOP,'Result:')
        #resE = self.createEntry(topF,TOP,ioPut['result_ouput'])
        #mid Frame
        midF = self.createFrame(self,TOP)
        i = 0
        l = len(item)
        while i < l:
            L = self.createLabel(midF,LEFT,itemVar[i])
            E = self.createEntry(midF,LEFT,res[item[i]])
            i = i + 1
        #bottom Frame
        botF = self.createFrame(self,TOP)
        searchB = Button(botF,text = 'Detect',
                         command = lambda ioPut = ioPut,res = res:self.IpSearch(ioPut,res))
        searchB.pack(side = TOP,expand = YES,fill = BOTH)
    def createFrame(self,parent,side):
        f = Frame(parent)
        f.pack(side = side,expand = YES,fill = BOTH)
        return f
    def createLabel(self,parent,side,text):
        l = Label(parent,text = text)
        l.pack(side = side,expand = YES)
        return l
    def createEntry(self,parent,side,textvariable):
        e = Entry(parent,relief = SUNKEN,textvariable = textvariable,width = 15)
        e.pack(side = side,expand = NO)
        return e
    def IpSearch(self,ioPut,res):
        ipRex = '((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))'
        ip = ioPut['ip_input'].get()
        tmp = re.findall(re.compile(ipRex),ip)
        if not tmp:
            ioPut['result_ouput'].set('ip is invalid format, type in again')
            return
        reponseData = IpS().searchByTaobao(ip)
        data = json.loads(reponseData)
        if data['code'] == 0:
            ioPut['result_ouput'].set('IP Information')
        else:
            ioPut['result_ouput'].set('No Result')
        d = data['data']
        for vx in item:
            res[vx].set(d[vx])
class IpS():
    def __init__(self):
        self.apiUrlTaobao = 'http://ip.taobao.com/service/getIpInfo.php?ip='
    def searchByTaobao(self,ip):
        headers = ('User-Agent','Mozilla/5.0 (Windows NT 5.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        data = opener.open(self.apiUrlTaobao+ip).read()
        data = data.decode('UTF-8')
        return data
if __name__ == '__main__':
    MWindow().mainloop()
