import requests
import logging
import os
import sys
import urllib
import yaml
from requests.exceptions import ConnectionError

import http.client
http.client._MAXHEADERS = 10000

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class Sync:
    sugar_host = None
    username = None
    password = None
    config_file = 'config.yaml'
    oauth_token = None
    refresh_token = None
    auth_headers = None
    bulk_limit = 200


    def __init__(self):
        logging.basicConfig(filename='/tmp/sugar-generator.log',level=logging.DEBUG,format='%(asctime)s :: %(message)s')

        self.load_config()


    def generate_records(self):
        pass


    def load_config(self):
        try:
            with open(self.config_file) as config_file:
                config = yaml.safe_load(config_file)

            self.sugar_host = config['sugar']['host'] + '/rest/v11_1/'
            self.username = config['sugar']['username']
            self.password = config['sugar']['password']

        except FileNotFoundError:
            print("Configuration file not found at: {}".format(self.config_file))
            exit(1)


    def login(self):
        data = {
                "grant_type": "password",
                "client_id": "sugar",
                "client_secret": "",
                "username": self.username,
                "password": self.password,
                "platform": "base"
            }

        r = requests.post(self.sugar_host + 'oauth2/token', json=data)
        response = r.json()

        if 'access_token' in response and response['access_token'] != None:
            self.oauth_token = response['access_token']
            self.refresh_token = response['refresh_token']
            self.auth_headers = {'OAuth-Token': self.oauth_token, 'Content-Type': 'application/json'}
            logging.info("=== Logged in to {}".format(self.sugar_host))
        else:
            logging.info("!!! Could not log in")

        return


    def run(self):
        self.login()
        self.generate_records()


sync = Sync()
print("\n= Generating...")
sync.run()
