import urllib.request as urllib
import json, requests
import schedule
import time
from bs4 import BeautifulSoup


def sumPrior(i,arr):
    res = 0
    while i>=0:
        res += arr[i]
        i -= 1
    return res

def returnSlices(text, startString, endString):
    numberOfTables = min(text.count(startString),text.count(endString))
    aux_text = text
    start = [0]*numberOfTables
    end = start
    text_slice = [None] * numberOfTables
    i = 0
    while i<numberOfTables:
        start[i] = aux_text.find(startString)
        aux_text = aux_text[start[i]+len(startString):]
        end[i] = aux_text.find(endString)
        text_slice[i] = aux_text[:end[i]]
        i += 1
    return text_slice

def connectedDevices():

    url = "http://192.168.1.1/"

    page = urllib.urlopen(url).read()
    soup = BeautifulSoup(page, "html.parser")

    data = soup.find_all('script', attrs={'type':'text/javascript'})
    text = str(data[7])

    text_slices = returnSlices(text, "setWirelessTable(", ");")

    text = text_slices[1]

    ip_slices = returnSlices(text,"xx:xx:xx:xx:", "','")

    for ip in ip_slices:
        print(ip.upper())

    return ip_slices

def sendMessage(*entering, entering_counter):

    msg = "A b3 está aberta! <https://jekb3.herokuapp.com/b3|:telescope:>\n"

    while(entering_counter>0):
        entering_counter -= 1
        msg += "["+entering[0][entering_counter]+"]"

    # webhook_url = "https://hooks.slack.com/services/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"
    webhook_url = "https://hooks.slack.com/services/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"
    payload= {
        "username":"HoDoor", 
        "text":msg, 
        "channel":"@erbarbar",
        "icon_url":"https://pbs.twimg.com/profile_images/970049878465409024/ZmJw4bly_400x400.jpg",
        # "icon_emoji":":b3:"
        }
    m = requests.request("POST", webhook_url, auth=('admin','adminpass'), json=payload)


# ip_found = connectedDevices()

ip_found=[
"7C:00",
"8A:D6",
"BE:CA",
"qw:we"]

def updatePresence():
    url = "https://jekb3.herokuapp.com/api/jeKers/"
    r = requests.request("GET",url, auth=('admin', 'adminpass'))

    previous_presence = 0

    # quem está a entrar na sala
    entering = [None]*len(ip_found)
    entering_counter = 0

    # para cada jeKer na BD
    for j in r.json():
        found = False
        # para cada ip encontrado
        for ip in ip_found:
            # confirma-se que o jeKer está na sala
            if(j["mac_address"].upper()==ip.upper()):
                found = True
                # se o jeKer estiver como ausente na Bd, quer dizer que acabou de entrar na b3
                if(j["presence"]==False):
                    # actualiza a BD
                    s = requests.request("PATCH", url+str(j['id'])+"/", auth=('admin', 'adminpass'), data={'presence':'True'})
                    print("%s entrou na B3"%(j["name"]))
                    entering[entering_counter] = j["name"]
                    entering_counter += 1
                # se o jeKer já estiver como presente, quer dizer que não entrou neste ciclo
                if(j["presence"]==True):
                    previous_presence += 1
        # se nao está na sala, mas na BD está, quer dizer que saiu
        if (found==False and j["presence"]==True):
            s = requests.request("PATCH", url+str(j['id'])+"/", auth=('admin', 'adminpass'), data={'presence':'False'})
            print("%s saiu da B3"%(j["name"]))

    # se alguém entrar na sala vazia
    if previous_presence==0 and entering_counter>0:
        sendMessage(entering,entering_counter=entering_counter)

def job():
    updatePresence()

updatePresence()
schedule.every().minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
