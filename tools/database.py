import sqlite3
from contextlib import contextmanager

# prevent repeating connection for every function
@contextmanager
def connect_db():
    conn = sqlite3.connect('networks.db')
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
            )
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

        cursor.executemany('''
                        INSERT INTO users (user_name, real_name, age, gender, job, location) VALUES (?, ?, ?, ?, ?, ?)
                        ''', users_data)

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

        cursor.executemany('''
                        INSERT INTO connections (user_id, target_user_id, connection_type) VALUES (?, ?, ?)
                        ''', connections_data)

        # (post_id, user_id, content, post_date)
        
        posts_data = [
            # John's posts
            (1, 1, "As a doctor, I am constantly inspired by the resilience of my patients. Each day brings new challenges, but also incredible opportunities to make a difference in someone's life.", "2024-01-01 12:00:00"),
            # Jane's posts
            (2, 2, "Teaching young minds is both a privilege and a responsibility. I love finding creative ways to make learning fun and impactful for my students.", "2024-01-02 12:00:00"),
            # Mohammad's posts
            (3, 3, "Engineering has taught me to think critically and solve problems effectively. Today, I'm working on an innovative project that could positively impact millions.", "2024-01-03 12:00:00"),
            # Susan's posts
            (4, 4, "Nursing is not just a job—it's a calling. Helping patients recover and seeing their smiles reminds me why I chose this path.", "2024-01-04 12:00:00"),
            # Ana's posts
            (5, 5, "Life as a student is a whirlwind of exams, friendships, and endless possibilities. I'm excited about what the future holds!", "2024-01-05 12:00:00"),
            # Elena's posts
            (6, 6, "Designing is my passion. I love creating visuals that not only look good but also tell a compelling story.", "2024-01-06 12:00:00"),
            # Sergei's posts
            (7, 7, "Entrepreneurship is a journey of constant learning and adapting. I'm excited to share some new insights from my latest venture.", "2024-01-07 12:00:00"),
            # Elon's posts
            (8, 8, "Innovation is the driving force of progress. Today, I want to share some thoughts on sustainable energy solutions for a better tomorrow.", "2024-01-08 12:00:00"),
            # Jackie's posts
            (9, 9, "Martial arts taught me discipline and perseverance. These lessons have shaped who I am both on and off the screen.", "2024-01-09 12:00:00"),
            # Nicki's posts
            (10, 10, "Music is my sanctuary. Through every note and lyric, I strive to connect with people and share my story.", "2024-01-10 12:00:00")
        ]


        cursor.executemany('''
                        INSERT INTO posts (post_id, user_id, content, post_date) VALUES (?, ?, ?, ?)
                        ''', posts_data)

        # (comment_id, user_id, post_id, content, comment_date)
        comments_data = [
            # John's comments
            (1, 1, 1, "I really liked the way you expressed your thoughts. Keep it up!", "2024-01-01 12:01:00"),
            # Jane's comments
            (2, 2, 1, "It's great to see someone sharing this kind of positivity. Looking forward to more!", "2024-01-02 12:02:00"),
            # Mohammad's comments
            (3, 3, 1, "It's refreshing to read something so thoughtful. Great work!", "2024-01-03 12:03:00"),
            # Susan's comments
            (4, 4, 1, "I appreciate the effort you put into writing this. Keep inspiring others!", "2024-01-04 12:04:00"),
            # Ana's comments
            (5, 5, 1, "Your words really resonated with me. Thank you for sharing!", "2024-01-05 12:05:00"),
            # Elena's comments
            (6, 6, 1, "This is exactly the kind of content I enjoy. Keep writing more!", "2024-01-06 12:06:00"),
            # Sergei's comments
            (7, 7, 1, "Your perspective is unique, and I find it very interesting. Good job!", "2024-01-07 12:07:00"),
            # Elon's comments
            (8, 8, 1, "It's always a pleasure reading your updates. Very inspiring!", "2024-01-08 12:08:00"),
            # Jackie's comments
            (9, 9, 1, "Thanks for sharing such an uplifting message. Keep up the great work!", "2024-01-09 12:09:00"),
            # Nicki's comments
            (10, 10, 1, "Your writing has a way of connecting with readers. Can't wait for more!", "2024-01-10 12:10:00"),
        ]


        cursor.executemany('''
                        INSERT INTO comments (comment_id, user_id, post_id, content, comment_date) VALUES (?, ?, ?, ?, ?)
                        ''', comments_data)

        # (post_id, user_id, view_time)
        views_data = [
            # John's views
            (1, 1, "2024-01-01 12:01:00"),
            (1, 3, "2024-01-01 12:03:00"),
            (1, 5, "2024-01-01 12:05:00"),

            # Jane's views
            (2, 2, "2024-01-02 12:02:00"),
            (2, 4, "2024-01-02 12:04:00"),
            (2, 6, "2024-01-02 12:06:00"),

            # Mohammad's views
            (3, 1, "2024-01-03 12:01:00"),
            (3, 4, "2024-01-03 12:04:00"),
            (3, 7, "2024-01-03 12:07:00"),

            # Susan's views
            (4, 2, "2024-01-04 12:02:00"),
            (4, 5, "2024-01-04 12:05:00"),
            (4, 8, "2024-01-04 12:08:00"),

            # Ana's views
            (5, 1, "2024-01-05 12:01:00"),
            (5, 3, "2024-01-05 12:03:00"),
            (5, 9, "2024-01-05 12:09:00"),

            # Elena's views
            (6, 2, "2024-01-06 12:02:00"),
            (6, 4, "2024-01-06 12:04:00"),
            (6, 10, "2024-01-06 12:10:00"),

            # Sergei's views
            (7, 3, "2024-01-07 12:03:00"),
            (7, 6, "2024-01-07 12:06:00"),
            (7, 8, "2024-01-07 12:08:00"),

            # Elon's views
            (8, 1, "2024-01-08 12:01:00"),
            (8, 5, "2024-01-08 12:05:00"),
            (8, 9, "2024-01-08 12:09:00"),

            # Jackie's views
            (9, 2, "2024-01-09 12:02:00"),
            (9, 4, "2024-01-09 12:04:00"),
            (9, 7, "2024-01-09 12:07:00")
        ]

        cursor.executemany('''
                           INSERT INTO views (post_id, user_id, view_time) VALUES (?, ?, ?)
                        ''', views_data)


def reset_db():
    with connect_db() as cursor:
        cursor.execute('DROP TABLE IF EXISTS users')
        cursor.execute('DROP TABLE IF EXISTS connections')
        cursor.execute('DROP TABLE IF EXISTS posts')
        cursor.execute('DROP TABLE IF EXISTS comments')
        cursor.execute('DROP TABLE IF EXISTS views')
        create_db()