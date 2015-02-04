#!/usr/bin/python
import ceilometerclient.client
import os

VERSION = 2
USERNAME = os.environ.get('OS_USERNAME', None) 
PASSWORD = os.environ.get('OS_PASSWORD', None)
PROJECT_NAME = os.environ.get('OS_TENANT_NAME', None) 
AUTH_URL = os.environ.get('OS_AUTH_URL', None)

auth_vars = (VERSION, USERNAME, PASSWORD, PROJECT_NAME, AUTH_URL)

for var in auth_vars:
    if not var:
        print "Missing nova environment variables, exiting."
        sys.exit(1)



cclient = ceilometerclient.client.get_client(VERSION, username=USERNAME, password=PASSWORD, tenant_name=PROJECT_NAME, auth_url=AUTH_URL)
