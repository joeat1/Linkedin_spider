#coding=utf-8
import pymysql
import sys

class Operate_table(object):

    def __init__(self):
        self.username = 'root'
        self.password = 'root'
        self.host = 'localhost'
        self.database = 'linkedin2'
        self.conn = pymysql.connect(self.host, self.username, self.password, self.database)
        self.cur = self.conn.cursor()

    def create_table(self):
        sql = '''CREATE TABLE users (
                 publicIdentifier VARCHAR(100) primary key not null,
                 name text null,
                 entity_name text null,
                 headline text null,
                 location text null,
                 profileId text not null)'''
        self.cur.execute(sql)
        '''CREATE TABLE users (
                 publicIdentifier VARCHAR(100) primary key not null,
                 lastName text null,
                 firstName text null,
                 occupation text null,
                 profileId text not null,
                 phoneNumbers text null,
                 address text null,
                 emailAddress text null)
        '''
        print('[+] The table users is created')

        sql = '''CREATE TABLE feeds (
                 id integer primary key AUTO_INCREMENT not null,
                 shared_actor_url text null,
                 content text null,
                 ctime text null,
                 like_count text not null,
                 comment_count text not null,
                 comment text null)'''
        self.cur.execute(sql)
        '''CREATE TABLE feeds (
                 id integer primary key AUTO_INCREMENT not null,
                 publicIdentifier text null,
                 content text null,
                 ctime text null,
                 like_count integer not null,
                 comment_count integer not null)'''
        print('[+] The table feeds is created')
        sql = '''CREATE TABLE usersurl (
                 user_url VARCHAR(100) primary key not null)'''
        self.cur.execute(sql)
        print('[+] The table usersurl is created')

    def drop_table(self):
        self.cur.execute('drop table users')
        self.cur.execute('drop table feeds')
        self.cur.execute('drop table usersurl')

if __name__ == '__main__':
    app = Operate_table()
    argv = sys.argv[1]
    
    if argv == 'create_table':
        app.create_table()
    elif argv == 'drop_table':
        app.drop_table()
    else:
        print("please set create_table or drop_table")
        raise ValueError
