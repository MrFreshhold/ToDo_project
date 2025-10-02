import sqlite3


class ToDoList:
    def __init__(self,file_name: str):
        '''Класс программы ToDoList'''

        self.file_name = file_name

        self.connect = sqlite3.connect(f"{self.file_name}.db")
        self.cur = self.connect.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS users
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         login TEXT UNIQUE NOT NULL, 
                         name TEXT NOT NULL,
                         password TEXT UNIQUE NOT NULL)""" )
        '''Таблица пользователей'''

        self.cur.execute("""CREATE TABLE IF NOT EXISTS task_list
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         name TEXT, 
                         text TEXT, 
                         deadline TEXT, 
                         status TEXT, 
                         importance TEXT,
                         user_id INTEGER,
                         FOREIGN KEY (user_id) REFERENCES users (id)
                         )""")
        '''Таблица (лист) задач, привязанных к юзер айди'''

        self.connect.commit()

    
    def create(self, name: str, text: str, deadline: str, status: str, importance: str, user_id: int):
        '''метод класса для создания задачи с пользовательскими параметрами и порядковым айди'''

        sql = """INSERT INTO task_list (name, text, deadline, status, importance, user_id) VALUES (?,?,?,?,?,?)"""
        self.cur.execute(sql, (name, text, deadline, status, importance, user_id))
        
        self.connect.commit()
        
    
    def read(self, user_id: int):
        '''метод класса для вывода задач по определенному user_id. для вывода всех задач введите 0 id'''

        if (user_id == 0):
            user_id = '*'

        sql = """SELECT * FROM task_list WHERE user_id = ?"""
        self.cur.execute(sql, (user_id,))
        tasks = self.cur.fetchall()

        for task in tasks:
            print(task)
    

    def update_task(self, id: int, status: str):
        '''обновление статуса задачи по ее id'''
        
        try:
            
            sql = """UPDATE task_list SET status = ? WHERE id = ?"""
            self.cur.execute(sql, (status, id))

        except: 

            print('Возникла ошибка')

        self.connect.commit()
    
    
    def delete(self, id: int):
        '''удаление задачи по ее айди'''

        sql = """DELETE FROM task_list WHERE id = ?"""
        self.cur.execute(sql, (id,))

        self.connect.commit()

        print('Задача удалена')



class User:
    def __init__(self,file_name: str):
        '''Класс пользователя с уникальным порядковым айди и именем и почти личным паролем'''

        self.file_name = file_name
        self.connect = sqlite3.connect(f"{self.file_name}.db")
        self.cur = self.connect.cursor()


    def create_user(self, user_login: str, name: str, password: str):


        sql = """INSERT INTO users (name, login, password) VALUES (?, ?, ?)"""
        self.cur.execute(sql, (name, user_login, password))

        self.connect.commit()
    

    def check_id(self, login: str):
        '''проверка своего айди по логину пользователя'''
        
        sql = """SELECT id FROM users WHERE login = ?"""
        self.cur.execute(sql, (login,))
        id = self.cur.fetchall()

        print(id)





FirstList = ToDoList('first_list')

# cjplfybt gjkmpjdfntkz
Danil = User('first_list')
Danil.create_user('Mrf','Danil', '123')
Danil.check_id('Mrf')

# коннект для работы с бд
connect = sqlite3.connect(f"first_list.db")
cur = connect.cursor()

# вывод списка логинов
cur.execute("""SELECT login FROM users""")
logins = cur.fetchall()
for login in logins:
    for user_login in login:
        print (user_login)

# проверка указания айди задачи
# cur.execute("""SELECT id FROM task_list""")
# id_list = cur.fetchall()
# new_id = len(id_list) + 1
# print(id_list)
# print(new_id)

# создание, проверка и удаление задачи
FirstList.create('задача 1', 'тест', 'сегодня', 'выдана', 'важная', 1)

FirstList.read(1)

FirstList.delete(1)
