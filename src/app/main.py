#!/usr/bin/env python3

import os
import subprocess
import threading
import concurrent.futures

import helpers

# # Pycharm pydevd
# PYCHARM_PYDEVD_ENABLED = int(os.getenv('PYCHARM_PYDEVD_ENABLED'))
# PYCHARM_PYDEVD_HOST = str(os.getenv('PYCHARM_PYDEVD_HOST'))
# PYCHARM_PYDEVD_PORT = int(os.getenv('PYCHARM_PYDEVD_PORT'))
#
# # Enable pydevd debugger
# if (PYCHARM_PYDEVD_ENABLED):
#     import pydevd_pycharm
#     pydevd_pycharm.settrace(PYCHARM_PYDEVD_HOST, port=PYCHARM_PYDEVD_PORT, stdoutToServer=True, stderrToServer=True)


# # Create lightsail immutable
# def create_lightsail(immutable):
#     subprocess.call(['aws', 'lightsail','create-instances-from-snapshot', '--instance-snapshot-name', immutable['refer'], '--instance-names', immutable['name'], '--availability-zone', immutable['zone'], '--bundle-id', immutable['bundle']])

# Create azure immutable
def create_azure(immutable):
    pass


# Multi process azure immutable
def process_lightsail(azure_immutables):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(create_azure, immutable) for immutable in azure_immutables]

        for f in concurrent.futures.as_completed(results):
            f.result()


# Main
def main():
    data = helpers.app()

    azure_immutables = []

    for k,immutable in data['immutables'].items():

        # Filter lightsail deployments
        if (immutable['type'] == "azure"):
            azure_immutables.append(immutable)


    t1 = threading.Thread(target=process_lightsail, args=[azure_immutables])

    t1.start()

    t1.join()



# Execute
if __name__ == '__main__':
    main()