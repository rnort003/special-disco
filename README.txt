                                         /$$           /$$                    
                                        |__/          | $$                    
  /$$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$$ /$$  /$$$$$$ | $$                    
 /$$_____/ /$$__  $$ /$$__  $$ /$$_____/| $$ |____  $$| $$       /$$$$$$      
|  $$$$$$ | $$  \ $$| $$$$$$$$| $$      | $$  /$$$$$$$| $$      |______/      
 \____  $$| $$  | $$| $$_____/| $$      | $$ /$$__  $$| $$                    
 /$$$$$$$/| $$$$$$$/|  $$$$$$$|  $$$$$$$| $$|  $$$$$$$| $$                    
|_______/ | $$____/  \_______/ \_______/|__/ \_______/|__/                    
          | $$                                                                
          | $$                                                                
          |__/                                                                                                                                 
                                                                              
       /$$ /$$                                                                
      | $$|__/                                                                
  /$$$$$$$ /$$  /$$$$$$$  /$$$$$$$  /$$$$$$                                   
 /$$__  $$| $$ /$$_____/ /$$_____/ /$$__  $$                                  
| $$  | $$| $$|  $$$$$$ | $$      | $$  \ $$                                  
| $$  | $$| $$ \____  $$| $$      | $$  | $$                                  
|  $$$$$$$| $$ /$$$$$$$/|  $$$$$$$|  $$$$$$/                                  
 \_______/|__/|_______/  \_______/ \______/                                   
                                                                                                 
This is a tool to lock out accounts in active directory and kill sessions in Azure. 

This tool works in conjuction with a SumoLogic script action and the Proofpoint TAP tool. Every 15 minutes a bash script is run to pull the logs from TAP console. In SumoLogic, the logs are parsed through to filter out the events that had a click permitted on a malicious or phishing link. SumoLogic will search for these events every 15 minutes. If a permitted click is found, it invokes the auto-response.py script to run. The first thing it will do is parse out the email addresses from the alert. After that, it seperates threat from victim email by finding which email contains your domain. The program will lock out the account in Active Directory by opening an powershell script to elevate permissions and lockout the victims account. Once this is completed, the program opens an Azure session through a powershell script and kills all sessions. The script will then send an email to an appropiate group to communicate the preventative action has been taken.
