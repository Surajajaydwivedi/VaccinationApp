import os
def cmd(s):
    ss='cmd /c '
    ss+='"'+s+'"'
    os.system(s)
os.system('cmd /c "python -m pip install --upgrade pip"')
cmd("pip install geocoder")
import geocoder
g = geocoder.ip('me')
print(g.latlng)