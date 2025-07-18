import sqlite3

def get_user_data_by_id(db_name: str, user_id: int):
    """
    Получает все данные пользователя из таблицы 'users' по user_id.

    Args:
        db_name (str): Имя файла базы данных SQLite.
        user_id (int): Идентификатор пользователя, данные которого нужно получить.

    Returns:
        list of tuples: Список кортежей, где каждый кортеж представляет строку
                        с данными пользователя. Возвращает пустой список, если
                        пользователь не найден или произошла ошибка.
    """
    conn = None
    try:
        # Подключение к базе данных SQLite
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Создание таблицы, если она еще не существует (используем вашу схему)
        # Этот шаг важен, чтобы функция работала даже с новой/пустой базой данных
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
        conn.commit() # Сохраняем изменения (создание таблицы)

        # Выполнение запроса SELECT для получения данных по user_id
        # Используем параметризованный запрос для предотвращения SQL-инъекций
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))

        # Получение всех найденных строк
        rows = cursor.fetchall()
        return rows

    except sqlite3.Error as e:
        print(f"Ошибка базы данных при получении данных: {e}")
        return []
    finally:
        # Закрытие соединения с базой данных
        if conn:
            conn.close()

def create_user_data(db_name: str, user_id: int, text: str, task_time: str,
                     task_date: str, when_puplished_time: str,
                     when_published_date: str, when_edited_time: str,
                     when_edited_date: str):
    """
    Создает новую запись в таблице 'users'.

    Args:
        db_name (str): Имя файла базы данных SQLite.
        user_id (int): Идентификатор пользователя.
        text (str): Текст задачи.
        task_time (str): Время задачи.
        task_date (str): Дата задачи.
        when_puplished_time (str): Время публикации.
        when_published_date (str): Дата публикации.
        when_edited_time (str): Время последнего редактирования.
        when_edited_date (str): Дата последнего редактирования.

    Returns:
        bool: True, если запись успешно создана, False в противном случае.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Убедимся, что таблица существует
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

        cursor.execute('''
            INSERT INTO users (user_id, text, task_time, task_date,
                               when_puplished_time, when_published_date,
                               when_edited_time, when_edited_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, text, task_time, task_date,
              when_puplished_time, when_published_date,
              when_edited_time, when_edited_date))
        conn.commit()
        print(f"Запись для пользователя {user_id} успешно создана.")
        return True
    except sqlite3.Error as e:
        print(f"Ошибка базы данных при создании записи: {e}")
        return False
    finally:
        if conn:
            conn.close()

def delete_user_data_by_id(db_name: str, user_id: int):
    """
    Удаляет все записи для указанного user_id из таблицы 'users'.

    Args:
        db_name (str): Имя файла базы данных SQLite.
        user_id (int): Идентификатор пользователя, записи которого нужно удалить.

    Returns:
        bool: True, если записи успешно удалены, False в противном случае.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Убедимся, что таблица существует
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

        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Записи для пользователя {user_id} успешно удалены. Удалено строк: {cursor.rowcount}")
            return True
        else:
            print(f"Записи для пользователя {user_id} не найдены для удаления.")
            return False
    except sqlite3.Error as e:
        print(f"Ошибка базы данных при удалении записей: {e}")
        return False
    finally:
        if conn:
            conn.close()

# --- Пример использования ---
if __name__ == "__main__":
    database_name = 'instance/data.db' # Имя файла вашей базы данных
    delete_user_data_by_id(database_name, 45)

    print(get_user_data_by_id(database_name, 45))

