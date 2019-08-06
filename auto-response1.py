#!/usr/bin/env python3
#rnort003
import re
import glob
import os
import subprocess
import time
import smtplib, ssl
import configpy as cfg
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ITSEC_email = cfg.bones['ITSEC_email']
SC_email = cfg.bones['SC_email']
SS_email = cfg.bones['SS_email']
myaddr = cfg.bones['user']
pw = cfg.bones['passwd']
tmp = cfg.bones['tmp']

# email the support services to alert about action taken on all crm related emails
def email_ss(crm):
    message = MIMEMultipart("alternative")
    message['Subject'] = "Account(s) disabled by IT Sec"
    message['From'] = "ITSecurity@company.com"
    message['To'] = SS_email
    message['Cc'] = ITSEC_email

    text = (
    "Hi Support Services,\n"
    "We received notice {} have clicked on a malicious email attachment/ link. "
    "We have temporarily disabled the account(s) and terminated all active "
    "sessions."
    "\n\n"
    "Thanks,\n"
    "IT Sec".format(crm))

    p1 = MIMEText(text, "plain")
    message.attach(p1)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(myaddr, pw)
        server.sendmail(
             myaddr, [SS_email,ITSEC_email], message.as_string()
        )

# email the service center to alert about action taken on all non-crm emails
def email_SC(not_crm):
    message = MIMEMultipart("alternative")
    message['Subject'] = "Account(s) disabled by IT Sec"
    message['From'] = "ITSecurity@company.com"
    message['To'] = SC_email
    message['Cc'] = ITSEC_email

    text = (
    "Hi Service Center,\n"
    "We received notice {} have clicked on a malicious email attachment/ link. "
    "We have temporarily disabled the account(s) and terminated all active "
    "sessions."
    "\n\n"
    "Thanks,\n"
    "IT Sec".format(not_crm))

    p1 = MIMEText(text, "plain")
    message.attach(p1)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(myaddr, pw)
        server.sendmail(
            myaddr, [SC_email,ITSEC_email], message.as_string()
        )

#look for specific email address types to alert appropiate groups
def crm_check(recipients, crm, not_crm):
    for each in recipients:
        if "crm" in each:
            crm.append(each)
        else:
            not_crm.append(each)

#lock out the recipients active directory account
def lock(recipients):
    for recipient in recipients:
        acctLock = subprocess.Popen([r'c:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe',
                         '-ExecutionPolicy',
                         'Unrestricted',
                         './lockAcct.ps1',
                         recipient], cwd=os.getcwd())
        result = acctLock.wait()
        time.sleep(3)

# kill all active sessions in O365 by using Revoke-AzureADUserAllRefreshToken in AzureAD PS module
def kill_session(UPN_list):
     for upn in UPN_list:
         print(upn)
         azurecheck = subprocess.Popen([r'c:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe',
                              '-ExecutionPolicy',
                              'Unrestricted',
                              './killSessions.ps1',
                              upn], cwd=os.getcwd())
         result = azurecheck.wait()

#get UPN value of all recipients to find the user in AzureAD
def getUPN(recipients,UPN_list):
    for recipient in recipients:
        print("checking recipient", recipient)
        getUPNval = subprocess.run([r'c:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe',
                         '-ExecutionPolicy',
                         'Unrestricted',
                         './getUPN.ps1',
                         recipient], stdout=subprocess.PIPE)
        upn = getUPNval.args[4]
        UPN_list.append(upn)

# Get the recipients from your domain from the email list
def get_recipients(recipients, emails):
    for addr in emails:
        if "@company.com" in addr:
            recipients.append(addr)
    return recipients

#remove all duplicate email addresses so you are not looking at the same account twice
def remove_duplicates(all_emails,emails):
    for addr in all_emails:
        if addr not in emails:
            emails.append(addr)
    return emails

# use a regex statement to parse all email addresses out of log file
def get_data(data):
    regex = r'\b[\w.-]+?@\w+?\.\w+?\b'
    reg_data = re.findall(regex,data)
    return reg_data

#find most recent log file from directory
def get_latest_file():
    list_of_files = glob.glob('path/to/alerts/*')
    if not list_of_files:
        exit()
    latest_file = max(list_of_files, key=os.path.getctime)
    file_name = os.path.basename(latest_file)
    read = open('./recentlog.txt', 'r+')
    text = read.readline()
    text=text.strip()
    if text == file_name:
        print('no new logs')
        exit()
    else:
        read.seek(0)
        read.write(file_name)
    ofile = open(latest_file, "r")
    recent_data = ofile.read()
    ofile.close()
    print('read latest log')
    return(recent_data)

def main():
    emails = []
    recipients = []
    UPN_list = []
    crm = []
    not_crm = []
    data = get_latest_file()
    all_emails = get_data(data)
    remove_duplicates(all_emails,emails)
    get_recipients(recipients, emails)
    lock(recipients)
    getUPN(recipients, UPN_list)
    kill_session(UPN_list)
    crm_check(recipients, crm, not_crm)
    print(crm)
    print(not_crm)
    # send alert to appropiate group based on email criteria
    if crm:
        email_ss(crm)
    elif not_crm:
        email_SC(not_crm)



if __name__ == '__main__':
    main()
