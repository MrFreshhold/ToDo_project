import sqlite3


class ToDoList:
    def __init__(self,file_name: str):
        '''Класс программы ToDoList'''

        self.file_name = file_name

        self.connect = sqlite3.connect(f"{self.file_name}.db")
        self.cur = self.connect.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS users
                        (id INTEGER PRIMARY KEY,
                         password TEXT, 
                         name TEXT)""" )
        '''Таблица пользователей'''

        self.cur.execute("""CREATE TABLE IF NOT EXISTS task_list
                        (id INTEGER PRIMARY KEY, 
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

        self.cur.execute("""SELECT id FROM task_list""")
        id_list = self.cur.fetchall()
        new_id = len(id_list) + 1
        '''блок создания нового порядкового айди задачи'''

        self.cur.execute(f"""INSERT INTO task_list (id, name, text, deadline, status, importance, user_id)
                         VALUES({new_id}, '{name}', '{text}', '{deadline}', '{status}', '{importance}', {user_id})""")
        
        self.connect.commit()
        
    
    def read(self, user_id: int):
        '''метод класса для вывода задач по определенному user_id. для вывода всех задач введите 0 id'''

        if (user_id == 0):
            user_id = '*'

        self.cur.execute(f"""SELECT * FROM task_list WHERE user_id = {user_id}""")
        tasks = self.cur.fetchall()

        for task in tasks:
            print(task)
    

    def update_task(self, id: int, status: str):
        '''обновление статуса задачи по ее id'''
        
        try:
            
            self.cur.execute(f"""UPDATE task_list SET status = '{status}' WHERE id = {id}""")

        except: 

            print('Возникла ошибка')

        self.connect.commit()
    
    
    def delete(self, id: int):
        '''удаление задачи по ее айди'''

        self.cur.execute(f"""DELETE FROM task_list WHERE id = {id}""")

        self.connect.commit()

        print('Задача удалена')



class User:
    def __init__(self,file_name: str):
        '''Класс пользователя с уникальным порядковым айди и именем и почти личным паролем'''

        self.file_name = file_name
        self.connect = sqlite3.connect(f"{self.file_name}.db")
        self.cur = self.connect.cursor()


    def create_user(self, user_name: str, password: str):

        self.cur.execute("""SELECT id FROM users""")
        id_list = self.cur.fetchall()
        new_id = len(id_list) + 1
        '''создание порядкового айди пользователя'''

        self.cur.execute("""SELECT name FROM users""")
        name_list = self.cur.fetchall()

        while (True):

            for names in name_list:

                for name in names:

                    if (name == user_name):

                        user_name = input('имя пользователя существует, введите другое: ')

            break
        '''проверка существующих  имен. 2 цикла for так как получаем массив из списков и их тоже надо открыть'''

        self.cur.execute(f"""INSERT INTO users (id, name, password) VALUES ({new_id}, '{user_name}', '{password}')""")

        self.connect.commit()
    

    def check_id(self, name: str):
        '''проверка своего айди по имени пользователя'''
        
        self.cur.execute(f"""SELECT id FROM users WHERE name = '{name}'""")
        id = self.cur.fetchall()

        print(id)







FirstList = ToDoList('first_list')

# cjplfybt gjkmpjdfntkz
Danil = User('first_list')
# Danil.create_user('Danil', '123')
Danil.check_id('Danil')

# коннект для работы с бд
connect = sqlite3.connect(f"first_list.db")
cur = connect.cursor()

# вывод списка имен
# cur.execute("""SELECT name FROM users """)
# names = cur.fetchall()
# for name in names:
#     for user_name in name:
#         print (user_name)

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
