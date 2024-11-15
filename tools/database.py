import sqlite3
from contextlib import contextmanager

# prevent repeating connection for every function
@contextmanager
def connect_db():
    conn = sqlite3.connect('islands.db')
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        conn.close()

# initialize database
def create_db():
    with connect_db() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                       user_id INTEGER PRIMARY KEY,
                       user_name TEXT UNIQUE NOT NULL,
                       real_name TEXT,
                       age INTEGER,
                       gender TEXT,
                       job TEXT,
                       location TEXT
                            
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS connections (
                       connection_id INTEGER PRIMARY KEY,
                       user_id INTEGER NOT NULL,
                       target_user_id INTEGER NOT NULL,
                       connection_type TEXT CHECK (connection_type IN ('follows','friends', 'co-worker', 'blocked', 'has read posts by')),
                       FOREIGN KEY (user_id) REFERENCES users(user_id),
                       FOREIGN KEY (target_user_id) REFERENCES users(user_id)
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                       post_id INTEGER PRIMARY KEY,
                       user_id INTEGER NOT NULL,
                       content TEXT NOT NULL,
                       post_date TEXT DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                       comment_id INTEGER PRIMARY KEY,
                       user_id INTEGER NOT NULL,
                       post_id INTEGER NOT NULL,
                       content TEXT NOT NULL,
                       comment_date TEXT DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (user_id) REFERENCES users(user_id),
                       FOREIGN KEY (post_id) REFERENCES posts(post_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS views (
                       view_id INTEGER PRIMARY KEY,
                       post_id INTEGER NOT NULL,
                       user_id INTEGER NOT NULL,
                       view_time TEXT DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (post_id) REFERENCES posts(post_id),
                       FOREIGN KEY (user_id) REFERENCES users(user_id)
            
            )
        ''')
        
        # seed database if empty
        if cursor.execute('SELECT COUNT(*) from users').fetchone()[0] == 0:
            seed_db(cursor)

def seed_db(cursor=None):
    if cursor is None:
        with connect_db() as cursor:
            seed_db(cursor)
            return
    
    # prevent duplication
    if cursor.execute('SELECT COUNT(*) from users').fetchone()[0] == 0:

        # (user_name, real_name, age, gender, job, location)
        users_data = [
            ("john_doe", "John Doe", 30, "Male", "Doctor", "USA"),                      # user id 1
            ("jane_doe", "Jane Doe", 28, "Female", "Teacher", "USA"),                   # user id 2
            ("mohammad_singh", "Mohammad Singh", 27, "Male", "Engineer", "IND"),        # user id 3
            ("susan_kim", "Susan Kim", 38, "Female", "Nurse", "KOR"),                   # user id 4
            ("ana_souza", "Ana Souza", 16, "Female", "Student", "BRA"),                 # user id 5
            ("elena_martinez", "Elena Martinez", 25, "Female", "Designer", "MEX"),      # user id 6
            ("sergei_petrov", "Sergei Petrov", 45, "Male", "Entrepreneur", "RUS"),      # user id 7
            ("elon_musk", "Elon Musk", 53, "Male", "CEO", "USA"),                       # user id 8
            ("jackie_chan", "Jackie Chan", 70, "Male", "Actor", "CHN"),                 # user id 9
            ("nicki_minaj", "Nicki Minaj", 41, "Female", "Singer", "TTO")               # user id 10
        ]

        # (user_id, target_user_id, connection_type)
        # some are bidirectional
        connections_data = [
            # "follows" connections
            (1, 2, "follows"), # John and Jane follow eachother
            (2, 1, "follows"),
            (5, 10, "follows"), # Ana follows Nicki

            # "friends" connections
            (4, 6, "friends"), # Susan and Elena are friends
            (6, 4, "friends"),
            (8, 9,"friends"), # Elon and Jackie are friends
            (9, 8, "friends"),

            # "co-worker" connections
            (3, 7, "co-worker"), # Mohammad and Sergei are co-workers
            (7, 3, "co-worker"),
            (1, 4, "co-worker"), # John and Susan are co-workers
            (4, 1, "co-worker"),

            # "blocked" connections
            (10, 8, "blocked"), # Nicki blocked Elon
            (6, 2, "blocked"), # Elena blocked Jane

            # "has read posts by" connections
            (6, 9, "has read posts by"), # Elena has read posts by Jackie
            (3, 8, "has read posts by"), # Mohammad has read posts by Elon
        ]

        # (post_id, user_id, content, post_date)
        posts_data = [
            (1, 1, "Blah Blah Blah", "2024-01-01 12:00:00"),
            (2, 2, "Hello", "2024-01-02 12:00:00"),
            (3, 3, "Namaste", "2024-01-03 12:00:00"),
            (4, 4, "Annyeonghaseyo", "2024-01-04 12:00:00"),
            (5, 5, "Ola", "2024-01-05 12:00:00"),
            (6, 6, "Hola", "2024-01-06 12:00:00"),
            (7, 7, "Privet", "2024-01-07 12:00:00"),
            (8, 8, "Hello World!", "2024-01-08 12:00:00"),
            (9, 9, "Ni hao", "2024-01-09 12:00:00"),
            (10, 10, "Hello", "2024-01-10 12:00:00")
        ]

    