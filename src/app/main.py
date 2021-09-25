#!/usr/bin/env python3

import os
import subprocess
import threading
import concurrent.futures
import uuid
from hashlib import sha256

import helpers

DEPLOY_TEMPLATE = '/var/www/app/templates/deploy.template.ps1'
BUILD_DIRECTORY = '/var/www/app/.build'

# # Pycharm pydevd
# PYCHARM_PYDEVD_ENABLED = int(os.getenv('PYCHARM_PYDEVD_ENABLED'))
# PYCHARM_PYDEVD_HOST = str(os.getenv('PYCHARM_PYDEVD_HOST'))
# PYCHARM_PYDEVD_PORT = int(os.getenv('PYCHARM_PYDEVD_PORT'))
#
# # Enable pydevd debugger
# if (PYCHARM_PYDEVD_ENABLED):
#     import pydevd_pycharm
#     pydevd_pycharm.settrace(PYCHARM_PYDEVD_HOST, port=PYCHARM_PYDEVD_PORT, stdoutToServer=True, stderrToServer=True)


# Build unique workspace - return string
def build_workspace(name):
    stringId = uuid.uuid4()
    salted_string = str(stringId) + str(name)
    hash_result = sha256(str(salted_string).encode())
    return hash_result.hexdigest()

# Create azure immutable
def create_azure(immutable):

    if not os.path.exists(BUILD_DIRECTORY):
        os.makedirs(BUILD_DIRECTORY)

    workspace = build_workspace(immutable['name'])

    if not os.path.exists(BUILD_DIRECTORY + '/' + workspace):
        os.makedirs(BUILD_DIRECTORY + '/' + workspace)

    subprocess.call('cp '+DEPLOY_TEMPLATE+' '+BUILD_DIRECTORY + '/' + workspace+'/deploy.template.ps1', shell=True)

    common = helpers.common()
    current_template = BUILD_DIRECTORY + '/' + workspace + '/deploy.template.ps1'
    current_script = BUILD_DIRECTORY + '/' + workspace + '/deploy.ps1'

    # TODO: filter common values

    with open(current_template, 'r') as template:
        with open(current_script, 'w+') as output:
            for line in template.readlines():
                line = line.replace("@@IMMUTABLE_RESOURCE_GROUP@@", immutable["rg"])
                line = line.replace("@@IMMUTABLE_REGION@@", immutable["region"])
                line = line.replace("@@IMMUTABLE_VPC@@", immutable["vpc"])
                line = line.replace("@@IMMUTABLE_SUBNET@@", immutable["subnet"])
                line = line.replace("@@IMMUTABLE_NAME@@", immutable["name"])
                line = line.replace("@@IMMUTABLE_BLUEPRINT@@", immutable["blueprint"])
                line = line.replace("@@IMMUTABLE_BUNDLE@@", immutable["bundle"])
                line = line.replace("@@IMMUTABLE_STORAGE_ACCOUNT_TYPE@@", immutable["storage"])
                line = line.replace("@@IMMUTABLE_PRIVATE_IP_ADDRESS@@", immutable["private_ip_address"])

                output.write(line)

    # Execute powershell script
    stdout = subprocess.check_output(['pwsh', BUILD_DIRECTORY + '/' + workspace + '/deploy.ps1'], universal_newlines=True)
    print(stdout)

# Multi process azure immutables
def process_azure(azure_immutables):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(create_azure, immutable) for immutable in azure_immutables]

        for f in concurrent.futures.as_completed(results):
            f.result()


# Main
def main():
    data = helpers.app()

    azure_immutables = []

    for k,immutable in data['immutables'].items():

        # Filter azure deployments
        if (immutable['type'] == "azure"):
            azure_immutables.append(immutable)


    t1 = threading.Thread(target=process_azure, args=[azure_immutables])

    t1.start()

    t1.join()



# Execute
if __name__ == '__main__':
    main()