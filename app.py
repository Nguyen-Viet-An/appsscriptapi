"""
Shows basic usage of the Apps Script API.
Call the Apps Script API to create a new script project, upload a file to the
project, and log the script's URL to the user.
"""
from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors
from googleapiclient.discovery import build

import time
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/script.projects']

SAMPLE_CODE = '''
function install() {
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    ScriptApp.deleteTrigger(triggers[i]);
  }
  ScriptApp.newTrigger('GetandSetProperty.locationOnEdit').forSpreadsheet(SpreadsheetApp.getActive()).onEdit().create();
  ScriptApp.newTrigger('GetandSetProperty.lithOnEdit').forSpreadsheet(SpreadsheetApp.getActive()).onEdit().create();
  // getCoreLogging();
  var ss = SpreadsheetApp.getActiveSpreadsheet()
  ss.deleteActiveSheet();
  //Browser.msgBox("Installed sucessfully");
  // PropertiesService.getScriptProperties().setProperty('key', 'installed correctly');
}
'''.strip()

SAMPLE_MANIFEST = '''
{
  "timeZone": "Australia/Adelaide",
  "dependencies": {
    "enabledAdvancedServices": [
      {
        "userSymbol": "Drive",
        "serviceId": "drive",
        "version": "v2"
      }
    ],
    "libraries": [
      {
        "userSymbol": "GetandSetProperty",
        "version": "0",
        "libraryId": "15eHrt4uWZP1Gy2b2xJ_alHWIHtnUOoOKmOnLVuta40P9SdxSHqhbFjb8",
        "developmentMode": true
      }
    ]
  },
  "exceptionLogging": "STACKDRIVER",
  "oauthScopes": [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/script.container.ui",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/script.external_request",
    "https://www.googleapis.com/auth/script.scriptapp"
  ],
  "runtimeVersion": "V8"
}
'''.strip()
def callback(request_id, response, exception):
  if exception is not None:
    print(exception)
  else:
    print(response['scriptId'])


def main():
    """Calls the Apps Script API.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        tic = time.perf_counter()
        service = build('script', 'v1', credentials=creds)
        batch = service.new_batch_http_request()


        
        # Call the Apps Script API
        # Create a new project
        
        sheetIds =  ['1XgAlL-HaBQ9h5xAaU6E1Tomu_6BqzRj6Pi6XkrQgQvo', '1jwO2WAg5nFIiGv1WHD1JsQLkPDVdguBVhR8khlnwfB8', '1ygG7WNIrgK6DaCO3hSPgy7edz8Z3akgXMjwS1h0xR_Q', '1u6ReCG1DJBBUO2NMyp_R9ongtPGW0T8cyK0ITIEQHZw', '1oPiwWOPi4zsm0dpli0FSau8XvLeKV97O2x2A7HlTrUs', '1uZBXHnxZzxx2ZbXkKzswTKUUf7UwA6yphUuqsBpuRKE', '1wpySFHMOzYKHVl3Wn66jci8Cvhh9Oac7vypNUEspXjI', '1D5oaqrhGe66eK2Xco7W702IC6wbUw4re8Nqpses2gZw', '1G53YM6quQsHdHBKdKE9vrCY4mYmei3B8L7F1F-znAfE', '1x8gyyNicQedJTC5Eva4T6D9xuh5c1yyhG0j3Xfg-b6s', '124dXODFEnMBGtMN8IpgYyRF7nZAVIegNkJ48Euecgk8']
        for id in sheetIds:
            script_body = {'title': 'Core Logging',
                           'parentId': id}
            request = service.projects().create(body=script_body) 
            batch.add(request, callback)
        
        batch.execute()

        # response = service.projects().create(body=request).execute()
        # print(response['scriptId'])
        tok = time.perf_counter()
        print("done in {}s".format(tok-tic))
        # Upload two files to the project
        request = {
            'files': [{
                'name': 'Code',
                'type': 'SERVER_JS',
                'source': SAMPLE_CODE
            }, {
                'name': 'appsscript',
                'type': 'JSON',
                'source': SAMPLE_MANIFEST
            }]
        }
        response = service.projects().updateContent(
            body=request,
            scriptId=response['scriptId'][0]).execute()
        print('https://script.google.com/d/' + response['scriptId'] + '/edit')
    except errors.HttpError as error:
        # The API encountered a problem.
        print(error.content)


if __name__ == '__main__':
    main()