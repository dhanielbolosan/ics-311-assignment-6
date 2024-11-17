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
            # ? read posts by John
            (2, 1, "has read posts by"),
            (3, 1, "has read posts by"),
            (4, 1, "has read posts by"),
            (5, 1, "has read posts by"),
            (6, 1, "has read posts by"),
            (7, 1, "has read posts by"),
            (8, 1, "has read posts by"),
            (9, 1, "has read posts by"),
            (10, 1, "has read posts by"),
            # ? read posts by Jane
            (1, 2, "has read posts by"),
            (3, 2, "has read posts by"),
            (4, 2, "has read posts by"),
            (6, 2, "has read posts by"),
            # ? read posts by Mohammed
            (1, 3, "has read posts by"),
            (4, 3, "has read posts by"),
            (7, 3, "has read posts by"),
            (8, 3, "has read posts by"),
            (9, 3, "has read posts by"),
            # ? read posts by Susan
            (2, 4, "has read posts by"),
            (5, 4, "has read posts by"),
            (8, 4, "has read posts by"),
            # ? read posts by Ana
            (1, 5, "has read posts by"),
            (3, 5, "has read posts by"),
            (9, 5, "has read posts by"),
            # ? read posts by Elena
            (2, 6, "has read posts by"),
            (4, 6, "has read posts by"),
            (10, 6, "has read posts by"),
            # ? read posts by Sergei
            (3, 7, "has read posts by"),
            (6, 7, "has read posts by"),
            (8, 7, "has read posts by"),
            # ? read posts by Elon
            (1, 8, "has read posts by"),
            (2, 8, "has read posts by"),
            (3, 8, "has read posts by"),
            (4, 8, "has read posts by"),
            (5, 8, "has read posts by"),
            (6, 8, "has read posts by"),
            (7, 8, "has read posts by"),
            (9, 8, "has read posts by"),
            (10, 8, "has read posts by"),
            # ? read posts by Jackie
            (2, 9, "has read posts by"),
            (4, 9, "has read posts by"),
            (6, 9, "has read posts by"), # Elena has read posts by Jackie
            (7, 9, "has read posts by"),
            # ? read posts by Nicki            
            (1, 10, "has read posts by"),
            (2, 10, "has read posts by"),
            (3, 10, "has read posts by"),
            (4, 10, "has read posts by"),
            (5, 10, "has read posts by"),
            (6, 10, "has read posts by"),
            (7, 10, "has read posts by"),
            (8, 10, "has read posts by"),
            (9, 10, "has read posts by")
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
            (10, 10, "Music is my sanctuary. Through every note and lyric, I strive to connect with people and share my story.", "2024-01-10 12:00:00"),
            # John's second post
            (11, 1, "Share this post! It is flu season, so make sure you get the flu vaccine as soon as possible!", "2024-01-11 12:00:00"),
            # Elon's second post
            (12, 8, "URGENT. Who wants to go to Mars? I will take only ten volunteers.", "2024-01-12 12:00:00"),
            # Nicki's second post
            (13, 10, "My new music video just came out! See my YouTube channel.", "2024-01-13 12:00:00")
        ]


        cursor.executemany('''
                        INSERT INTO posts (post_id, user_id, content, post_date) VALUES (?, ?, ?, ?)
                        ''', posts_data)

        # (comment_id, user_id, post_id, content, comment_date)
        comments_data = [
            # Comments on John's post (post #1)
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
            # Comments on Jane's post (post #2)
            (11, 1, 2, "Jane, you are a great teacher", "2024-01-02 13:00:00"), # From John
            (12, 3, 2, "Agreed", "2024-01-02 14:00:00"), # From Mohammed
            (13, 4, 2, "Go, Jane!", "2024-01-02 15:00:00"), # From Susan
            # Comments on Mohammed's post (post #3)
            (14, 7, 3, "What is that project?", "2024-01-03 12:30:00"), # From Sergei
            (15, 3, 3, "You will see soon", "2024-01-03 13:00:00"), # From Sergei
            (16, 8, 3, "Let me know if you need any help", "2024-01-03 14:00:00"), # From Elon
            (17, 9, 3, "Same here", "2024-01-03 15:00:00"), # From Jackie
            # Comments on John's second post (post #11)
            (18, 2, 11, "I will get it later today", "2024-01-11 12:10:00"),
            (19, 3, 11, "I already got it", "2024-01-11 12:20:00"),
            (20, 4, 11, "Flu shot is important for sure.", "2024-01-11 12:30:00"),
            (21, 5, 11, "I will make sure to get it this week", "2024-01-11 12:40:00"),
            (22, 6, 11, "I do not like getting shots", "2024-01-11 12:50:00"),
            # Comments on Elon's second post (post #12)
            (23, 1, 12, "I will never want to go to Mars", "2024-01-12 12:10:00"),
            (24, 2, 12, "I want to go to Mars", "2024-01-12 12:11:00"),
            (25, 3, 12, "I want to go", "2024-01-12 12:12:00"),
            (26, 4, 12, "I want to go!", "2024-01-12 12:13:00"),
            (27, 5, 12, "I want to go!!", "2024-01-12 12:14:00"),
            (28, 6, 12, "I want to go!!!", "2024-01-12 12:15:00"),
            (29, 7, 12, "I want to go!!", "2024-01-12 12:16:00"),
            (31, 9, 12, "I want to go!!", "2024-01-12 12:18:00"),
            (32, 10, 12, "I want to go!!!", "2024-01-12 12:19:00"),
            # Comments on Nicki's second post (post #13)
            (33, 1, 13, "Love it!", "2024-01-13 12:10:00"),
            (34, 2, 13, "I like the beat", "2024-01-13 12:20:00"),
            (35, 3, 13, "Very nice song", "2024-01-13 12:30:00"),
            (36, 4, 13, "Wow I cannot stop listening", "2024-01-13 12:40:00")
        ]


        cursor.executemany('''
                        INSERT INTO comments (comment_id, user_id, post_id, content, comment_date) VALUES (?, ?, ?, ?, ?)
                        ''', comments_data)

        # (post_id, user_id, view_time)
        views_data = [
            # John's views
            (1, 1, "2024-01-01 12:01:00"),
            (1, 2, "2024-01-01 12:00:01"),
            (1, 3, "2024-01-01 12:03:00"),
            (1, 4, "2024-01-01 12:00:01"),
            (1, 5, "2024-01-01 12:05:00"),
            (1, 6, "2024-01-01 12:00:01"),
            (1, 7, "2024-01-01 12:00:01"),
            (1, 8, "2024-01-01 12:00:01"),
            (1, 9, "2024-01-01 12:00:01"),
            (1, 10, "2024-01-01 12:00:01"),

            # Jane's views
            (2, 1, "2024-01-02 12:00:10"),
            (2, 2, "2024-01-02 12:02:00"),
            (2, 3, "2024-01-02 12:00:11"),
            (2, 4, "2024-01-02 12:04:00"),
            (2, 6, "2024-01-02 12:06:00"),

            # Mohammad's views
            (3, 1, "2024-01-03 12:01:00"),
            (3, 4, "2024-01-03 12:04:00"),
            (3, 7, "2024-01-03 12:07:00"),
            (3, 8, "2024-01-03 12:00:10"),
            (3, 9, "2024-01-03 12:00:11"),

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
            (9, 6, "2024-01-09 12:02:00"),
            (9, 7, "2024-01-09 12:07:00"),
            
            # John's second post views
            (11, 1, "2024-01-11 12:00:00"),
            (11, 2, "2024-01-11 12:00:20"),
            (11, 3, "2024-01-11 12:00:30"),
            (11, 4, "2024-01-11 12:00:40"),
            (11, 5, "2024-01-11 12:00:50"),
            (11, 6, "2024-01-11 12:00:51"),
            (11, 7, "2024-01-11 12:00:52"),
            
            # Elon's second post views
            (12, 1, "2024-01-12 12:00:01"),
            (12, 2, "2024-01-12 12:00:02"),
            (12, 3, "2024-01-12 12:00:03"),
            (12, 4, "2024-01-12 12:00:04"),
            (12, 5, "2024-01-12 12:00:05"),
            (12, 6, "2024-01-12 12:00:06"),
            (12, 7, "2024-01-12 12:00:07"),
            (12, 8, "2024-01-12 12:00:01"),
            (12, 9, "2024-01-12 12:00:09"),
            (12, 10, "2024-01-12 12:00:10"),
            
            # Nickie's second post views
            (13, 1, "2024-01-13 12:00:01"),
            (13, 2, "2024-01-13 12:00:02"),
            (13, 3, "2024-01-13 12:00:03"),
            (13, 4, "2024-01-13 12:00:04"),
            (13, 5, "2024-01-13 12:00:05"),
            (13, 6, "2024-01-13 12:00:06"),
            (13, 7, "2024-01-13 12:00:07"),
            (13, 8, "2024-01-13 12:00:08"),
            (13, 9, "2024-01-13 12:00:09"),
            (13, 10, "2024-01-13 12:00:01")
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

def get_users_data():
    users = []
    with connect_db() as cursor:
        cursor.execute('''
                    SELECT user_id, user_name, real_name, age, gender, job, location FROM users
                   ''')
        for row in cursor.fetchall():
            users.append({
                'user_id': row[0],
                'user_name': row[1],
                'real_name': row[2],
                'age': row[3],
                'gender': row[4],
                'job': row[5],
                'location': row[6]
            })
    return users

def get_connections_data():
    connections = []
    with connect_db() as cursor:
        cursor.execute('''
                    SELECT connection_id, user_id, target_user_id, connection_type FROM connections
                   ''')
        for row in cursor.fetchall():
            connections.append({
                'connection_id': row[0],
                'user_id': row[1],
                'target_user_id': row[2],
                'connection_Type': row[3]
            })
    return connections

def get_posts_data():
    posts = []
    with connect_db() as cursor:
        cursor.execute('''
                    SELECT post_id, user_id, content, post_date FROM posts
                   ''')
        for row in cursor.fetchall():
            posts.append({
                'post_id': row[0],
                'user_id': row[1],
                'content': row[2],
                'post_date': row[3]
            })
    return posts

def get_comments_data():
    comments = []
    with connect_db() as cursor:
        cursor.execute('''
                    SELECT comment_id, user_id, post_id, content, comment_date FROM comments
                   ''')
        for row in cursor.fetchall():
            comments.append({
                'comment_id': row[0],
                'user_id': row[1],
                'post_id': row[2],
                'content': row[3],
                'comment_date': row[4]
            })
    return comments

def get_views_data():
    views = []
    with connect_db() as cursor:
        cursor.execute('''
                    SELECT post_id, user_id, view_time FROM views
                   ''')
        for row in cursor.fetchall():
            views.append({
                'post_id': row[0],
                'user_id': row[1],
                'view_time': row[2]
            })
    return views
