import requests


def getViaCep(cep):

    url = f"https://viacep.com.br/ws/{cep}/json/"

    payload = ""
    return requests.request("GET", url, data=payload)



