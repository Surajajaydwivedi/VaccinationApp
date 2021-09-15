import os
# Importing necessary modules
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import ast
from datetime import date
import datetime
def typecast(s):
    return ast.literal_eval(s)
''''''
def find_city(pincode):
    import requests
    from lxml import html 
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
def getdists(addr):
    try:
        fdistricts = open((addr)+"DistDef.txt","r+")
    except:
        fdistricts = open((addr)+"DistDef.txt","w+")
        fdistricts.write(',')
        fdistricts.close()
        fdistricts = open(addr+"DistDef.txt","r+")
    try:
        dists="{"+fdistricts.read()[1:-1]+"}"
    except:
        fdistricts = open((addr)+"DistDef.txt","w+")
        fdistricts.write(',')
        fdistricts.close()
        fdistricts = open(addr+"DistDef.txt","r+")
        dists="{"+fdistricts.read()[1:-1]+"}"
    dists=typecast(dists)
    if type(dists) is not dict:
        fdistricts = open((addr)+"DistDef.txt","w+")
        fdistricts.write(',')
        fdistricts.close()
        fdistricts = open(addr+"DistDef.txt","r+")
        dists="{"+fdistricts.read()[1:-1]+"}"
        dists=typecast(dists)
    return [dists,fdistricts]
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

def url_by_pincode(today,pincode):
    return ("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+pincode+"&date="+today)
# WebDriver Chrome
def get_by_pincode(pincode):
    url=url_by_pincode(get_date(),pincode)
    

    driver = webdriver.Chrome(ChromeDriverManager().install())

# Target URL
    driver.get(url)

# print(driver.title)

# Printing the whole body text
    s=(driver.find_element_by_xpath("/html/body").text)
    driver.close()
    return s
def organise(s):
    s=s[12:-1]
    s=typecast(s)
    print(type(s),s)
    s18=[]
    s45=[]
    for i in s:
        if i["min_age_limit"]==45:
            s45.append(i)
        else:
            s18.append(i)
        #print(i["name"],"(",i["min_age_limit"],"+) : ",i["available_capacity"])
    print(s18,len(s45))
    return [s18,s45]
# Closing the driver
if __name__=="__main__":
    print("WEW")
    pincode="208014"
    '''fcity=find_city(pincode)
    city,state,code=fcity[1],fcity[0]
    city=city.upper()
    print(city)'''
    if 0==0:
        sdata=get_by_pincode(pincode)
        sdata=organise(sdata)
        s18,s45=sdata[0],sdata[1]
        pins,fpins=getpins(getaddr())
        try:
            city=pins[pincode]
        except:
            fcity=find_city(pincode)
            city,state,code=fcity[2],fcity[1],fcity[0]
            city=city.upper()
            print(city)
            fpins.write('"'+pincode+'" : "'+city+'" ,')
        fpins.close()
        distr,fdis=getdists(getaddr())
        try:
            er=distr[city]
        except:
            fdis.write('"'+city+'" : "1" ,')
        fdis.close()
        print("Vaccines Available!!")
        print("details : ")



