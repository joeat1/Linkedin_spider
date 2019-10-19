#coding=utf-8
import pymysql

class Conf():
    username1= "XXXXXX"
    username2 = "XXXXXX"
    password = "*******"

    db_temp = pymysql.connect("localhost","root","root","linkedin" )
    db_cur = db_temp.cursor()
    
class Conf1():
    username = "XXXXXXX"
    username1= "XXXXXX" 
    username2 = "XXXXXX"
    username3 = 'XXXXXX'
    username4 = 'XXXXXX'
    password = "********"

    current_num = 0
    max_num = 50     
    max_page = 10          
    Chromeheadless = False
    START_URL1 = 'https://www.linkedin.com/mynetwork/invite-connect/connections/'
    START_URL2 = "https://www.linkedin.com/in/jeffweiner08"                       
    START_URL3 = 'https://www.linkedin.com/search/results/people/?facetNetwork=["S"]&origin=FACETED_SEARCH&page=1'
    #
    db_temp = pymysql.connect("localhost","root","root","linkedin" )
    db_cur = db_temp.cursor()  #
    db_url_cur = db_temp.cursor() #
    db_url_cur1 = db_temp.cursor()
