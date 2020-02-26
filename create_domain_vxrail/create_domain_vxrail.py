#Create WLD
import requests
import json
import sys
import time


def get_request(url,username,password):
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers,auth=(username, password))
    if(response.status_code == 200):
        data = json.loads(response.text)
    else:
        print ("Error reaching the server.")
        exit(1)
    return data

def post_request(data,url,username,password):
    headers = {'Content-Type': 'application/json'}
    print (url)
    print (data)
    response = requests.post(url, headers=headers, json=data, auth=(username, password))
    if(response.status_code == 200 or response.status_code == 202):
        data = json.loads(response.text)
    else:
        print ("Error reaching the server.")
        response = json.loads(response.text)
        print (json.dumps(response,indent=4, sort_keys=True))
        exit(1)
    return data


def poll_on_id(url,username,password):
    status = get_request(url,username,password)['status']
    c = 0
    while(status == 'In Progress' or status == 'Pending'):
        c = c+1
        n = c%6
        print ("\rOperation in progress" + "."*n + " "*(5-n),end = "")
        status = get_request(url,username,password)['status']
        time.sleep(5)
    print ("")
    return status


def create_workload_domain(hostname,username,password):
    data = read_input()
    validationUrl =  hostname+'/domainmanager/v1/domains/validations/creations'
    response = post_request(data,validationUrl,username,password)
    print ('Validating the input....')
    if(response['executionStatus'] == 'COMPLETED' and response['resultStatus'] == 'SUCCEEDED'):
        print ('Validation Succeeded.')
    else:
        print ('Validation failed.')
        print (json.dumps(response,indent=4, sort_keys=True))
        exit(0)
    postUrl = hostname + '/domainmanager/v1/domains'
    response = post_request(data,postUrl,username,password)
    print ('Creating Domain...')
    task_id = response['id']
    taskUrl = hostname+'/v1/tasks/'+task_id
    result = poll_on_id(taskUrl,username,password)
    if(result == 'SUCCESSFUL'):
        print ('Successfully created Domain.')
    else:
        print ('Domain Creation failed.')
        print (json.dumps(response,indent=4, sort_keys=True))
        print (result)


def read_input():
    with open('domain_creation_spec_vxrail.json') as json_file:
        data = json.load(json_file)
        return data

def get_help():
    help_description = '''\n\t\t----Create Domain----
    Usage:
    python create_domain_vxrail.py <hostname> <username> <password>\n Refer to documentation for more detais\n'''
    print (help_description)


def action_performer():
    arguments = sys.argv
    if(len(arguments) < 3):
        get_help()
        return
    hostname = 'http://'+arguments[1]
    username = arguments[2]
    password = arguments[3]
    create_workload_domain(hostname,username,password)
    return

action_performer()

