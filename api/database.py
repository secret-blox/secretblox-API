import pymysql.cursors

connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='secretblox',
        cursorclass=pymysql.cursors.DictCursor
)