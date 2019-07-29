#!/usr/bin/env python3
#rnort003
import re
import glob
import os
import subprocess
import time


def lock(recipients):
    for recipient in recipients:
        acctLock = subprocess.Popen([r'/cygdrive/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe',
                         '-ExecutionPolicy',
                         'Unrestricted',
                         './elevate.ps1',
                         recipient], cwd=os.getcwd())
        time.sleep(3)


def kill_session(UPN_list):
     for upn in UPN_list:
         print(upn)
         azurecheck = subprocess.Popen([r'/cygdrive/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe',
                              '-ExecutionPolicy',
                              'Unrestricted',
                              './addrCheck.ps1',
                              upn], cwd=os.getcwd())
         result = azurecheck.wait()

def getUPN(recipients,UPN_list):
    for recipient in recipients:
        #print("checking recipient", recipient)
        getUPNval = subprocess.run([r'/cygdrive/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe',
                         '-ExecutionPolicy',
                         'Unrestricted',
                         './getUPN.ps1',
                         recipient], stdout=subprocess.PIPE)
        upn = getUPNval.args[4]
        UPN_list.append(upn)

def get_recipients(recipients, emails):
    for addr in emails:
        if "@test.com" in addr:
            recipients.append(addr)
    return recipients

def remove_duplicates(all_emails,emails):
    for addr in all_emails:
        if addr not in emails:
            emails.append(addr)
    return emails


def get_data(data):
    regex = r'\b[\w.-]+?@\w+?\.\w+?\b'
    reg_data = re.findall(regex,data)
    return reg_data

def get_latest_file():
    list_of_files = glob.glob('Path/to/files/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    file_name = os.path.basename(latest_file)
    ofile = open(latest_file, "r")
    recent_data = ofile.read()
    ofile.close()
    return(recent_data)

def main():
    emails = []
    recipients = []
    UPN_list = []
    data = get_latest_file()
    all_emails = get_data(data)
    remove_duplicates(all_emails,emails)
    get_recipients(recipients, emails)
    lock(recipients)
    getUPN(recipients, UPN_list)
    kill_session(UPN_list)


if __name__ == '__main__':
    main()
