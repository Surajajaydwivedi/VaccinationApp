#imports

import os
def cmd(s):
    ss='cmd /c '
    ss+='"'+s+'"'
    os.system(s)
os.system('cmd /c "python -m pip install --upgrade pip"')
try: 
    from datetime import date
except:
    cmd("pip install DateTime")
    from datetime import date
import datetime
import time
start=time.time()
try:
    from selenium import webdriver
except:
    os.system('cmd /c "pip install selenium"')
    from selenium import webdriver
try:
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options
except:
    cmd("pip install webdriver-manager")
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options
try:
    import ast
except:
    cmd("pip install AST")
    import ast

try:
    import requests
except:
    cmd("pip install requests")
    import requests
try:
    from lxml import html 
except:
    cmd("pip install lxml")
    from lxml import html
opts = Options()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
driver = webdriver.Chrome(ChromeDriverManager().install(),options=opts)


#Basics

def typecast(s):
    return ast.literal_eval(s)

def get_date():
    today = date.today()
    today = str(today.strftime("%d/%m/%Y"))
    return today

def getaddr():
    addr=(os.path.abspath(__file__))
    i=-1
    while addr[i]!="\\":
        i-=1
    i+=1
    addr=addr[:i]
    return addr

def organise(s):
    s=s[12:-1]
    s=typecast(s)
    s18=[]
    s45=[]
    for i in s:
        i['address']+=", "+i['block_name']+", "+i['district_name']+", "+str(i['pincode'])
        if i["min_age_limit"]==45:
            s45.append(i)
        else:
            s18.append(i)
    return [s18,s45]

def organisests(s):
    s=s[10:-10]
    s=typecast(s)
    stid={}
    for i in s:
        stid[i["state_name"].upper()]=str(i["state_id"])
    return stid

def organisedts(s):
    s=s[13:-10]
    s=typecast(s)
    did={}
    for i in s:
        did[i["district_name"].upper()]=str(i["district_id"])
    return did



#Web Drivers
def drive(url):
    driver.get(url)
    s=(driver.find_element_by_xpath("/html/body").text)
    return s
def distrify(sid):
    url="https://cdn-api.co-vin.in/api/v2/admin/location/districts/"+sid
    return drive(url)

def get_by_pincode(pincode):
    url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+pincode+"&date="+get_date()
    return drive(url)
def get_by_pincode7(pincode):
    url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="+pincode+"&date="+get_date()
    return drive(url)

def get_by_district(dcode):
    url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id="+dcode+"&date="+get_date()
    return drive(url)
def get_by_district7(dcode):
    url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+dcode+"&date="+get_date()
    return drive(url)
def statesfy():
    url="https://cdn-api.co-vin.in/api/v2/admin/location/states"
    return drive(url)

def find_city(pincode):
    
    url= "https://pincode.net.in/"
    url+=pincode
    path = '//*[@id="content"]/div[2]/div/a[2]'
    path2 = '//*[@id="content"]/div[2]/div/a[3]'
    response = requests.get(url)
    byte_data = response.content
    source_code = html.fromstring(byte_data)
    try:
        tree = source_code.xpath(path)
        city=(tree[0].text_content())
        tree = source_code.xpath(path2)
        state=(tree[0].text_content())
        code=0
    except:
        code=1
        city=("Data for Pincode does not exist.")
    return [code,state,city]



#Writing to files

def writestates(addr):
    fstat = open((addr)+"States.txt","w")
    fstat.write(', ')
    statlist=organisests(statesfy())
    for i in statlist:
        fstat.write('"'+i+'" : "'+statlist[i]+'" ,')
    fstat.close()

def writedist(addr,sid,sname):
    fdist = open((addr)+sname+".txt","w")
    ffd = open((addr)+"Dists.txt","a+")
    dlist=organisedts(distrify(sid))
    fdist.write(str(len(dlist)))
    fdist.write("\n")
    for i in dlist:
        fdist.write('"'+i+'" : "'+dlist[i]+'" ,')
        ffd.write('"'+i+'" : "'+dlist[i]+'" ,')
    fdist.close()
    ffd.close()

#Reading Files
#Pincodes
def getpins(addr):
    try:
        fpins = open(addr+"PinDef.txt","r+")
    except:
        fpins = open(addr+"PinDef.txt","w+")
        fpins.write(',')
        fpins.close()
        fpins = open(addr+"PinDef.txt","r+")
    try:
        pins="{"+fpins.read()[1:-1]+"}"
    except:
        fpins = open(addr+"PinDef.txt","w+")
        fpins.write(',')
        fpins.close()
        fpins = open(addr+"PinDef.txt","r+")
        pins="{"+fpins.read()[1:-1]+"}"
    pins=typecast(pins)
    if type(pins) is not dict:
        fpins = open(addr+"PinDef.txt","w+")
        fpins.write(',')
        fpins.close()
        fpins = open(addr+"PinDef.txt","r+")
        pins="{"+fpins.read()[1:-1]+"}"
        pins=typecast(pins)
    return [pins,fpins]

#States
def checkstates(addr):
    try:
        fstat = open((addr)+"States.txt","r+")
    except:
        writestates(addr)
        
        fstat = open(addr+"States.txt","r+")
    s="{"+fstat.read()[1:-1]+"}"
    try:
        s=typecast(s)
        if len(s)!=37:
            writestates(addr)
    except:
        writestates(addr)
        fstat = open(addr+"States.txt","r+")
        s="{"+fstat.read()[1:-1]+"}"
    fstat.close()
    print("States Ok")
    return s

#District
def checkdistricts(addr,sid,sname):
    
    try:
        fdist = open((addr)+sname+".txt","r+")
    except:
        
        writedist(addr,sid,sname)
        
        fdist = open((addr)+sname+".txt","r+")
    try:
        n=int(fdist.readline().strip())
    except:
        writedist(addr,sid,sname)
        fdist = open((addr)+sname+".txt","r+")
        n=int(fdist.readline().strip())
    s="{"+fdist.read()[:-1]+"}"

    try:
        s=typecast(s)
        if len(s)!=n:
            writedist(addr,sid,sname)
    except:
        writedist(addr,sid,sname)
        fdist = open((addr)+sname+".txt","r+")
        n=int(fdist.readline())
        s="{"+fdist.read()[:-1]+"}"
    fdist.close()
    print(sname,"Ok")

def getdist(addr):
    fdist = open(addr+"Dists.txt","r+")
    dists="{"+fdist.read()[:-1]+"}"
    dists=typecast(dists)
    return dists

def getdcode(addr,sname,dname):
    fdist = open(addr+sname+".txt","r+")
    n=int(fdist.readline())
    dists="{"+fdist.read()[:-1]+"}"
    dists=typecast(dists)
    return dists[dname]
#Print 
#Eng
def printvaccines(s18,s45):
    
    if len(s45)==0 and len(s18)==0:
        print("Sorry, seems like there are no vaccines around you. :(")
    elif len(s45)!=0 and len(s18)!=0:
        print("We found vaccines for both 18+ and 45+!")
        print("Here are the details : ")
        print("For 18+:")
        for i in s18:
            print("\t",i['date'],i['name'],"(",i['available_capacity'],i['vaccine'],")")
            print("\t\t",i['address'])
        
        print("For 45+:")
        for i in s45:
            print("\t",i['date'],i['name'],"(",i['available_capacity'],i['vaccine'],")")
            print("\t\t",i['address'])
        
    else:
        if len(s18)!=0:
            print("Vaccines are available only for 18+")
            print("Here are the details : ")
            print("For 18+")
            for i in s18:
                print("\t",i['date'],i['name'],"(",i['available_capacity'],i['vaccine'],")")
                print("\t\t",i['address'])
        
        else:
            print("Vaccines are available only for 45+")
            print("Here are the details : ")
            print("For 45+:")
            
            for i in s45:
                print("\t",i['date'],i['name'],"(",i['available_capacity'],i['vaccine'],")")
                print("\t\t",i['address'])

def selectbydistrict7(distname,sname):
    addr=getaddr()
    if distname=="z":
        distname=input("Enter District Name : ").upper()
        dist=getdist((addr+"\\states\\"))
        dcode=dist[distname]
    else:
        dcode=getdcode((addr+"\\states\\"),sname,distname)
    sdata=get_by_district7(dcode)
    sdata=organise(sdata)
    s18,s45=sdata[0],sdata[1]
    printvaccines(s18,s45)
        
def selectbydistrict(distname,sname):
    addr=getaddr()
    if distname=="z":
        distname=input("Enter District Name : ").upper()
        dist=getdist((addr+"\\states\\"))
        dcode=dist[distname]
    else:
        dcode=getdcode((addr+"\\states\\"),sname,distname)
    sdata=get_by_district(dcode)
    sdata=organise(sdata)
    s18,s45=sdata[0],sdata[1]
    printvaccines(s18,s45)
    
def selectbypincode7(ll):
    if ll[0]==0:
        pincode=input("Enter pincode : ")
        sdata=get_by_pincode7(pincode)
        sdata=organise(sdata)
        s18,s45=sdata[0],sdata[1]
        pins,fpins=getpins(getaddr())
        fcity=find_city(pincode)
        city,state,code=fcity[2],fcity[1],fcity[0]
        city=city.upper()
        fpins.write('"'+pincode+'" : "'+city+'" ,')
        fpins.close()
    else:
        pincode=ll[0]
        city,state,code=ll[1],ll[2],ll[3]
        sdata=get_by_pincode7(pincode)
        sdata=organise(sdata)
        s18,s45=sdata[0],sdata[1]
        
    printvaccines(s18,s45)
    

def selectbypincode():
    pincode=input("Enter pincode : ")
    sdata=get_by_pincode(pincode)
    sdata=organise(sdata)
    s18,s45=sdata[0],sdata[1]
    pins,fpins=getpins(getaddr())
    fcity=find_city(pincode)
    city,state,code=fcity[2],fcity[1],fcity[0]
    city=city.upper()
    fpins.write('"'+pincode+'" : "'+city+'" ,')
    fpins.close()
    printvaccines(s18,s45)
    print("Would you like to check all vaccines in rest of",city.title(),"as well?")
    if input("Enter 1 for Yes\n\t 2 for No : ")=="1":
        selectbydistrict(city,state)
    '''print("Would you like to check all vaccines in your area for next 7 days?")
    if input("Enter 1 for Yes\n\t 2 for No : ")=="1":
        selectbypincode7([pincode,city,state,code])'''
    
def initialize():
    addr=getaddr()
    k=checkstates(addr)
    for i in k:
        checkdistricts((addr+"\\states\\"),k[i],i)
    print("Districts OK")
if __name__=="__main__":
    initialize()
    select=int(input("Enter 1 to check by Pincode\nEnter 2 to check by District : \nEnter 3 to check by Pincode for next 7 days\nEnter 4 to check by District for next 7 days: \n"))
    if select==1:
        
        selectbypincode()
    else :
        selectbydistrict("z","z")
    end=time.time()
    print()
    print()
    print(end-start)    
        



