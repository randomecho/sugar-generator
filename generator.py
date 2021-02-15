import argparse
import faker
import logging
import requests
import os
import sys
import urllib
import yaml
from requests.exceptions import ConnectionError

import http.client
http.client._MAXHEADERS = 10000

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger('faker').setLevel(logging.ERROR)


class Sync:
    sugar_host = None
    username = None
    password = None
    config_file = 'config.yaml'
    oauth_token = None
    refresh_token = None
    auth_headers = None
    max_limit = 10


    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", dest="verbose",
            action='store_true', default=False,
            help="Toggle verbose mode - stdout or logfile")
        parser.add_argument("-m", dest="module",
            default='Accounts',
            help="Which module to create record in")
        parser.add_argument("-n", default='1',
            dest="max_num_to_create", metavar='number',
            help="How many records to create")
        parser.add_argument("-p", dest="prefix",
            help="Prefix of all generated records")
        parser.add_argument("-person", dest="person",
            action='store_true', default=False,
            help="Flag if person module or not")
        self.args = parser.parse_args()

        logging.basicConfig(filename='/tmp/sugar-generator.log',level=logging.DEBUG,format='%(asctime)s :: %(message)s')

        self.load_config()


    def generate_records(self):
        sync.logline("Generating...")

        requested_max_num = int(self.args.max_num_to_create,10)
        start_count = self.max_limit if requested_max_num > self.max_limit else requested_max_num
        fake = faker.Faker()
        prefix = self.args.prefix + ' ' if self.args.prefix != None else ''

        for x in range(start_count):
            payload = self.generate_payload(fake, prefix)
            r = requests.post(self.sugar_host + self.args.module, headers=self.auth_headers, json=payload)
            response = r.json()

            if 'id' in response and 'name' in response:
                self.logline("Created: {}/{} {}".format(self.args.module, response['id'], response['name']))
            else:
                self.logline("Error: {}".format(response))


    def generate_payload(self, fake, prefix):
        if self.args.person:
            fullname = fake.name().split(' ')
            payload = {
                'first_name': prefix+fullname[0],
                'last_name': fullname[1]
                }
        else:
            payload = {'name': prefix+fake.name()}

        return payload

    def load_config(self):
        try:
            with open(self.config_file) as config_file:
                config = yaml.safe_load(config_file)

            self.sugar_host = config['sugar']['host'] + '/rest/v11_1/'
            self.username = config['sugar']['username']
            self.password = config['sugar']['password']

        except FileNotFoundError:
            self.logline("Configuration file not found at: {}".format(self.config_file))
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
            self.logline("Logged in to {}".format(self.sugar_host))
        else:
            self.logline("! Could not log in")

        return


    def logline(self, line):
        if self.args.verbose:
            print(line)
        else:
            logging.info(line)


    def run(self):
        self.login()
        self.generate_records()


sync = Sync()
sync.run()
