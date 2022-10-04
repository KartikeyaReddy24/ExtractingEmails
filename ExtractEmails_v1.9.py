from tld import get_tld
from openpyxl import load_workbook
from googlesearch import search
from tld import get_tld
import re
import requests
import pandas as pd
import time
import random
import os
import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'AKIAXFEZEMGXMQUCUXIC'
SECRET_KEY = '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'

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                    aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

# Get environment variables
MINIMUM =  1 #os.getenv('min_val')
MAXIMUM = 8 #os.environ.get('max_val')

print("The Minimum row: ",MINIMUM)
print("The Maximum row: ",MAXIMUM)

start_time = time.time()

LinksCount=0
count = 0

#PhoneNumber=set()
SearchingFor=[]
LinksSearched=[]
l=set()
NotFoundLink=set()
links=set()
Nooflinkssearched=[]

############################################ SQS CODE HERE

########################################INITIALIZE CONNECTION TO AWS VIA BOTO3 'CLIENT'#############################################
client = boto3.resource('sqs',aws_access_key_id='AKIAXFEZEMGXLZLDHQEX',
    aws_secret_access_key='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',region_name='us-east-1')

accthttp='https://sqs.us-east-1.amazonaws.com/492094906798/'

###INPUT THE IAM CREDENTIALS WITH PERMISSIONS TO THE AWS ACCOUNT AND RESOURCE YOU'RE TRYING TO ACCESS.



################################################CREATE SQS-QUEUES IN THE CLIENT-CONNECTED ACCOUNT##########################################
# response = client.create_queue(
#      QueueName='TrialQueue'
# )
# print(response)

print("##########################################")
print("AVAILABLE QUEUES : URLS")

#The response is NOT a resource, but gives you a message ID and MD5
for queue in client.queues.all():
    print(queue.url)
#
print("##########################################")
########################################################SQS SEND OR RECEIVE###############################################

url = accthttp + str('TrialQueue')
# print(receipt)

while True:

    receipt = client.Queue(url=url).receive_messages(MaxNumberOfMessages=2)


 
    for cell in receipt:
        print("\nSearching for: ",cell.body)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        search_value=''
        for val in cell.body.split():
            search_value+=val+'+'

        # url = 'https://www.google.com?q=' + search_value

        for i in search(search_value, num_results=1):
            #print("count ",count)
            if count>0 and count % 18 == 0:
                print(f'\n\n\t\t::::::::::: You have now reached maximun Websearches. Please wait :::::::::::\n\n')
                time.sleep(300)
            count+=1
            #print("\nFor loop started. Wait 30 seconds\n")
            random.uniform(30,60)
            time.sleep(3)
            LinksCount +=1
            print(f'\n\n\tNo. of Web Searches: {LinksCount}\n\tExtracting Emails in: {i}')
            #print(i)
            SearchingFor.append(cell.body)
            LinksSearched.append(i)
            try:
                #print("\nYou are at Extracting Emails. Wait for 18 seconds\n")
                # random.uniform(30,60)
                time.sleep(5)
                EMAIL_REGEX= r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"      #r'[\w.+-]+@[\w-]+\.[\w.-]+'        #r'(?:\.?)([\w\-_+#~!$&\'\.]+(?<!\.)(@|[ ]?\(?[ ]?(at|AT)[ ]?\)?[ ]?)(?<!\.)[\w]+[\w\-\.]*\.[a-zA-Z-]{2,3})(?:[^\w])'  #re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+')            # r"[\w\.-]+@[\w\.-]+"
                #phone = r'\(?\b[2-9][0-9]{2}\)?[-][2-9][0-9]{2}[-][0-9]{4}\b'
                r=requests.get(i, headers=headers)
                for re_match in re.findall(EMAIL_REGEX, r.text):
                    l.add(re_match)
                    links.add(i)
                    #PhoneNumber.add(re_match)
                    print(f'\n\t',re_match)
            except:
                print("\n\tNot Found: ",i)
                NotFoundLink.add(i)
        cell.delete(QueueUrl=url, ReceiptHandle=cell.receipt_handle)
        print("\n\t\t\tThis message has been deleted.")
        time.sleep(15)


    websearch=pd.DataFrame(SearchingFor)
    searchlinks=pd.DataFrame(LinksSearched)
    copying_links=pd.DataFrame(links)
    data = pd.DataFrame(l)
    NotFounddata = pd.DataFrame(NotFoundLink)
    #PhNos=pd.DataFrame(PhoneNumber)
    LinksEmails=pd.concat((copying_links, data), ignore_index=True, axis=1)
    searchData=pd.concat((websearch, data), ignore_index=True, axis=1)


    print("\nLinks Searched\n",copying_links)
    print("\nEmail-ID's Collected:\n",data)
    print("\nNot Found Links:\n",NotFounddata)
    print("\nLinks Searched and Emails Collected:\n",LinksEmails)
    #print("\nPhone Number Collected:\n",PhNos)

    with pd.ExcelWriter("Industries_"+str(MINIMUM)+"_"+str(MAXIMUM)+".xlsx", engine='xlsxwriter') as writer:    
        # Write each dataframe to a different worksheet.
        searchData.to_excel(writer, sheet_name='Websearch Cell & Emails')
        searchlinks.to_excel(writer, sheet_name='LinksSearched')
        copying_links.to_excel(writer, sheet_name='UniqueLinksSearched')
        data.to_excel(writer, sheet_name='Emails')
        LinksEmails.to_excel(writer, sheet_name='Links & Emails')
        NotFounddata.to_excel(writer, sheet_name='NotFoundList')
        writer.save()
        print("\n\t\tFile saved")

    def convert(seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        
        return "%d:%02d:%02d" % (hour, minutes, seconds)

    print("\n------------------------------- DATA SAVED -------------------------------\n")

    print("\n\t----------- Time Taken For Execution: %s  -----------\n\n" % (convert(time.time() - start_time)))

    for file in os.listdir():
        if file.endswith(".xlsx"):
            print("\n\n\t\tThis is the file:::::::::::::::",file)
            print("\n\n\t\t",os.path.dirname(os.path.realpath(__file__)))
            # upload_file_bucket= 'extract.emails.storage'
            # upload_file_key= 'Container_Output/'+ str(file)
            # uploaded = upload_to_aws('extract.emails.storage', 'Industries_"+str(MINIMUM)+"_"+str(MAXIMUM)+".xlsx')
            uploaded = upload_to_aws(os.path.dirname(os.path.realpath(__file__))+"/"+file,'extract.emails.storage', file)
