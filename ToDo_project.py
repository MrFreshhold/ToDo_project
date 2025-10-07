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
                         password TEXT NOT NULL)""" )
        '''Таблица пользователей'''

        self.cur.execute("""CREATE TABLE IF NOT EXISTS task_list
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         name TEXT NOT NULL, 
                         text TEXT, 
                         deadline TEXT, 
                         status TEXT, 
                         importance TEXT,
                         user_id INTEGER,
                         FOREIGN KEY (user_id) REFERENCES users (id)
                         )""")
        '''Таблица (лист) задач, привязанных к юзер айди'''

        self.connect.commit()

    
    def create_task(self, name: str, text: str, deadline: str, importance: str, user_id: int):
        '''метод класса для создания задачи с пользовательскими параметрами и порядковым айди'''

        status = 'выдана'
        sql = """INSERT INTO task_list (name, text, deadline, status, importance, user_id) VALUES (?,?,?,?,?,?)"""
        self.cur.execute(sql, (name, text, deadline, status, importance, user_id))
        
        self.connect.commit()
        
    
    def read_task(self, user_id: int):
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
    
    
    def delete_task(self, id: int):
        '''удаление задачи по ее айди'''

        sql = """DELETE FROM task_list WHERE id = ?"""
        self.cur.execute(sql, (id,))

        self.connect.commit()

        print('Задача удалена')

    
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


    def check_user(self, login: str, password: str):
        '''возвращает статус входа в булевом формате'''

        sql = """SELECT * FROM users WHERE login = ? AND password = ?"""
        self.cur.execute(sql, (login, password))

        status = self.cur.fetchall()

        if (len(status) > 0):

            status = 1
        
        else:

            status = 0
        
        return status



file_name = input('Это программа TODO подключаемая к вашей БД, если БД не существует, будет создана новая \nвведите имя файла: ')
task_list = ToDoList(file_name)


while (True):

    answer = input('хотите 1. войти или 2. зарегистрироваться?')

    if (answer.lower() == 'войти' or answer == '1' ):

        log = input('введите логин пользователя: ')
        pas = input('введите пароль: ')

        status = task_list.check_user(log, pas)

        if (status == 1):

            print ('вы успешно вошли!')
            break
        
        else:

            print ('логин или пароль указаны неверно')


    elif (answer.lower() == 'зарегистрироваться' or answer == '2'):

        log = input('введите логин пользователя: ')
        name = input(' введите имя пользователя')
        pas = input('введите пароль: ')
        
        task_list.create_user(log, name, pas)

        
    else:

        print('такой команды не существует')

while (True):

    answer = input('что вы хотите сделать?' \
    '1. создать задачу' \
    '2. просмотреть задачи по id пользователя' \
    '3. обновить статус задачи' \
    '4. удалить задачу')

    if (answer == 1):

        name = input('имя задачи')
        text =input('задачу')
        deadline = input('дедлайн задачи')
        importance = input('приоритет задачи')
        user_id = input('id пользователя')
        user_id = int(user_id)

        task_list.create_task(name, text, deadline, importance, user_id)

    elif (answer == 2):

        id = input('введите id пользователя')
        id = int(id)
        task_list.read_task(id)

    elif (answer == 3):

        id = input('введите id задачи')
        id = int(id)
        status = input('введите статус задачи')

        task_list.update_task(id, status)

    elif (answer == 4):

        id = ('введите id задачи для ее удаления')
        task_list.delete_task(id)
    
    else:

        print('Такой команды не существует.')