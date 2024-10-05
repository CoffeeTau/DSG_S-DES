# -*- coding: utf-8 -*-
"""
连接和操作数据库
"""
import pymysql
import hashlib  # 用于密码哈希

def init_conn():  # 初始化数据库连接
    return pymysql.connect(
        host="127.0.0.1",  # 数据库的IP地址
        user="root",  # 数据库用户名称
        password="Ljj200402260522",  # 数据库用户密码
        db="SDES",  # 数据库名称
        port=3306,  # 数据库端口名称
        charset="utf8mb4"  # 数据库的编码方式
    )

def execute_with_bool(sql_str, args=()):  # 执行SQL语句 （SQL语句，SQL语句的参数） ---插入，更新，删除
    with init_conn() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql_str, args)
                conn.commit()
                return True
            except Exception as e:
                print(f"Error executing SQL: {e}")
                return False

def execute_with_list(sql_str, params=None):  # 执行对数据库的查询操作
    results = []
    with init_conn() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql_str, params)
                results = cursor.fetchall()
            except Exception as e:
                print(f"Error fetching data: {e}")
    return results

# 用户
def search_by_name(username):
    sql_str = "SELECT * FROM users WHERE username = %s"
    results = execute_with_list(sql_str, (username,))
    return results[0] if results else None  # 返回第一个匹配的用户，若无则返回None

# 用户注册
def insert_user(username, password):

    sql_str = "INSERT INTO users (username, password) VALUES (%s, %s)"
    return execute_with_bool(sql_str, (username,password))

if __name__ == "__main__":
    print(not search_by_name('123'))
