#coding=utf-8
import sys
import re
import json
import time
import requests

import logging
logging.basicConfig(level=logging.INFO)  # 


def register(phoneNumber, firstName="li", lastName="li", password="li"):
    """Creates a new authenticated session.
    
    Note that a mobile user agent is used. Parsing using the desktop results
    proved extremely difficult, as shared connections would be returned in
    a manner that was indistinguishable from the desired targets.
    The other header matters as well, otherwise advanced search functions
    (region and keyword) will not work.
    """
    session = requests.session()

    # Our search and regex will work only with a mobile user agent and
    # the correct REST protocol specified below.
    mobile_agent = ('Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid '
                    'Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) '
                    'Version/4.0 Mobile Safari/533.1')
    session.headers.update({'User-Agent': mobile_agent,
                            'X-RestLi-Protocol-Version': '2.0.0'})

    # We wll grab an anonymous response to look for the CSRF token, which
    # is required for our register attempt.
    anon_response = session.get('https://www.linkedin.com/')
    login_csrf = re.findall(r'name="loginCsrfParam".*?value="(.*?)"',
                            anon_response.text)
    if login_csrf:
        login_csrf = login_csrf[0]
    else:
        logging.error("[!] Having trouble with loading the linkedin page... try again.")
        sys.exit()

    # Define the data we will POST for our register.
    info_payload = {
    	"firstName":firstName,
    	"lastName":lastName,
    	"password":password,
    	"phoneNumber":phoneNumber}

    # 
    response = session.post('https://www.linkedin.com/start/reg/api/cors/createAccount?trk=public_guest-home_default&csrfToken='+csrfToken,
                            data=info_payload, allow_redirects=False)

    if response.status_code == 200:
    	try:
    		reply = json.loads(response.text)
    		challengeId = reply['challengeId']
    		phoneNumberInNationalFormat = reply['phoneNumberInNationalFormat']
    		submissionId = reply['submissionId']
    	except:
    		return False
    	Sms_payload = {"phoneNumber":{"number":phoneNumberInNationalFormat},"pinDeliveryChannel":"SMS"}
        Sms_response = session.post('https://www.linkedin.com/checkpoint/challenges/sendPinViaSms/'+challengeId+'?displayTime=' + str(int(time.time() *1000)), data=Sms_payload, allow_redirects=False)
        if "SUCCESS" in Sms_response.text:
        	code = get_sms_online(phoneNumber)
        	check_payload = {"pin":code}
        	check_response = session.post('https://www.linkedin.com/checkpoint/challenges/phoneVerificationChallenge/'+challengeId+'?displayTime=' + str(int(time.time() *1000)), data=check_payload)
        	if "INTERNAL_ERROR" in check_response.text:
        		logging.info("[+] check_response : " + check_response.text)
        		return False
        	moreinfo_payload = {"firstName":firstName,
        		"lastName":lastName,
        		"password":password,
    			"phoneNumber":phoneNumber,
    			"submissionId":submissionId,
    			"challengeId":challengeId}
        	more_response = session.post('https://www.linkedin.com/start/reg/api/cors/createAccount?trk=public_guest-home_default&csrfToken='+csrfToken,
                            data=moreinfo_payload, allow_redirects=False)
        	if (more_response.status_code == 400) or ("Duplicate phone number" in more_response.text):
        		#
        		logging.info("[+] more_response : " + more_response.text)
        		return False
        	# 
    return False
