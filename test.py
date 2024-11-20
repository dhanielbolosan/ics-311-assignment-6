from tools.database import create_db, reset_db, get_posts_data, get_views_data, get_users_data, get_comments_data
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

def get_trending_posts(keyword_include=None, keyword_exclude=None, user_filter=None):
    posts = get_posts_data()
    views = get_views_data()
    comments = get_comments_data()

    # calculate report
    trend_report = {}
    for post in posts:
        post_id = post['post_id']

        # count number of views & comments for post
        post_views = len([v for v in views if v['post_id'] == post_id])
        post_comments = len([c for c in comments if c['post_id'] == post_id])

        # store in dictionary
        trend_report[post_id] = post_views + post_comments

    # post filtering
    filtered_posts = []
    for post in posts:
        content = post['content'].lower()
        user_id = post['user_id']

        if keyword_include and keyword_include.lower() not in content:
            continue
        if keyword_exclude and keyword_exclude.lower() in content:
            continue
        if user_filter:
            users = get_users_data()
            user = next((u for u in users if u['user_id'] == user_id), None)
            if not user or not all(user.get(k) == v for k, v in user_filter.items()):
                continue

        filtered_posts.append(post)

    filtered_posts.sort(key=lambda p: trend_report[p['post_id']], reverse=True)

    return filtered_posts, trend_report


def generate_word_cloud(posts):
    text = " ".join(post['content'] for post in posts)
    text = re.sub(r'\W+', ' ', text)

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def print_posts_and_comments():
    posts = get_posts_data()
    comments = get_comments_data()
    users = get_users_data()

    for post in posts:
        user_id = post['user_id']
        user = next((u for u in users if u['user_id'] == user_id), None)
        user_name = user['user_name'] if user else 'Unknown User'

        print(f"Post ID: {post['post_id']}, User: {user_name}, Content: {post['content']}, Date: {post['post_date']}")
        
        post_comments = [comment for comment in comments if comment['post_id'] == post['post_id']]
        
        if post_comments:
            print(f"  Comments:")
            for comment in post_comments:
                user_id = post['user_id']
                user = next((u for u in users if u['user_id'] == user_id), None)
                user_name = user['user_name'] if user else 'Unknown User'
                print(f"    Comment ID: {comment['comment_id']}, Use {user_name}, Content: {comment['content']}, Date: {comment['comment_date']}")
        else:
            print("  No comments.")
        
        print("\n" + "-"*50 + "\n")

def filter_posts(posts, keyword_include=None, keyword_exclude=None, user_filter=None):
    users = get_users_data()
    def apply_filters(post):
        content = post['content'].lower()

        # Keyword filters
        if keyword_include and keyword_include.lower() not in content:
            return False
        if keyword_exclude and keyword_exclude.lower() in content:
            return False

        # User filters (avoiding nested if by using dictionary lookup)
        if user_filter:
            user_id = post['user_id']
            user = next((u for u in users if u['user_id'] == user_id), None)
            if user:
                for key, value in user_filter.items():
                    if user.get(key) != value:
                        return False  # If any attribute doesn't match, exclude the post

        return True

    return [post for post in posts if apply_filters(post)]

def get_user_filter_input():
    """
    Gather and return user filter input as a dictionary.
    This avoids multiple if statements by using a dictionary to manage inputs.
    """
    user_filter = {}

    print("Enter filter criteria for users (leave blank to skip each option).")
    
    gender = input("Enter gender to filter by: ").strip()
    if gender:
        user_filter["gender"] = gender
    
    location = input("Enter location to filter by: ").strip()
    if location:
        user_filter["location"] = location

    age = input("Enter age to filter by: ").strip()
    if age:
        user_filter["age"] = age

    return user_filter


def main():
    create_db()
    reset_db()

    print("\nDatabase initialized and reset.\n")

    print_posts_and_comments()
    
    # Ask if the user wants to filter
    filter_option = input("Would you like to filter the posts? (yes/no): ").strip().lower()
    if filter_option != "yes":
        print("Skipping filters.\n")
        filtered_posts, attention_rates = get_trending_posts()
    else:
        # Ask if the user wants to include a word
        keyword_include = input("Enter a keyword to include in posts (or leave blank): ").strip() or None
        
        # Ask if the user wants to exclude a word
        keyword_exclude = input("Enter a keyword to exclude from posts (or leave blank): ").strip() or None
        
        # Get user filters (avoiding nested if-else by using a function)
        user_filter = get_user_filter_input()

        # Produce the trend report
        filtered_posts, attention_rates = get_trending_posts(
            keyword_include=keyword_include,
            keyword_exclude=keyword_exclude,
            user_filter=user_filter
        )

    # Display the results
    if filtered_posts:
        print("\nTrending Posts:")
        for post in filtered_posts:
            print(f"Post ID: {post['post_id']}, Attention Rate: {attention_rates[post['post_id']]:.2f}")
    else:
        print("\nNo posts match the criteria.")
    
    # Generate and display the word cloud for filtered posts
    generate_word_cloud(filtered_posts) 
    

if __name__ == '__main__':
    main()

'''
    # Example usage of get_trending_posts and generate_word_cloud
    print("\nFetching trending posts...")

    # Define filters (if any)
    keyword_include = input("Enter a keyword to include in posts (or leave blank): ").strip() or None
    keyword_exclude = input("Enter a keyword to exclude from posts (or leave blank): ").strip() or None
    user_filter = {}

    # Optional user filtering
    filter_by_user = input("Do you want to filter by user attributes? (yes/no): ").strip().lower()
    if filter_by_user == "yes":
        gender = input("Enter gender to filter by (or leave blank): ").strip()
        location = input("Enter location to filter by (or leave blank): ").strip()
        if gender:
            user_filter["gender"] = gender
        if location:
            user_filter["location"] = location

    # Fetch trending posts
    filtered_posts, attention_rates = get_trending_posts(
        keyword_include=keyword_include,
        keyword_exclude=keyword_exclude,
        user_filter=user_filter
    )

    # Display the results
    if filtered_posts:
        print("\nTrending Posts:")
        for post in filtered_posts:
            print(f"Post ID: {post['post_id']}, Attention Rate: {attention_rates[post['post_id']]:.2f}")
    else:
        print("\nNo posts match the criteria.")

    # Generate a word cloud
    generate_word_cloud(filtered_posts)
    '''