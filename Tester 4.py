
import os
def cmd(s):
    ss='cmd /c '
    ss+='"'+s+'"'
    os.system(s)
os.system('cmd /c "python -m pip install --upgrade pip"')
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
    from datetime import date
except:
    cmd("pip install DateTime")
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
import datetime

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

#Web Drivers
def drive(url):
    driver.get(url)
    s=(driver.find_element_by_xpath("/html/body").text)
    return s
def calendarbypincode(pincode):
    url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="+pincode+"&date="+get_date()
    return(drive(url))
def organcalpin(s):
    s=typecast(s)
    s18=[{}]
    s45=[{}]
    d145=0
    d245=0
    d118=0
    d218=0
    for i in s["centers"]:
        i['address']+=", "+i['block_name']+", "+i['district_name']+", "+str(i['pincode'])
        for ii in i["sessions"]:
            if ii["min_age_limit"]==45:
                d145+=ii["available_capacity_dose1"]
                d245+=ii["available_capacity_dose2"]
                


s=calendarbypincode("281001")

print(type(s))
for i in s:
    print(type(i))
    print(i)
