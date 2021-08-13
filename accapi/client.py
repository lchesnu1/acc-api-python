from .token import AccToken
import requests


class AccClientFactory:
    def __init__(self, user_nonce, user_key):
        self._token = AccToken(user_nonce, user_key)

    def create(self, address, username, password, client_name="Python client"):
        response = _query("POST", _url(address, "login"), json={
            "authorizationToken": self._token.generate(),
            "username": username,
            "password": password,
            "clientName": client_name
        })
        return AccClient(address, response['session'])


class AccClient:
    def __init__(self, address, session):
        self.address = address
        self.session = session

    def get_cameras(self, verbosity="LOW"):
        response = _query("GET", _url(self.address, "cameras"), {
            "verbosity": verbosity,
            "session": self.session
        })
        return response["cameras"]
    
    def get_servers(self):                                           
        response = _query("GET", _url(self.address, "server/ids"), { 
            "session": self.session                                  
        })                                                           
        return response["servers"]
    
    def destroy(self):
        # logs out session
        response = requests.request("POST", _url(self.address, "logout"), params=None,json={"session": self.session} , verify=False)
        response.raise_for_status()
        response_data = response.json()
        return response


def _url(address, path):
    return f"{address}/mt/api/rest/v1/{path}"


def _query(method, url, params=None, json=None):
    response = requests.request(
        method, url, params=params, json=json, verify=False)
    response.raise_for_status()
    response_data = response.json()
    if (response_data["status"] != "success"):
        raise Exception(response_data["status"])
    return response_data["result"]
