import urllib.request as urllib
import json, requests
import schedule
import time
from bs4 import BeautifulSoup

debug = False
jeKers = []






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
    if(debug):
        print("connectedDevices")
    url = "http://192.168.1.1/"
    while True:
        try:
            url_open = urllib.urlopen(url)
        except:
            if(debug):
                print("Error accessing b3, trying again")
        else:
            break

    page = url_open.read()
    soup = BeautifulSoup(page, "html.parser")

    data = soup.find_all('script', attrs={'type':'text/javascript'})
    text = str(data[7])

    text_slices = returnSlices(text, "setWirelessTable(", ");")

    text = text_slices[1]

    ip_slices = returnSlices(text,"xx:xx:xx:xx:", "','")

    for ip in ip_slices:
        if(debug):
            print(ip.upper())
        pass

    if(debug):
        print("---")
    return ip_slices


def sendMessage(jeKer, action):
    channel = "@" + jeKer

    #webhook_url = "https://hooks.slack.com/services/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"
    webhook_url = "https://hooks.slack.com/services/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"
    payload = {
        "username" : "Door BOT", 
        "text" : "Foste a ultima pessoa a sair da b3, a porta ficou trancada?", 
        "channel" : channel,
        "icon_url":"https://pbs.twimg.com/profile_images/970049878465409024/ZmJw4bly_400x400.jpg",
        #"icon_emoji" : ":b3:"
    }

    while True:
        try:
            m = requests.request("POST", webhook_url, auth=('admin','adminpass'), json=payload)
        except:
            if(debug):
                print("Error sending message to slack")
        else:
            break
    

def updatePresence(jeK):
    if(debug):
        print("updatePresence")
    ip_found = connectedDevices()
    # quem está a entrar na sala
    entering = []
    # quem está a sair da sala
    leaving = []

    before_inside_count = 0
    before_outside_count = 0

    after_inside_count = 0
    after_outside_count = 0

    changes = False

    # para cada jeKer na BD
    for j in jeK:
        # conta todos os que estavam dentro
        if j["presence"]==True:
            before_inside_count += 1
        # conta todos os que estavam fora
        if j["presence"]==False:
            before_outside_count += 1
            
        found = False
        # para cada ip encontrado
        for ip in ip_found:
            # confirma-se que o jeKer está na sala
            if(j["mac_address"].upper()==ip.upper()):
                found = True
                # se o jeKer estiver como ausente na Bd, quer dizer que acabou de entrar na b3
                if(j["presence"]==False):
                    # actualiza a BD
                    try:
                        s = requests.request("PATCH", url+str(j['id'])+"/", auth=('admin', 'adminpass'), data={'presence':'True'})
                    except requests.exceptions.HTTPError as e:
                        if(debug):
                            print("Erro a fazer patch [presence: True]")
                            print(e)

                    # actualiza local
                    j["presence"]=True
                    entering.append(j["name"])
                    changes = True
                    print(time.strftime("[%x] %X - ") + j["name"] + " entrou")
                    #sendMessage(entering, action="enter")
                # se o jeKer já estiver como presente, quer dizer que não entrou neste ciclo
                if(j["presence"]==True):
                    pass
        # se nao está na sala, mas na BD está, quer dizer que saiu
        if (found==False and j["presence"]==True):
            # actualiza BD
            try:
                s = requests.request("PATCH", url+str(j['id'])+"/", auth=('admin', 'adminpass'), data={'presence':'False'})
            except requests.exceptions.HTTPError as e:
                if(debug):
                    print("Erro a fazer patch [presence: False]")
                    print(e)

            # actualiza local
            j["presence"] = False
            leaving.append(j["name"])
            changes = True
            print(time.strftime("[%x] %X - ") + j["name"] + " saiu")
            #sendMessage(leaving, action="leave")

        # conta todos os que estão dentro
        if j["presence"]==True:
            after_inside_count += 1
        # conta todos os que estão fora
        if j["presence"]==False:
            after_outside_count += 1

    # se alguém entrar na sala vazia
    if before_inside_count==0 and after_inside_count>0:
        #sendMessage(entering, action="open")
        if(debug):
            print("B3 aberta")
        pass

    if (before_inside_count>0 and after_inside_count==0):
        #for leaver in leaving:
            #sendMessage(leaver, action="close")
        print("B3 fechada")
        #sendMessage(leaving, action="close")

    if(changes):
        jeKers = getJeKers()


def getJeKers():
    while True:
        try:
            jeKers = requests.request("GET",url, auth=('admin', 'adminpass')).json()
        except requests.exceptions.HTTPError as e:
            if(debug):
                print("Não consegue ler a base de dados")
                print(e)
        else:
            if(debug):
                for j in jeKers:
                    print(j["name"] + "->" + j["mac_address"])
                print("----------")
            break
    return jeKers


def job1():
    updatePresence(jeKers)


url = "https://jekb3.herokuapp.com/api/jeKers/"
jeKers = getJeKers()
job1()
schedule.every(5).seconds.do(job1)


while True:
    schedule.run_pending()
    time.sleep(1)