import requests


def getViaCep(cep):

    url = f"https://viacep.com.br/ws/{cep}/json/"

    payload = ""
    try:
        res = requests.request("GET", url, data=payload)
    except Exception as e:
        return False

    return res



