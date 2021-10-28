import json
import requests


getUrlApiWhats = "https://v4.chatpro.com.br/chatpro-z9unpb0pg0/api/v1/send_message"
getAuthorization = "fa0324ee59e6ffca9b24a9462d20c6088f3b547a"

ativarEnvio = True
ativarLog = True


def sendMessage(message, number):

    global ativarEnvio

    url = f'{getUrlApiWhats}'
    payload = {'message': f'{message}',
               'number': f'{number}'}
    headers = {'content-type': 'application/json',
               'accept': 'application/json',
               'Authorization': f'{getAuthorization}'}

    return requests.post(url, data=json.dumps(payload), headers=headers)


def sendMessageLog(message, number):

    global ativarLog

    if ativarLog:
        return sendMessage(message, number)
    else:
        return False


def sendMessageAlert(message, number):

    global ativarEnvio

    if ativarEnvio:
        return sendMessage(message, number)
    else:
        return False
