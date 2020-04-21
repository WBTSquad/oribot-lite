import requests


async def mcsrv(host):
    endpoint = 'https://api.mcsrvstat.us/2/'
    url = endpoint + host
    resp = requests.get(url=url)
    data = resp.json()
    return data