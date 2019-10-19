#coding=utf-8
import sys
import re
import json
import time
import requests
import logging
logging.basicConfig(level=logging.INFO)  # 

from test_conf import Conf

username = Conf.username1
username2 = Conf.username2
password = Conf.password

def set_search_csrf(session):
    """Extract the required CSRF token.

    LinkedIn's search function requires a CSRF token equal to the JSESSIONID.
    """
    csrf_token = session.cookies['JSESSIONID'].replace('"', '')
    session.headers.update({'Csrf-Token': csrf_token})
    return session

def login(username, password):
    """Creates a new authenticated session.
    
    Note that a mobile user agent is used. Parsing using the desktop results
    proved extremely difficult, as shared connections would be returned in
    a manner that was indistinguishable from the desired targets.
    The other header matters as well, otherwise advanced search functions
    (region and keyword) will not work.
    
    The function will check for common failure scenarios - the most common is
    logging in from a new location. Accounts using multi-factor auth are not
    yet supported and will produce an error.
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
    # is required for our logon attempt.
    anon_response = session.get('https://www.linkedin.com/')
    login_csrf = re.findall(r'name="loginCsrfParam".*?value="(.*?)"',
                            anon_response.text)
    if login_csrf:
        login_csrf = login_csrf[0]
    else:
        logging.error("[!] Having trouble with loading the linkedin page... try again.")
        sys.exit()

    # Define the data we will POST for our login.
    auth_payload = {
        'session_key': username,
        'session_password': password,
        'isJsEnabled': 'false',
        'loginCsrfParam': login_csrf
        }

    # Perform the actual login. We disable redirects as we will use that 302
    # as an indicator of a successful logon.
    response = session.post('https://www.linkedin.com/uas/login-submit',
                            data=auth_payload, allow_redirects=False)

    # Define a successful login by the 302 redirect to the 'feed' page. Try
    # to detect some other common logon failures and alert the user.
    if response.status_code == 302:
        redirect = response.headers['Location']
        if 'feed' in redirect:
            logging.info("[+] Successfully logged in.\n")
            return session
        if 'consumer-email-challenge' in redirect:
            logging.error("[!] LinkedIn doesn't like something about this"
                  " login. Maybe you're being sneaky on a VPN or something."
                  " You may get an email with a verification token. You can"
                  " ignore the email. Log in from a web browser and try"
                  " again.\n")
            return False
        if 'captcha' in redirect:
            logging.error("[!] You've triggered a CAPTCHA. Oops. Try logging"
                  " in with your web browser first and come back later.")
            return False
        else:
            # The below will detect some 302 that I don't yet know about.
            logging.error("[!] Some unknown error logging in. If this"
                  " persists, please open an issue on gitlab.\n")
            return False

    # A failed logon doesn't generate a 302 at all, but simply reponds with
    # the logon page. We detect this here.
    if '<title>Sign In</title>' in response.text:
        logging.error("[!] You've been returned to a login page. Check your"
              " password and try again.\n")
        return False

    # If we make it past everything above, we have no idea what happened.
    # Oh well, we fail.
    logging.error("[!] Some unknown error logging in. If this persists,"
          "please open an issue on gitlab.\n")
    return False

def try_to_login(username, password, try_login_time=3):
    # Try to login
    while try_login_time > 0:
        session = login(username, password)
        session = set_search_csrf(session)
        if not session:
            try_login_time -= 1
            logging.error("[!] try fail")
        else:
            return session
    sys.exit()

def load_page(session, url):
    try:
        result = session.get(url)
        if result.status_code == 404:
            logging.error("[!] 404 Can not Get the {}".format(url))
            return None
        content = result.text #.encode('UTF-8')
        return json.loads(content)
    except Exception as e:
        logging.info('[-] Get the {} wrong'.format(url))
        logging.error(e)
        return None

def get_connections(session, friendCount=80):
    url = 'https://www.linkedin.com/voyager/api/relationships/connections?count={}&sortType=RECENTLY_ADDED'.format(friendCount)
    content = load_page(session, url)
    if content == None:
        return []
    friends = content['elements']
    #extract_miniProfile(friends)
    return friends

def get_2_degree(session, publicIdentifier, max_num=100):
    #Each user can get up to 0-99 second-degree users
    #There may be duplicates between users
    max_num = min(max_num, 100)
    url = 'https://www.linkedin.com/voyager/api/identity/profiles/{}/memberConnections?q=connections&count={}'.format(publicIdentifier, max_num)
    content = load_page(session, url)
    if content == None:
        return []
    else:
        two_degrees = content['elements']#[0]['miniProfile']
        #extract_miniProfile(two_degrees)
        return two_degrees

def extract_miniProfile(friends):
    for friend in friends:
        lastName = friend['miniProfile']['lastName']
        firstName = friend['miniProfile']['firstName']
        publicIdentifier= friend['miniProfile']['publicIdentifier']
        occupation = friend['miniProfile']['occupation']
        entityUrn = friend['miniProfile']['entityUrn']
        profileId = friend['miniProfile']['entityUrn'].split(':')[-1]
        #Can be stored directly friend['miniProfile'] 
        #print(lastName, firstName, publicIdentifier, occupation, entityUrn)

def get_profileContactInfo(session, publicIdentifier):
    url = 'https://www.linkedin.com/voyager/api/identity/profiles/{}/profileContactInfo'.format(publicIdentifier)
    #['phoneNumbers', 'address', 'weChatContactInfo', 'twitterHandles', 'connectedAt', 'emailAddress', 'entityUrn']
    content = load_page(session, url)

    if content == None:
        return ('', '', '')
    else:
        if 'phoneNumbers' in content.keys():
            phoneNumbers = content['phoneNumbers']
        else:
            phoneNumbers = ''
        if 'address' in content.keys():
            address = content['address']
        else:
            address = ''
        if 'emailAddress' in content.keys():
            # weChatContactInfo = content['weChatContactInfo']
            # twitterHandles = content['twitterHandles']
            emailAddress = content['emailAddress']
        else:
            emailAddress = ''
        return (phoneNumbers, address, emailAddress)

def get_networkinfo(session, publicIdentifier):
    url = 'https://www.linkedin.com/voyager/api/identity/profiles/{}/networkinfo'.format(publicIdentifier)
    content = load_page(session, url)
    if content == None:
        return []
    else:
        followersCount = content['followersCount'] # int
        distance = content['distance']['value']  #DISTANCE_1
        return content

def get_youmayknow(session, start_num=0):
    url = 'https://www.linkedin.com/voyager/api/relationships/peopleYouMayKnow?count=100&start={}&usageContext=p_flagship3_people_connections&includeInsights=false'.format(start_num) #When the count is 100, the maximum start_num is 1899 (up to 2000 user information can be obtained 0-1999)
    content = load_page(session, url)
    if content == None:
        return []
    else:
        friends = content['elements'] #friend=friends[0]
        for friend in friends:
            try:
                lastName = friend['entity']['com.linkedin.voyager.identity.shared.MiniProfile']['lastName']
                firstName = friend['entity']['com.linkedin.voyager.identity.shared.MiniProfile']['firstName']
                publicIdentifier= friend['entity']['com.linkedin.voyager.identity.shared.MiniProfile']['publicIdentifier']
                occupation = friend['entity']['com.linkedin.voyager.identity.shared.MiniProfile']['occupation']
                entityUrn = friend['entity']['com.linkedin.voyager.identity.shared.MiniProfile']['entityUrn']
                profileId = friend['entity']['com.linkedin.voyager.identity.shared.MiniProfile']['entityUrn'].split(':')[-1]
            except:
                lastName, firstName, publicIdentifier, occupation, profileId= '', '', '', '', ''

            phoneNumbers, address, emailAddress = get_profileContactInfo(session, publicIdentifier)
            get_shares(session, profileId)
            #print(lastName, firstName, publicIdentifier, occupation, profileId)
            try:
                sql = '''INSERT INTO users (publicIdentifier, lastName,  firstName, occupation, profileId, phoneNumbers, address, emailAddress) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")''' % (publicIdentifier, lastName,  firstName, occupation, profileId, phoneNumbers, address, emailAddress)
                Conf.db_cur.execute(sql) #Duplicate entry
            except:
                logging.error(sql)
        Conf.db_temp.commit()

def get_profileView(session, publicIdentifier):
    url = 'https://www.linkedin.com/voyager/api/identity/profiles/{}/profileView'.format(publicIdentifier)
    content = load_page(session, url)
    if content == None:
        return []
    else:
        educationView = content['educationView']['elements'] # list 'schoolName' 'fieldOfStudy' 'degreeName' 'activities' 'timePeriod' {'startDate': {'year': 2008}, 'endDate': {'year': 2010}}
        honorView = content['honorView']['elements']         # list
        certificationView = content['certificationView']['elements'] #list Each take['name']
        skillView = content['skillView']['elements']  #list Each take['name']
        positionView = content['positionView']['elements'] #list Each take 'description' 'company' 'title' (position)'locationName'  ['companyName']'timePeriod'
        testScoreView = content['testScoreView']['elements'] #list0

def get_shares(session, profileId):
    #Only include sharing parts
    url = 'https://www.linkedin.com/voyager/api/feed/updates?count=20&includeLongTermHistory=true&moduleKey=member-shares%3Aphone&numComments=0&numLikes=0&profileId={}&q=memberShareFeed'.format(profileId)
    content = load_page(session, url)
    try:
        shares = content['elements']
        #['isSponsored', 'socialDetail', 'value', 'tracking', 'urn', 'permalink', 'entityUrn', 'id']
    except:
        return None
    for share in shares:
        try:
            like_count = share['socialDetail']['totalSocialActivityCounts']['numLikes'] #int
            comment_count = share['socialDetail']['totalSocialActivityCounts']['numComments']
            miniProfile = share['value']['com.linkedin.voyager.feed.ShareUpdate']['actor']['com.linkedin.voyager.feed.MemberActor']['miniProfile']
            ctime = share['value']['com.linkedin.voyager.feed.ShareUpdate']['createdTime'] #If it is reprinted or commented, there will be originalUpdate
            tmp_content = share['value']['com.linkedin.voyager.feed.ShareUpdate']['content']
        except:
            like_count, comment_count = 0, 0
            tmp_content = {}
            ctime = ''
            miniProfile = {'publicIdentifier':''}

        if 'com.linkedin.voyager.feed.ShareImage' in tmp_content.keys():
            try:
                text = tmp_content['com.linkedin.voyager.feed.ShareImage']['text']['values'][0]['value']  #Picture or text
            except:
                text = ''
        elif 'com.linkedin.voyager.feed.ShareText' in tmp_content.keys():
            try:
                text = tmp_content['com.linkedin.voyager.feed.ShareText']['text']['values'][0]['value']  #text
            except:
                text = ''
        else:
            text = ''
        #print(like_count, comment_count, miniProfile['publicIdentifier'], ctime, text)
        try:
            sql = '''INSERT INTO feeds (publicIdentifier, content,  ctime, like_count, comment_count) VALUES ("%s", "%s", "%s", "%d", "%d")''' % (miniProfile['publicIdentifier'], text,  ctime, like_count, comment_count)
            Conf.db_cur.execute(sql) #Duplicate entry
        except:
            logging.error(sql)
    Conf.db_temp.commit()

def get_activity(session, profileId):
    #Including praise and comment
    #If it is praise or comment 'com.linkedin.voyager.feed.ViralUpdate'
    ##If it is reprinted or commented, there will be originalUpdate
    url = 'https://www.linkedin.com/voyager/api/feed/updates?count=20&includeLongTermHistory=true&moduleKey=member-activity%3Aphone&numComments=0&numLikes=0&profileId={}&q=memberFeed'.format(profileId)
    content = load_page(session, url)
    activitys = content['elements']
    for activity in activitys:
        like_count = activity['socialDetail']['totalSocialActivityCounts']['numLikes'] #int数字
        comment_count = activity['socialDetail']['totalSocialActivityCounts']['numComments']
        if 'com.linkedin.voyager.feed.ViralUpdate' in activity['value'].keys():
            miniProfile = activity['value']['com.linkedin.voyager.feed.ViralUpdate']['actor']['com.linkedin.voyager.feed.MemberActor']['miniProfile']
            ctime = activity['value']['com.linkedin.voyager.feed.ViralUpdate']['originalUpdate']['value']['com.linkedin.voyager.feed.ShareUpdate']['createdTime'] #If it is reprinted or commented, there will be originalUpdate
            text = activity['value']['com.linkedin.voyager.feed.ViralUpdate']['header']['text']
        elif 'com.linkedin.voyager.feed.ShareUpdate' in activity['value'].keys():
            miniProfile = activity['value']['com.linkedin.voyager.feed.ShareUpdate']['actor']['com.linkedin.voyager.feed.MemberActor']['miniProfile']
            ctime = activity['value']['com.linkedin.voyager.feed.ShareUpdate']['createdTime'] #If it is reprinted or commented, there will be originalUpdate
            tmp_content = activity['value']['com.linkedin.voyager.feed.ShareUpdate']['content']
            if 'com.linkedin.voyager.feed.ShareImage' in tmp_content.keys():
                try:
                    text = tmp_content['com.linkedin.voyager.feed.ShareImage']['text']['values'][0]['value']  #pic text
                except:
                    text = ''
            elif 'com.linkedin.voyager.feed.ShareText' in tmp_content.keys():
                try:
                    text = tmp_content['com.linkedin.voyager.feed.ShareText']['text']['values'][0]['value']  #text
                except:
                    text = ''
            else:
                text = ''
        print(like_count, comment_count, miniProfile['publicIdentifier'], ctime, text)

def insert_info(session, friends):
    for friend in friends:
        lastName = friend['miniProfile']['lastName']
        firstName = friend['miniProfile']['firstName']
        publicIdentifier = friend['miniProfile']['publicIdentifier']
        occupation = friend['miniProfile']['occupation']
        profileId = friend['miniProfile']['entityUrn'].split(':')[-1]
        phoneNumbers, address, emailAddress = get_profileContactInfo(session, publicIdentifier)
        get_shares(session, profileId)
        try:
            sql = '''INSERT INTO users (publicIdentifier, lastName,  firstName, occupation, profileId, phoneNumbers, address, emailAddress) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")''' % (publicIdentifier, lastName,  firstName, occupation, profileId, phoneNumbers, address, emailAddress)
            Conf.db_cur.execute(sql) #Duplicate entry
        except:
            logging.error(sql)

def test_diff(start_num=0):
    url = 'https://www.linkedin.com/voyager/api/relationships/peopleYouMayKnow?count=100&start={}&usageContext=p_flagship3_people_connections&includeInsights=false'.format(start_num) #When the count is 100, the maximum start_num is 1899 (up to 2000 user information can be obtained 0-1999)
    session = try_to_login(username, password)
    content = load_page(session, url)
    session2 = try_to_login(username2, password)
    content2 = load_page(session2, url)
    if content == content2:
        print("info not different")
    else:
        print("There are some differences in the information")
    # get_youmayknow(session, start_num=start_num)
    # get_youmayknow(session2, start_num=start_num)
    try:
        friends = content['elements']
        friends2 = content2['elements']
        print(friends[0])
        print(friends2[0])
    except:
        pass

# test_diff()

start_time = time.time()
session = try_to_login(username, password)

for i in range(20):
    logging.info('[*] Now get the {}'.format(i*100))
    start_num = min(i*100, 1899)
    get_youmayknow(session, start_num=start_num)

friends = get_connections(session)
insert_info(session, friends)
for friend in friends:
    try:
        publicIdentifier = friend['miniProfile']['publicIdentifier']
        two_degrees = get_2_degree(session, publicIdentifier)
        insert_info(session, two_degrees)
    except:
        logging.error('[-] Someting was wrong')

used_time = time.time() - start_time
logging.info('[*] The scrapy project used time: {}'.format(used_time))
