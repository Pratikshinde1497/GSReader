from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

def createHie(dist, arr):
    for i in range(len(arr)):
        ele = arr[i]
        if ele not in dist:
            dist[ele] = {}
        arr.pop(i)
        dist[ele] = createHie(dist[ele], arr)
        return dist


def createTree(values):
    keys = []
    d = {}
    for i in range(len(values)):
        arr = values[i][4].split('.')
        keys.append(arr)
    for i in range(len(keys)):
        d = createHie(d, keys[i])
    return d


def saveJSON(filename, object):
    try:
        file_object = open(filename, 'w')
        dict_object = object
        # Save dict data into the JSON file.
        json.dump(dict_object, file_object)
        print(filename + " created. ")    
    except FileNotFoundError:
        print(filename + " not found. ") 


def readJSON(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def PutValue(obj, chain, val):
    _key = chain.pop(0)
    if _key in obj:
        obj[_key] = val if obj[_key] is None else PutValue(obj[_key], chain, val)
    return obj


def CreateLangFile(values, lang):
    data = readJSON('JsonTree.json')
    d = {}
    if lang == 'en': 
        l = 1
    elif lang == 'fn':
        l = 2
    else :
        l = 3
    for i in range(len((values))):
        ref = values[i][4]
        lang_val = values[i][l]
        d[lang] = PutValue(data, ref.split('.'), lang_val)
    print(d)
    saveJSON('languages/p'+lang+'.json', d)



# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1dQmJaod_3Bmhu0BX3gK55a_j73UqsY_NdG_3R-AGPOs'
SAMPLE_RANGE_NAME = 'Users!A2:E7'



def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    filename = 'JsonTree.json'
    
    """ ---------------------------- """
    """ Creating a Json file With the Tree of Hierarchy String in the GSheet 4th column"""
    
    # tree = createTree(values)
    # saveJSON(filename, tree)
    
    """ ---------------------------- """
    
    CreateLangFile(values, 'en')
    
if __name__ == '__main__':
    main()
