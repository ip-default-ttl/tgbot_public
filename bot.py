import requests
from time import sleep
import datetime
import array

url="https://api.telegram.org/bot<token>/"

def get_chat_id(update):  
    chat_id = update['message']['chat']['id']
    return chat_id

def send_message(chat, text):  
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response

def get_message (request, msg_num):
    results = request['result']
    msg = request['result'][msg_num]['message']['text']
    return msg

def get_updates_json(request, offset_param):    
    params = {'timeout': 0, 'offset': offset_param}
    response = requests.get(request + 'getUpdates', data=params)
    return response.json()

def Ban_User(chat, user):
    now = datetime.datetime.now()
    if int(now.month) == 11:
        until = now.replace (month = 1)
        until = now.replace (year = int(now.year+1))
    else:
        until = now.replace(month = int(now.month+1))
    params = {
    'chat_id' : chat,
    'user_id' : user,
    'until_date' : until,
    'can_send_messages' : False,
    'can_send_media_messages': False,
    'can_send_polls': False,
    'can_send_other_messages': False,
    'can_add_web_page_previews': False,
    'can_change_info': False,
    'can_invite_users': False,
    'can_pin_messages': False
    }
    response = requests.post (url + 'restrictChatMember', data = params )

def main():
    offst=-1
    warnlist = []
    while True:
        our_json=get_updates_json(url,offst)
        while ('result' not in our_json):
            our_json=get_updates_json(url,offst)
            sleep (1)
        if (len(our_json['result'])==0):
            sleep (3)
            continue
        else:
            msg_last_num = len (our_json['result']) - 1
            for i in range ( 0 , msg_last_num+1 ):
                buf = our_json['result'][i]['message']
                if ('text' in buf):
                    txt = get_message (our_json,i)
                    if (txt == "/help") or (txt=="/help@ip_default_ttl_bot"):
                        send_message(get_chat_id(our_json['result'][i]),"Мануал еще не написан, все вопросы по боту к @ip_default_ttl")
                    elif (txt == "/flood") or (txt == "/flood@ip_default_ttl_bot"):
                        send_message(get_chat_id(our_json['result'][i]),"[ ! ] [ ! ] [ ! ] [ ! ] [ ! ] [ ! ] [ ! ] [ ! ] [ ! ] [ ! ] [ ! ] " "Беседа достигла границ флуда, прекращайте балаган и не злите админов :)")
                    elif (txt == "/grammar") or (txt == "/grammar@ip_default_ttl_bot"):
                        send_message(get_chat_id(our_json['result'][i]),"[ ! ] [ ! ] [ ! ] [ ! ] [ ! ] [ ! ] [ ! ] [ ! ] [ ! ] [ ! ] [ ! ] " "В этом чате уважают русский язык, пожалуйста, старайтесь писать грамотнее! ;) ")
                    elif (txt == "/iwantofp"):
                        flag1 = True #если вы знаете костыль получше этого, исправьте
                        if ('username' in our_json['result'][i]['message']['from']):
                            send_message(get_chat_id(our_json['result'][i]), "[ + ] @"+our_json['result'][i]['message']['from']['username']+" записался(-ась) на ОФП")
                            flag1 = False
                        elif ('last_name' in our_json['result'][i]['message']['from']) and flag1:
                            send_message(get_chat_id(our_json['result'][i]), "[ + ]"+our_json['result'][i]['message']['from']['first_name']+" "+our_json['result'][i]['message']['from']['last_name']+" записался(-ась) на ОФП")
                            flag1 = False
                        elif flag1:
                            send_message(get_chat_id(our_json['result'][i]), "[ + ] "+our_json['result'][i]['message']['from']['first_name']+" записался(-ась) на ОФП")
                        flag1 = True
                elif ('voice' in buf) and ( (buf['chat']['type']=='group') or (buf['chat']['type']=='supergroup')):
                    if (buf['from']['id'] in warnlist):
                        Ban_User(buf['chat']['id'], buf['from']['id'])
                        warnlist.remove(buf['from']['id'])
                        flag3= True
                        if ('username' in our_json['result'][i]['message']['from']):
                            send_message(get_chat_id(our_json['result'][i]), "[ + ] "+"@"+our_json['result'][i]['message']['from']['username']+" Забанен(-a) за голосовые сообщения")
                            flag3 = False
                        elif ('last_name' in our_json['result'][i]['message']['from']) and flag3:
                            send_message(get_chat_id(our_json['result'][i]), our_json['result'][i]['message']['from']['first_name']+" "+our_json['result'][i]['message']['from']['last_name']+" Забанен(-a) за голосовые сообщения")
                            flag3 = False
                        elif flag3:
                            send_message(get_chat_id(our_json['result'][i]), our_json['result'][i]['message']['from']['first_name']+" Забанен(-a) за голосовые сообщения")
                    else:
                        flag2 = True
                        if ('username' in our_json['result'][i]['message']['from']):
                            send_message(get_chat_id(our_json['result'][i]), "@"+our_json['result'][i]['message']['from']['username']+", голосовые сообщения не приветствуются в групповом чате. Пожалуйста продублируйте то же самое, но текстом. Спасибо за понимание! (Вам выдано предупреждение!)")
                            flag2 = False
                            warnlist.append(buf['from']['id'])
                        elif ('last_name' in our_json['result'][i]['message']['from']) and flag2:
                            send_message(get_chat_id(our_json['result'][i]), our_json['result'][i]['message']['from']['first_name']+" "+our_json['result'][i]['message']['from']['last_name']+", голосовые сообщения не приветствуются в групповом чате. Пожалуйста продублируйте то же самое, но текстом. Спасибо за понимание! (Вам выдано предупреждение!)")
                            flag2 = False
                            warnlist.append(buf['from']['id'])
                        elif flag2:
                            send_message(get_chat_id(our_json['result'][i]), our_json['result'][i]['message']['from']['first_name']+", голосовые сообщения не приветствуются в групповом чате. Пожалуйста продублируйте то же самое, но текстом. Спасибо за понимание! (Вам выдано предупреждение!)")
                            warnlist.append(buf['from']['id'])
                    flag2 = True
                    flag3=True
            offst = our_json['result'][msg_last_num]['update_id']
            offst += 1
            sleep (1)

if __name__ == '__main__':  
    main()
