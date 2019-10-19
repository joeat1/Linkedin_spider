#coding=utf-8
import sys
import re
import time
import string
import random

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import logging
logging.basicConfig(level=logging.INFO)

from test_conf import Conf1

WAIT_TIMEOUT = 10

def set_proxy():
    proxy = webdriver.Proxy()
    proxy.http_proxy = '127.0.0.1:1080'
    proxy.add_to_capabilities(webdriver.DesiredCapabilities.CHROME)
    browser.start_session(webdriver.DesiredCapabilities.CHROME)

def init_chromium():
    options = webdriver.ChromeOptions()
    if Conf1.Chromeheadless == True:
        options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)
    return driver

def get_by_xpath_or_none(driver, xpath, wait_timeout=None, logs=True):
    """
    Get a web element through the xpath string passed.
    If a TimeoutException is raised the else_case is called and None is returned.
    :param driver: Selenium Webdriver to use.
    :param xpath: String containing the xpath.
    :param wait_timeout: optional amounts of seconds before TimeoutException is raised, default WAIT_TIMEOUT is used otherwise.
    :param logs: optional, prints a status message to stdout if an exception occures.
    :return: The web element or None if nothing found.
    """
    try:
        return get_by_xpath(driver, xpath, wait_timeout=wait_timeout)
    except (TimeoutException, StaleElementReferenceException, WebDriverException) as e:
        if logs:
            logging.info("Exception Occurred:")
            logging.info("XPATH:{}".format(xpath))
            logging.info("Error:{}".format(e))
        return None

def get_by_xpath(driver, xpath, wait_timeout=None):
    """
    Get a web element through the xpath passed by performing a Wait on it.
    :param driver: Selenium web driver to use.
    :param xpath: xpath to use.
    :param wait_timeout: optional amounts of seconds before TimeoutException is raised, default WAIT_TIMEOUT is used otherwise.
    :return: The web element.
    """
    if wait_timeout is None:
        wait_timeout = WAIT_TIMEOUT
    return WebDriverWait(driver, wait_timeout).until(
        ec.presence_of_element_located(
            (By.XPATH, xpath)
        ))

def get_by_css_selector_or_none(driver, css_selector, wait_timeout=None, logs=True):
    """
    Get a web element through the css_selector string passed.
    If a TimeoutException is raised the else_case is called and None is returned.
    :param driver: Selenium Webdriver to use.
    :param css_selector: String containing the css_selector.
    :param wait_timeout: optional amounts of seconds before TimeoutException is raised, default WAIT_TIMEOUT is used otherwise.
    :param logs: optional, prints a status message to stdout if an exception occures.
    :return: The web element or None if nothing found.
    """
    try:
        return get_by_css_selector(driver, css_selector, wait_timeout=wait_timeout)
    except (TimeoutException, StaleElementReferenceException, WebDriverException) as e:
        if logs:
            logging.info("Exception Occurred:")
            logging.info("XPATH:{}".format(css_selector))
            logging.info("Error:{}".format(e))
        return None

def get_by_css_selector(driver, css_selector, wait_timeout=None):
    """
    Get a web element through the css_selector passed by performing a Wait on it.
    :param driver: Selenium web driver to use.
    :param css_selector: css_selector to use.
    :param wait_timeout: optional amounts of seconds before TimeoutException is raised, default WAIT_TIMEOUT is used otherwise.
    :return: The web element.
    """
    if wait_timeout is None:
        wait_timeout = WAIT_TIMEOUT
    return WebDriverWait(driver, wait_timeout).until(
        ec.presence_of_element_located(
            (By.CSS_SELECTOR, css_selector)
        ))

def get_css_selector_text(driver, css_selector, wait_timeout=None):
    """
    Get a web element content through the css_selector passed by performing a Wait on it.
    :param driver: Selenium web driver to use.
    :param css_selector: css_selector to use.
    :param wait_timeout: optional amounts of seconds before TimeoutException is raised, default WAIT_TIMEOUT is used otherwise.
    :return: The element content.
    """
    item = get_by_css_selector_or_none(driver, css_selector, logs=False)
    if item is not None:
        return item.text
    return 'Unknown'

def get_css_selector_href(driver, css_selector, wait_timeout=None):
    """
    Get a web element href through the css_selector passed by performing a Wait on it.
    :param driver: Selenium web driver to use.
    :param css_selector: css_selector to use.
    :param wait_timeout: optional amounts of seconds before TimeoutException is raised, default WAIT_TIMEOUT is used otherwise.
    :return: The element href.
    """
    item = get_by_css_selector_or_none(driver, css_selector, logs=False)
    if item is not None:
        return item.get_attribute('href')
    return 'Unknown'

def login(driver, username, password):
    """
    Logs in in Linkedin.
    :param driver: The yet open selenium webdriver.
    :return: Nothing
    """
    LINKEDIN_LOGIN_URL = 'https://www.linkedin.com/'
    driver.get(LINKEDIN_LOGIN_URL)
    driver.implicitly_wait(2)
    #driver.find_element_by_css_selector('.link-login.form-toggle').click()
    logging.info('[*] Searching for the Login btn')
    get_by_xpath(driver, '//*[@id="login-email"]').send_keys(username)

    logging.info('[*] Searching for the password btn')
    get_by_xpath(driver, '//*[@id="login-password"]').send_keys(password)

    logging.info('[*] Searching for the submit')
    get_by_xpath(driver, '//*[@id="login-submit"]').click()
    driver.implicitly_wait(1)
    if 'challenge' in driver.current_url or 'login-submit' in driver.current_url:
        logging.info('[-] Login function works wrong!')
        #valideEmail(driver)
    else:
        logging.info('[+] Login function perform well!')

def extracts_user_simple_info(driver):
    """
    Get a user info through the css_selector passed by performing a Wait on it.
    :param driver: Selenium web driver to use.
    :return: The info content.
    """
    name = get_css_selector_text(driver, '.pv-top-card-section__name', 2)                    
    entity_name = get_css_selector_text(driver, '.pv-top-card-v2-section__entity-name', 2)   
    headline = get_css_selector_text(driver, '.pv-top-card-section__headline', 2)            
    location = get_css_selector_text(driver, '.pv-top-card-section__location', 2)          
    profile_txt = ' '.join(re.findall('profile\.Profile(.*)', driver.page_source))
    try:
        profileId = re.findall('"profileId":"(.*?)"', profile_txt)[0]           
    except:
        profileId = ''.join(random.sample(string.ascii_letters + string.digits, 25))
    try:
        publicIdentifier = re.findall('"publicIdentifier":"(.*?)"', profile_txt)[0]
    except:     
        publicIdentifier = ''.join(random.sample(string.ascii_letters + string.digits, 25))
    logging.info('{} {} {} {} {} {}'.format(name, entity_name, headline, location, profileId, publicIdentifier) )
    return {'name':name, 'entity_name':entity_name, 'headline':headline, 'location':location, 'profileId':profileId, 'publicIdentifier':publicIdentifier}

def extracts_linkedin_users(driver):
    """
    Gets from a page containing a list of users, all the users.
    For instance: `https://www.linkedin.com/search/results/people/?facetConnectionOf=["ACoAABy7MPoBjLU7GxNfHQz2TKCgVEbdt8kQAGY"]&facetNetwork=["F","S"]&origin=MEMBER_PROFILE_CANNED_SEARCH`
    :param driver: The webdriver, logged in, and located in the page which lists users.
    :return: user url on LinkedinUser.
    """
    errors = 0
    for i in range(1, 11):
        logging.info('loading {}th user'.format(i))
        last_result_xpath = '//li[{}]/div/div[@class="search-result__wrapper"]'.format(i)
        result = get_by_xpath_or_none(driver, last_result_xpath, 3)
        if result is not None:
            # logging.info(result.text) 
            # name_elem = get_by_xpath_or_none(result, './/*[@class="name actor-name"]')
            # name = name_elem.text if name_elem is not None else None
            # title_elem = get_by_xpath_or_none(result, './/p')
            # title = title_elem.text if name_elem is not None else None
            link_elem = get_by_xpath_or_none(result, './/a', wait_timeout=1)
            if link_elem is not None:
                user_url = link_elem.get_attribute('href')
                insert_url(user_url)
            focus_elem_xpath = './/figure[@class="search-result__image"]'
            focus_elem = get_by_xpath_or_none(result, focus_elem_xpath, wait_timeout=1)
            if focus_elem is not None:
                driver.execute_script("arguments[0].scrollIntoView();", focus_elem)
            time.sleep(0.2)
        else:
            errors += 1
            if errors > 2:
                break
    try:
        Conf1.db_temp.commit()
    except:
        return

def extracts_linkedin_usersurl_simple(driver):
    '''
    '''
    js="var q=document.documentElement.scrollTop=600"
    driver.execute_script(js)
    time.sleep(1)
    results = driver.find_elements_by_css_selector('.search-result__wrapper')
    user_url = []
    for result in results:
        link_elem = get_by_xpath_or_none(result, './/a', wait_timeout=1)
        if link_elem is not None:
            user_url.append(link_elem.get_attribute('href'))
    return user_url

def search_more_user(driver, profileId, max_page=20, start_page=1):
    """
    Get more users URL through the button `more` in the page.
    :param driver: Selenium web driver to use.
    :param profileId:  profileId
    :param start_page: 
    :return: The users URL list.
    """
    driver.get('https://www.linkedin.com/search/results/people/?facetConnectionOf=["{}"]&facetNetwork=["S"]&origin=MEMBER_PROFILE_CANNED_SEARCH&page={}'.format(profileId, start_page))
    result = get_by_css_selector_or_none(driver, ".search-result__wrapper", 2)
    if result is None:
        logging.info('[*] 2-degree friends are None')
        return []
    extracts_linkedin_users(driver)
    next_button = get_by_css_selector_or_none(driver, '.artdeco-pagination__button--next', 2)
    page_num = 1
    while(next_button is not None and next_button.is_enabled()):
        try:
            next_button.click()
            time.sleep(2)
            extracts_linkedin_users(driver)
            #user_urllist += tmp
            page_num += 1
            if page_num >= max_page:
                break
        except:
            return None

def extracts_comment_simple(feed_shared):
    comment_button = get_by_css_selector_or_none(feed_shared, '.feed-shared-social-counts__num-comments', 1)
    if comment_button is not None:
        comment_count = comment_button.text
        comment_button.click() #
        comments = get_css_selector_text(feed_shared, '.comments-comments-list.ember-view', 1)
        return (comment_count, comments)
    return ('0', '')

def extracts_user_feed_simple(driver, user_url):
    """
    Get more users feed content through the recent-activity page.
    :param driver: Selenium web driver to use.
    :param user_url: The user's URL like  https://www.linkedin.com/in/dd08/
    :return: The user's feed content.
    """
    results = []
    driver.get(user_url +'detail/recent-activity/') #
    feed_shareds = driver.find_elements_by_css_selector('.feed-shared-update-v2.mh0.Elevation-2dp.ember-view')
    for feed_shared in feed_shareds:
        #logging.info(feed_shared.text.encode('gbk', errors='replace').decode('gbk'))   #
        # feed_shared.text
        result = {}
        feed_shared_actor_url = get_css_selector_href(feed_shared, '.feed-shared-actor__meta-link', 1) #feed-shared-actor__meta-link
        if feed_shared_actor_url is not None:
            result['shared_actor_url'] = feed_shared_actor_url[:feed_shared_actor_url.find('?mini')]
        else:
            result['shared_actor_url'] = 'unknown'
        result['content'] = (feed_shared.text).encode('gbk', errors='replace').decode('gbk') #
        ctimepart = get_by_css_selector_or_none(feed_shared, '.feed-shared-actor__sub-description', 0.5)
        if ctimepart is not None:
            result['ctime'] = ctimepart.text
        else:
            result['ctime'] = 'unknown'
        likers_button = get_by_css_selector_or_none(feed_shared, '.feed-shared-social-counts__num-likes', 0.5)
        if likers_button is not None:
            result['like_count'] = likers_button.text
        else:
            result['like_count'] = '0'
        result['comment_count'], result['comment'] = extracts_comment_simple(feed_shared)
        results.append(result)
    return results

def insert_info(profile):
    '''
     profile 
    '''
    try:
        sql = '''INSERT INTO users (profileId, name,  entity_name, headline, location, publicIdentifier) VALUES ("%s", "%s", "%s", "%s", "%s", "%s")''' % (profile['profileId'], profile['name'], profile['entity_name'], profile['headline'], profile['location'], profile['publicIdentifier'])
        #logging.info(sql)
        Conf1.db_cur.execute(sql) #Duplicate entry
        Conf1.db_temp.commit()
    except Exception as e:
        logging.info(e)
        #logging.info('[-] insert_info error!!')

def insert_url(url):
    '''
     user url 
    '''
    try:
        Conf1.db_cur.execute('INSERT INTO usersurl (user_url) VALUES ("%s")' % (url))
    except:
        return

def insert_feeds(feeds):
    for feed in feeds:
        try:
            sql = '''INSERT INTO feeds (shared_actor_url, content,  ctime, like_count, comment_count, comment) VALUES ("%s", "%s", "%s", "%s", "%s", "%s")''' % (feed['shared_actor_url'], feed['content'], feed['ctime'], feed['like_count'], feed['comment_count'], feed['comment'])
            Conf1.db_cur.execute(sql) #Duplicate entry
        except Exception as e:
            try:
                sql = '''INSERT INTO feeds (shared_actor_url, content,  ctime, like_count, comment_count, comment) VALUES ("%s", "%s", "%s", "%s", "%s", "%s")''' % (feed['shared_actor_url'], 'unknown', feed['ctime'], feed['like_count'], feed['comment_count'], feed['comment'])
                Conf1.db_cur.execute(sql)
            except:
                print(e)
    Conf1.db_temp.commit()

def get_friends(driver):
	NETWORK_URL = Conf1.START_URL1
	driver.get(NETWORK_URL)
	useritem = get_by_css_selector_or_none(driver, '.mn-connection-card__link.ember-view', 1)
	if useritem is not None:
		js="var q=document.documentElement.scrollTop=10000" 
		driver.execute_script(js) #
		time.sleep(1)
		userlist = driver.find_elements_by_css_selector('.mn-connection-card__link.ember-view')
	else:
	    logging.info('[-] Cannot find user network infomation!')
	    sys.exit(0)
	logging.info(len(userlist))
	logging.info('[+] Get the whole user url list....')
	my_friends = []
	for user in userlist:
	    #logging.info(user.text)  #
	    user_url = user.get_attribute('href') #
	    insert_url(user_url)

	Conf1.db_temp.commit()

def get_url_all(username):
    '''
    '''
    driver = init_chromium()
    login(driver, username, Conf1.password)
    get_friends(driver)
    Conf1.db_url_cur.execute('select * from usersurl')
    user_url = Conf1.db_url_cur.fetchone()
    while (user_url != None):
        if user_url[0] == 'https://www.linkedin.com/in/unavailable/':
            user_url = Conf1.db_url_cur.fetchone()
        else:
            driver.get(user_url[0])
            profile = extracts_user_simple_info(driver)
            insert_info(profile)
            search_more_user(driver, profile['profileId'], max_page=Conf1.max_page, start_page=1) #maxpage  max_page *10
            user_url = Conf1.db_url_cur.fetchone()
            time.sleep(1)
    driver.close()

def get_info_feed(usename, start=0, get_feed=False):
    driver = init_chromium()
    login(driver, usename, Conf1.password)
    Conf1.db_url_cur1.execute('select * from usersurl')
    Conf1.db_url_cur1.scroll(start)
    user_url = Conf.db_url_cur1.fetchone()
    while (user_url != None):
        if user_url[0] == 'https://www.linkedin.com/in/unavailable/':
            user_url = Conf1.db_url_cur1.fetchone()
        else:
            driver.get(user_url[0])
            profile = extracts_user_simple_info(driver)
            insert_info(profile)
            time.sleep(3)
            if get_feed == True:
                feeds = extracts_user_feed_simple(driver, user_url[0])
                insert_feeds(feeds)
            user_url = Conf1.db_url_cur1.fetchone()
            Conf1.current_num += 1
            if Conf1.current_num > Conf1.max_num:
                Conf1.current_num = 0
                break
    driver.close()


logging.info('[+] The datebase works well.')
logging.info('[*] Now get the users url...')
get_url_all(Conf1.username3)
logging.info('[*] Now get the users info and feeds...')
users = ['XXXXXXXX', 'XXXXXXXX', 'XXXXXXXX', 'XXXXXXXX']
num = 1
while (num < 9):
    j = 0
    for user in users:
        logging.info('[*] Now get the user {}'.format(user))
        get_info_feed(user, start=(num*200 + j*50))
        j += 1
        time.sleep(10)
    num += 1
