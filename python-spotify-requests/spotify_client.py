import base64
import datetime
from urllib.parse import urlencode
import requests


class SpotifyAPI(object):

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.access_token_expires = datetime.datetime.now()
        self.access_token_did_expire = True
        self.token_url = "https://accounts.spotify.com/api/token"

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret is None or client_id is None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        print("Client credentials encoded")
        return client_creds_b64.decode()

    def get_token_headers(self):
        """
        Returns token headers
        """
        client_creds_b64 = self.get_client_credentials()
        print("Token headers prepared")
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }

    @staticmethod
    def get_token_data():
        """
        :return:             "grant_type": "client_credentials"

        """
        return {
            "grant_type": "client_credentials"
        }

    def perform_auth(self):
        """
        :return: True if authorisation successful
        """
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        print("Sending request...")
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
        print("Access token received.")
        data = r.json()
        now = datetime.datetime.now()
        self.access_token = data['access_token']
        expires_in = data['expires_in']  # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        print("Authorization successful")
        return True

    def get_access_token(self):
        """
        :return: token
        """
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        print("\n"+"Check token ... ")
        if expires < now:
            print(f"Token is expired. Expiration date {expires} Request token ... ")
            self.perform_auth()
            return self.get_access_token()
        elif token is None:
            print("Token is undefined. Request token ... ")
            self.perform_auth()
            return self.get_access_token()
        print(f"Token is valid {token}.")
        return token

    def get_resource_header(self):
        """
        :return: header
        """
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_album(self, _id):
        return self.get_resource(_id, resource_type='albums')

    def get_artist(self, _id):
        return self.get_resource(_id, resource_type='artists')

    def base_search(self, query_params):  # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        print(f"Sending request {lookup_url} ....")
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            print(f"status code {r.status_code}")
            return {}
        replies = r.json()
        for reply in replies['tracks']['items']:
            print(f"Reply {reply['name']} {reply['type']}")
        return replies

    def search(self, query=None, operator=None, operator_query=None, search_type='artist'):
        if query is None:
            raise Exception("A query is required")
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k, v in query.items()])
        print(f"Query {query} is valid.")
        if operator is not None and operator_query is not None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        print(f"Query with operator {query} {operator} {operator_query} is valid.")
        query_params = urlencode({"q": query, "type": search_type.lower()})
        print(f"Query to request: {query_params}")
        return self.base_search(query_params)
