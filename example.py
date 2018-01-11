"""
Simple example code to communicate with Power BI REST API.

(c) Emmanuel Prochasson, Omnistream 2018
Licence: MIT
"""
import requests


# Configuration goes here:
RESOURCE = "https://analysis.windows.net/powerbi/api"  # Don't change that.
APPLICATION_ID = "abcdef-abcdef-abcdef-abcdef"  # The ID of the application in Active Directory
APPLICATION_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxx"  # A valid key for that application in Active Directory

USER_ID = "emmanuel@your_company.com"  # A user that has access to PowerBI and the application
USER_PASSWORD = "password"  # The password for that user

GROUP_ID = 'xxxxxxxxxxx'  # The id of the workspace containing the report you want to embed
REPORT_ID = 'xxxxxxxxxxxxxx'  # The id of the report you want to embed


def get_access_token(application_id, application_secret, user_id, user_password):
    data = {
        'grant_type': 'password',
        'scope': 'openid',
        'resource': "https://analysis.windows.net/powerbi/api",
        'client_id': application_id,
        'client_secret': application_secret,
        'username': user_id,
        'password': user_password
    }
    token = requests.post("https://login.microsoftonline.com/common/oauth2/token", data=data)
    assert token.status_code == 200, "Fail to retrieve token: {}".format(token.text)
    print("Got access token: ")
    print(token.json())
    return token.json()['access_token']


def make_headers(application_id, application_secret, user_id, user_password):
    return {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': "Bearer {}".format(get_access_token(application_id, application_secret, user_id, user_password))
    }


def get_embed_token_report(application_id, application_secret, user_id, user_password, group_id, report_id):
    endpoint = "https://api.powerbi.com/v1.0/myorg/groups/{}/reports/{}/GenerateToken".format(group_id, report_id)
    headers = make_headers(application_id, application_secret, user_id, user_password)
    res = requests.post(endpoint, headers=headers, json={"accessLevel": "View"})
    return res
    print(res.json())
    return res.json()['token']


def get_groups(application_id, application_secret, user_id, user_password):
    endpoint = "https://api.powerbi.com/v1.0/myorg/groups"
    headers = make_headers(application_id, application_secret, user_id, user_password)
    return requests.get(endpoint, headers=headers).json()


def get_dashboards(application_id, application_secret, user_id, user_password, group_id):
    endpoint = "https://api.powerbi.com/v1.0/myorg/groups/{}/dashboards".format(group_id)
    headers = make_headers(application_id, application_secret, user_id, user_password)
    return requests.get(endpoint, headers=headers).json()


def get_reports(application_id, application_secret, user_id, user_password, group_id):
    endpoint = "https://api.powerbi.com/v1.0/myorg/groups/{}/reports".format(group_id)
    headers = make_headers(application_id, application_secret, user_id, user_password)
    return requests.get(endpoint, headers=headers).json()


# ex:
# get_embed_token_report(APPLICATION_ID, APPLICATION_SECRET, USER_ID, USER_PASSWORD, GROUP_ID, REPORT_ID)
