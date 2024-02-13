from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from django.shortcuts import render
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from dotenv import load_dotenv
import os
load_dotenv()  

import firebase_admin
from firebase_admin import credentials, initialize_app, db

# Initialize Firebase with your credentials
# (Please handle credentials securely, don't share them here)
# cred = credentials.Certificate('/workspace/EmailApi/serviceAccountKey.json')
# initialize_app(cred)
if not firebase_admin._apps:
    cred = credentials.Certificate('/workspace/EmailApi/serviceAccountKey.json') 
    default_app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://internship-demo-7d427-default-rtdb.firebaseio.com'})


# Get a reference to your database (use the appropriate service here)
db_ref = db.reference()


def sendemail(request):
    if request.method == "POST":
        sender = 'Chirag Biradar'
        toemail = request.POST.get('to')
        toname = request.POST.get('toname')
        data = {'toname': toname, 'toemail': toemail}
        db_ref.push(data)
        fromemail = 'chiragsb16@gmail.com'
        subject = 'Test email for assignment'
        message = 'Thanks for Subscribing!!'
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = str(os.getenv('BrevoApi'))
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        subject = subject
        html_content = message
        sender = {"name": sender, "email": fromemail}
        to = [{"email": toemail, "name": toname}]
        headers = {"Some-Custom-Name": "unique-id-1234"}
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers,html_content=html_content, sender=sender, subject=subject)
        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            pprint(api_response)
            messages.success(request, "Email send successfully")
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
    return render(request, 'email.html', locals())
