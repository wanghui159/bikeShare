#-*- coding = utf-8 -*-
#@Time : 2021/4/20 17:46
#@Author : 王慧
#@File : db.py
#@Software : PyCharm
from django.db import connection
from bike import views
from django.http import HttpResponse
def mysql_connect(userName,password,email,company):
    # conn = connection(host='localhost', user='wanghui', password='XJuqiny6WP2eAwt', port=3306, database='user')
    cursor = connection.cursor()
    # sql = "INSERT INTO user values(%s,%s,%s)"
    datalist = [userName,password,email,company]
    print(datalist)
    sql = "insert into user(userName,password,email,company) values(%s,%s,%s,%s)"
    cursor.execute(sql,datalist)
    # cursor.execute("select * from user")
    # data = cursor.fetchall()
    # for i in data:
    #     print(i)
    cursor.close()


def mysql_change(userName,password,email,company):
    # conn = connection(host='localhost', user='wanghui', password='XJuqiny6WP2eAwt', port=3306, database='user')
    cursor = connection.cursor()
    # sql = "INSERT INTO user values(%s,%s,%s)"
    datalist = [password,email,company,userName]
    print(datalist)
    sql = "update user set password=%s,email=%s,company=%s where userName=%s"
    cursor.execute(sql,datalist)
    # cursor.execute("select * from user")
    # data = cursor.fetchall()
    # for i in data:
    #     print(i)
    cursor.close()

def select_All():
    cursor = connection.cursor()
    sql = "select userName from user"
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    return data

def select_userName(userName):
    cursor = connection.cursor()
    sql = "select * from user where userName=%s"
    username = (userName,)
    cursor.execute(sql, username)
    data = cursor.fetchall()
    cursor.close()
    return data

def is_password_correct(userName):
    cursor = connection.cursor()
    sql = "select password from user where userName=%s"
    username = (userName,)
    cursor.execute(sql, username)
    data = cursor.fetchall()
    cursor.close()
    return data

def save_file(userName,name,description,filePath):
    cursor = connection.cursor()
    datalist = [userName,name, description, filePath]
    print(datalist)
    sql = "insert into file(userName,name,description,filePath) values(%s,%s,%s,%s)"
    cursor.execute(sql, datalist)
    cursor.close()

def selece_file(name):
    cursor = connection.cursor()
    sql = "select filePath from file where name=%s"
    file_name = (name,)
    cursor.execute(sql, file_name)
    data = cursor.fetchall()
    cursor.close()
    return data

def select_file_all(userName):
    cursor = connection.cursor()
    sql = "select* from file where userName=%s"
    file_name = (userName,)
    cursor.execute(sql, file_name)
    data = cursor.fetchall()
    cursor.close()
    return data
