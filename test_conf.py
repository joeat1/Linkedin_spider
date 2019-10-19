#coding=utf-8
import pymysql

class Conf():
    username1= "XXXXXX"
    username2 = "XXXXXX"
    password = "*******"

    db_temp = pymysql.connect("localhost","root","root","linkedin" )
    db_cur = db_temp.cursor()
    
