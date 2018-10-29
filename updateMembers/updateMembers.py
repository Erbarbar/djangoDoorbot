import urllib.request as urllib
import json, requests
import schedule
import time
from bs4 import BeautifulSoup

debug = False

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
        #if(debug):
        print(ip.upper())
        pass
    return ip_slices

def createOpenMessage(*entering):
    msg = "A b3 está aberta! <https://jekb3.herokuapp.com/b3|:telescope:>\n"
    if(debug):
        print(entering[0])

    for j in entering[0]:
        msg += "["+j+"]"

    if(debug):
        print(msg)
    return msg

def createCloseMessage(*closing):
    msg = "A b3 está fechada! <https://jekb3.herokuapp.com/b3|:telescope:>\n"
    if(debug):
        print(closing[0])

    for j in closing[0]:
        msg += "["+j+"]"

    msg += "\nA porta ficou trancada? :thinking_face:"

    if(debug):
        print(msg)
    return msg

def createUpdateMessage(*updateJeker):
    msg = ''
    if(debug):
        print(updateJeker[0])

    for j in updateJeker[0]:
        msg += "["+j+"]"

    if(len(updateJeker[0])>1):
        msg += " Entraram na b3"
    else:
        msg += "\nEntrou na b3"

    if(debug):
        print(msg)
    return msg

def createEnterMessage(*updateJeker):
    msg = ''
    if(debug):
        print(updateJeker[0])

    for j in updateJeker[0]:
        msg += "["+j+"]"

    if(len(updateJeker[0])>1):
        msg += " Entraram na b3"
    else:
        msg += "\nEntrou na b3"

    if(debug):
        print(msg)
    return msg

def createLeaveMessage(*updateJeker):
    msg = ''
    if(debug):
        print(updateJeker[0])

    for j in updateJeker[0]:
        msg += "["+j+"]"

    if(len(updateJeker[0])>1):
        msg += " Sairam da b3"
    else:
        msg += "\nSaiu da b3"

    if(debug):
        print(msg)
    return msg

def sendMessage(*jeKers, action):
    channel = "#b3"
    if(action=="open"):
        msg = createOpenMessage(jeKers[0])
    if(action=="close"):
        msg = createCloseMessage(jeKers[0])
    if(action=="enter"):
        msg = createEnterMessage(jeKers[0])
        channel = "@erbarbar"
    if(action=="leave"):
        msg = createLeaveMessage(jeKers[0])
        channel = "@erbarbar"

    #webhook_url = "https://hooks.slack.com/services/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"
    webhook_url = "https://hooks.slack.com/services/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"
    payload = {
        "username" : "HoDoor", 
        "text" : msg, 
        "channel" : channel,
        #"icon_url":"https://pbs.twimg.com/profile_images/970049878465409024/ZmJw4bly_400x400.jpg",
        "icon_emoji" : ":b3:"
    }

    while True:
        try:
            m = requests.request("POST", webhook_url, auth=('admin','adminpass'), json=payload)
        except:
            if(debug):
                print("Error sending message to slack")
        else:
            break
    

def updatePresence(jeKers):
    
    ip_found = connectedDevices()

    # quem está a entrar na sala
    entering = []
    # quem está a sair da sala
    leaving = []

    before_inside_count = 0
    before_outside_count = 0

    after_inside_count = 0
    after_outside_count = 0

    # para cada jeKer na BD
    for j in jeKers:
        
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
                        if(debug):
                            print(e)

                    # actualiza local
                    j["presence"]=True
                    entering.append(j["name"])
                    sendMessage(entering, action="enter")
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
                if(debug):
                    print(e)

            # actualiza local
            j["presence"] = False
            leaving.append(j["name"])
            sendMessage(leaving, action="leave")

        # conta todos os que estão dentro
        if j["presence"]==True:
            after_inside_count += 1
        # conta todos os que estão fora
        if j["presence"]==False:
            after_outside_count += 1

    # se alguém entrar na sala vazia
    if before_inside_count==0 and after_inside_count>0:
        sendMessage(entering, action="open")

    if (before_inside_count>0 and after_inside_count==0):
        sendMessage(leaving, action="close")

def job1():
    updatePresence(jeKers)



url = "https://jekb3.herokuapp.com/api/jeKers/"
while True:
    try:
        jeKers = requests.request("GET",url, auth=('admin', 'adminpass')).json()
    except requests.exceptions.HTTPError as e:
        if(debug):
            print("Não consegue ler a base de dados")
        if(debug):
            print(e)
    else:
        updatePresence(jeKers)
        schedule.every(5).seconds.do(job1)
        break


while True:
    schedule.run_pending()
    time.sleep(1)

