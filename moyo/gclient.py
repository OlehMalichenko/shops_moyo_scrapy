import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

class Gclient(object):

    def __init__(self):
        self.client = self.create_client()


    def create_client(self):
        scope = ['https://spreadsheets.google.com/feeds']
        path = os.getcwd() + '\client_secret.json'
        creds = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
        return gspread.authorize(creds)


    def get_sheet(self):
        return self.client.open_by_key('1jOu6L8066TcWcC2dft5SvFK1IDzMG6QU2JJ7X_l6I7o').get_worksheet(0)

