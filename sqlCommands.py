import sqlite3

# Подключение (создаст файл, если не существует)
conn = sqlite3.connect('instance/data.db')
cursor = conn.cursor()

# 1. Создание таблицы
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER,
    text TEXT NOT NULL,
    task_time TEXT,
    task_date TEXT,
    when_puplished_time TEXT,
    when_published_date TEXT,
    when_edited_time TEXT,
    when_edited_date TEXT
)
''')


def add_new_task(paramsArr, dataArr:tuple):
    if  ( len(paramsArr) == len(dataArr) ) or (paramsArr == '*'):
        if (paramsArr == '*'):
            paramsArr = ["user_id", "text", "task_time", "task_date", "when_puplished_time", "when_published_date", "when_edited_time", "when_edited_date"]
        sqlStr = 'INSERT INTO users ('
        for i in range(len(paramsArr)-1):
            sqlStr += paramsArr[i]+', '
        sqlStr += paramsArr[len(paramsArr)-1]

        sqlStr += ') VALUES ('
        for i in range(len(paramsArr)-1):
            sqlStr += '?, '
        sqlStr += '?)'
        
        cursor.execute(sqlStr, dataArr)
        conn.commit()
    else:
        print("Ошибка в аdd_new_task (кол-во параметров и инфы не совпадает)!!!")

def delete_user_data_by_id(userId):
    cursor.execute(f'DELETE FROM users WHERE user_id = {userId};')
    conn.commit()


cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()
print(rows)

#delete_user_data_by_id(10010202)

#add_new_task("*", (112203293, "Hello", "15:35", "25.07.25", "17:18:45", "23.07.25", None, None))

cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()
print(rows)