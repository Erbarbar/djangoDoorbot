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
    while True:
        try:
            url_open = urllib.urlopen(url)
        except:
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
        #print(ip.upper())
        pass
    return ip_slices

def createOpenMessage(*entering):
    msg = "A b3 está aberta! <https://jekb3.herokuapp.com/b3|:telescope:>\n"
    print(entering[0])

    for j in entering[0]:
        msg += "["+j+"]"

    print(msg)
    return msg

def createCloseMessage(*closing):
    msg = "A b3 está fechada! <https://jekb3.herokuapp.com/b3|:telescope:>\n"
    print(closing[0])

    for j in closing[0]:
        msg += "["+j+"]"

    msg += "\nA porta ficou trancada? :thinking_face:"

    print(msg)
    return msg



def sendMessage(*jeKers, action):

    if(action=="open"):
        msg = createOpenMessage(jeKers[0])
    if(action=="close"):
        msg = createCloseMessage(jeKers[0])

    #webhook_url = "https://hooks.slack.com/services/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"
    webhook_url = "https://hooks.slack.com/services/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"
    payload= {
        "username":"HoDoor", 
        "text":msg, 
        "channel":"@erbarbar",
        #"icon_url":"https://pbs.twimg.com/profile_images/970049878465409024/ZmJw4bly_400x400.jpg",
        "icon_emoji":":b3:"
        }
    while True:
        try:
            m = requests.request("POST", webhook_url, auth=('admin','adminpass'), json=payload)
        except:
            print("Error sending message to slack")
        else:
            break
    


# ip_found=[
#  "7C:00",
#  "8A:D6",
#  "BE:CA",
#  "qw:we"]

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
                        print("Erro a fazer patch [presence: True]")
                        print(e)

                    # actualiza local
                    print("%s entrou na B3"%(j["name"]))
                    j["presence"]=True
                    entering.append(j["name"])
                # se o jeKer já estiver como presente, quer dizer que não entrou neste ciclo
                if(j["presence"]==True):
                    pass
        # se nao está na sala, mas na BD está, quer dizer que saiu
        if (found==False and j["presence"]==True):
            # actualiza BD
            try:
                s = requests.request("PATCH", url+str(j['id'])+"/", auth=('admin', 'adminpass'), data={'presence':'False'})
            except requests.exceptions.HTTPError as e:
                print("Erro a fazer patch [presence: False]")
                print(e)

            # actualiza local
            print("%s saiu da B3"%(j["name"]))
            j["presence"] = False
            leaving.append(j["name"])

        # conta todos os que estão dentro
        if j["presence"]==True:
            after_inside_count += 1
        # conta todos os que estão fora
        if j["presence"]==False:
            after_outside_count += 1

    print("inside: %s -> %s" %(before_inside_count,after_inside_count))
    print("outside: %s -> %s"%(before_outside_count, after_outside_count))
    # se alguém entrar na sala vazia
    if before_inside_count==0 and after_inside_count>0:
        sendMessage(entering, action="open")

    if (before_inside_count>0 and after_inside_count==0):
        sendMessage(leaving, action="close")

def job1():
    print("------------")
    updatePresence(jeKers)

def job2():
    webhook_url = "https://hooks.slack.com/services/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"
    payload= {
        "username":"HoDoor", 
        "text":"up", 
        "channel":"@erbarbar",
        #"icon_url":"https://pbs.twimg.com/profile_images/970049878465409024/ZmJw4bly_400x400.jpg",
        "icon_emoji":":b3:"
        }
    while True:
        try:
            m = requests.request("POST", webhook_url, auth=('admin','adminpass'), json=payload)
        except:
            print("Error sending message to slack")
        else:
            break

url = "https://jekb3.herokuapp.com/api/jeKers/"
while True:
    try:
        jeKers = requests.request("GET",url, auth=('admin', 'adminpass')).json()
    except requests.exceptions.HTTPError as e:
        print("Não consegue ler a base de dados")
        print(e)
    else:
        updatePresence(jeKers)
        schedule.every(5).seconds.do(job1)
        schedule.every(30).minutes.do(job2)
        break


while True:
    schedule.run_pending()
    time.sleep(1)

