# Importing necessary modules
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import ast
from datetime import date
import datetime
pincode="281001"

today = date.today()
today = today.strftime("%d/%m/%Y")
url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+pincode+"&date="+str(today)
# WebDriver Chrome
driver = webdriver.Chrome(ChromeDriverManager().install())

# Target URL
driver.get(url)

# print(driver.title)

# Printing the whole body text
s=(driver.find_element_by_xpath("/html/body").text)
driver.close()
s=s[12:-1]
s=ast.literal_eval(s)
print("Vaccines Available!!")
print("details : ")
print(type(s))
for i in s:
    print(type(i))
    #print(i["name"],"(",i["min_age_limit"],"+) : ",i["available_capacity"])
# Closing the driver



