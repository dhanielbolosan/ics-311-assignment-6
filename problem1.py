# ICS 311 Assignment 6
# Problem 1
# Author: Sujung Nam

from tools.database import create_db, reset_db, get_users_data, get_connections_data, get_posts_data, get_comments_data, get_views_data
from typing import Dict
from typing import List

class User:
    def __init__(self, user_data) -> None:
        self.user_id = user_data.user_id
        self.user_name = user_data.user_name
        self.real_name = user_data.real_name
        self.age = user_data.age
        self.gender = user_data.gender
        self.job = user_data.job
        self.location = user_data.gender
    
    def get_user_id(self) -> int:
        return self.user_id
   
    def get_user_name(self) -> str:
        return self.user_name
   
    def get_real_name(self) -> str:
        return self.real_name
   
    def get_age(self) -> int:
        return self.age
   
    def get_gender(self) -> str:
        return self.gender
   
    def get_job(self) -> str:
        return self.job
   
    def get_location(self) -> str:
        return self.location
   

class Connection:
    def __init__(self, connection_data) -> None:
        self.connection_id = connection_data.connection_id
        self.user_id = connection_data.user_id
        self.target_user_id = connection_data.target_user_id
        self.connection_type = connection_data.connection_type
    
    def get_connection_id(self) -> int:
        return self.connection_id

    def get_user_id(self) -> int:
        return self.user_id

    def get_target_user_id(self) -> int:
        return self.target_user_id

    def get_connection_type(self) -> str:
        return self.connection_type


class Post:
    def __init__(self, post_data) -> None:
        self.post_id = post_data.post_id
        self.user_id = post_data.user_id
        self.content = post_data.content
        self.post_date = post_data.post_date
      
    def get_post_id(self) -> int:
        return self.post_id

    def get_user_id(self) -> int:
        return self.user_id

    def get_content(self) -> str:
        return self.content

    def get_post_date(self) -> str:
        return self.post_date


class Comment:
    def __init__(self, comment_data) -> None:
        self.comment_id = comment_data.comment_id
        self.user_id = comment_data.user_id
        self.post_id = comment_data.post_id
        self.content = comment_data.content
        self.comment_date = comment_data.comment_date

    def get_comment_id(self) -> int:
        return self.comment_id

    def get_user_id(self) -> int:
        return self.user_id

    def get_post_id(self) -> int:
        return self.post_id

    def get_content(self) -> str:
        return self.content

    def get_comment_date(self) -> str:
        return self.comment_date


class View:
    def __init__(self, view_data) -> None:
        self.post_id = view_data.post_id
        self.user_id = view_data.user_id
        self.view_time = view_data.view_time
    
    def get_post_id(self) -> int:
        return self.post_id

    def get_user_id(self) -> int:
        return self.user_id

    def get_view_time(self) -> str:
        return self.view_time


class SocialNetwork:
    def __init__(self) -> None:
        self.users = []
        self.connections = []
        self.posts = []
        self.comments = []
        self.views = []

    def get_user_id_to_user(self):
        return self.user_id_to_user

    def get_users(self):
        return self.users

    def get_connections(self):
        return self.connections

    def get_posts(self):
        return self.posts

    def get_comments(self):
        return self.comments

    def get_views(self):
        return self.views

    def add_users_data(self, users_data) -> None:
        for user_data in users_data:
            user = User(user_data)
            self.users.append(user)
    
    def add_connections_data(self, connections_data) -> None:
        for connection_data in connections_data:
            connection = Connection(connection_data)
            self.connections.append(connection)
    
    def add_posts_data(self, posts_data) -> None:
        for post_data in posts_data:
            post = Post(post_data)
            self.posts.append(post)
    
    def add_comments_data(self, comments_data) -> None:
        for comment_data in comments_data:
            comment = Comment(comment_data)
            self.comments.append(comment)
    
    def add_views_data(self, views_data) -> None:
        for view_data in views_data:
            view = View(view_data)
            self.views.append(view)

def solve_problem_1():
    print('Solving problem 1')
    try:
        # Initialize database
        create_db()
        reset_db()
        
        # Get social network data
        social_network = SocialNetwork()
        social_network.add_users_data(get_users_data())
        social_network.add_connections_data(get_connections_data())
        social_network.add_posts_data(get_posts_data())
        social_network.add_comments_data(get_comments_data())
        social_network.add_views_data(get_views_data())

        # Test
        print('Testing')
        # print(len(users_data))
        # print(len(connections_data))
        # print(len(posts_data))
        # print(len(comments_data))
        # print(len(views_data))
    except (ValueError, IndexError):
        print("Invalid input. Please try again.")

if __name__ == '__main__':
  solve_problem_1()
