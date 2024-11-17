# ICS 311 Assignment 6
# Problem 1
# Author: Sujung Nam

from tools.database import create_db, reset_db, get_users_data, get_connections_data, get_posts_data, get_comments_data, get_views_data
from typing import Dict
from typing import List

class User:
  def __init__(self) -> None:
     pass

class Connection:
  def __init__(self) -> None:
     pass

class Post:
  def __init__(self) -> None:
     pass

class Comment:
  def __init__(self) -> None:
     pass

class View:
  def __init__(self) -> None:
     pass

class Graph:
  def __init__(self) -> None:
     pass

def solve_problem_1():
    print('Solving problem 1')
    try:
        # Initialize database
        create_db()
        reset_db()
        
        # Get graph data
        users_data = get_users_data()
        connections_data = get_connections_data()
        posts_data = get_posts_data()
        comments_data = get_comments_data()
        views_data = get_views_data()
        
        # Test
        print('Testing')
        print(len(users_data))
        print(len(connections_data))
        print(len(posts_data))
        print(len(comments_data))
        print(len(views_data))
    except (ValueError, IndexError):
        print("Invalid input. Please try again.")


if __name__ == '__main__':
  solve_problem_1()
