import sqlite3
from flask import g, current_app # Импортируем g и current_app из Flask

# Функция для получения соединения с базой данных
# Она будет создавать соединение для каждого запроса, если его еще нет в g
def get_db():
    # Проверяем, есть ли уже соединение в объекте g для текущего запроса
    db = getattr(g, '_database', None)
    if db is None:
        # Если нет, создаем новое соединение.
        # current_app.instance_path гарантирует правильный путь к папке instance
        database_path = current_app.instance_path + '/data.db'
        db = g._database = sqlite3.connect(database_path)
        # Устанавливаем row_factory, чтобы результаты fetchall/fetchone были доступны как словари
        db.row_factory = sqlite3.Row
    return db

# Функция для закрытия соединения с базой данных
# Она будет вызываться автоматически после каждого запроса
def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- Ваши функции для работы с БД, теперь они получают соединение через get_db() ---

def add_new_task(paramsArr, dataArr:tuple):
    conn = get_db()
    cursor = conn.cursor()
    
    if (len(paramsArr) == len(dataArr)) or (paramsArr == '*'):
        if (paramsArr == '*'):
            paramsArr = ["user_id", "text", "task_time", "task_date", 
                         "when_puplished_time", "when_published_date", 
                         "when_edited_time", "when_edited_date"]
        
        sqlStr = 'INSERT INTO users ('
        sqlStr += ', '.join(paramsArr) # Более питонический способ
        sqlStr += ') VALUES ('
        sqlStr += ', '.join(['?' for _ in paramsArr]) # Заполнители для каждого параметра
        sqlStr += ')'
        
        cursor.execute(sqlStr, dataArr)
        conn.commit()
    else:
        print("Ошибка в add_new_task (кол-во параметров и инфы не совпадает)!!!")

def delete_user_data_by_id(userId):
    conn = get_db()
    cursor = conn.cursor()
    # Используем параметризованный запрос для безопасности!
    cursor.execute('DELETE FROM users WHERE user_id = ?', (userId,))
    conn.commit()

def open_user_tasks(userId):
    conn = get_db()
    cursor = conn.cursor()
    # Используем параметризованный запрос для безопасности!
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (userId,))
    return cursor.fetchall()

# Функция для инициализации схемы базы данных (создания таблиц)
# Вызывайте ее один раз при первом запуске или при деплое
def init_db():
    with current_app.app_context():
        db = get_db()
        cursor = db.cursor()
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
        db.commit()


# --- Уберите все прямые вызовы функций add_new_task, delete_user_data_by_id, SELECT * FROM users
#     из этого файла, так как они должны вызываться только из Flask-приложения.
#     Они могут быть использованы для тестирования, но не в "боевом" файле утилит БД.