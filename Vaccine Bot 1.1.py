# Importing necessary modules
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import ast
from datetime import date
import datetime
def typecast(s):
    return ast.literal_eval(s)
def find_city(pincode):
    import requests
    from lxml import html 
    url= "https://pincode.net.in/"
    url+=pincode
    path = '//*[@id="content"]/div[2]/div/a[2]'
    response = requests.get(url)
    byte_data = response.content
    source_code = html.fromstring(byte_data)
    try:
        tree = source_code.xpath(path)
        city=(tree[0].text_content())
        code=0
    except:
        code=1
        city=("Data for Pincode does not exist.")
    return [code,city]

def get_date():
    today = date.today()
    today = str(today.strftime("%d/%m/%Y"))
    return today
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
    pincode="281001"
    fcity=find_city(pincode)
    city,code=fcity[1],fcity[0]
    print(city)
    if code==0:
        sdata=get_by_pincode(pincode)
        sdata=organise(sdata)
        s18,s45=sdata[0],sdata[1]


        print("Vaccines Available!!")
        print("details : ")



