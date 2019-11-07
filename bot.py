import requests
from time import sleep

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

def main():
    offst=-1
    while True:
        our_json=get_updates_json(url,offst)
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
                elif ('voice' in buf):
                    flag2 = True
                    if ('username' in our_json['result'][i]['message']['from']):
                        send_message(get_chat_id(our_json['result'][i]), "@"+our_json['result'][i]['message']['from']['username']+", голосовые сообщения не приветствуются в групповом чате. Пожалуйста продублируйте то же самое, но текстом. Спасибо за понимание!")
                        flag2 = False
                    elif ('last_name' in our_json['result'][i]['message']['from']) and flag2:
                        send_message(get_chat_id(our_json['result'][i]), our_json['result'][i]['message']['from']['first_name']+" "+our_json['result'][i]['message']['from']['last_name']+", голосовые сообщения не приветствуются в групповом чате. Пожалуйста продублируйте то же самое, но текстом. Спасибо за понимание!")
                        flag2 = False
                    elif flag2:
                        send_message(get_chat_id(our_json['result'][i]), our_json['result'][i]['message']['from']['first_name']+", голосовые сообщения не приветствуются в групповом чате. Пожалуйста продублируйте то же самое, но текстом. Спасибо за понимание!")
                    flag2 = True
            offst = our_json['result'][msg_last_num]['update_id']
            offst += 1
            sleep (1)

if __name__ == '__main__':  
    main()
