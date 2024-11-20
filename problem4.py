from tools.database import create_db, reset_db, get_posts_data, get_views_data, get_users_data, get_comments_data
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# provides trending posts with the options of filtering
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
    
    if keyword_include:
        posts = [post for post in posts if keyword_include.lower() in post['content'].lower()]
        print(f"After include filter: {len(posts)} posts")

    if keyword_exclude:
        posts = [post for post in posts if keyword_exclude.lower() not in post['content'].lower()]
        print(f"After exclude filter: {len(posts)} posts")

    if user_filter:
        posts = [post for post in posts if user_filter(post)]
        print(f"After user filter: {len(posts)} posts")

    return posts, trend_report


def get_user_filter_option():
    users = get_users_data()
    genders = set(user['gender'] for user in users)
    ages = set(user['age'] for user in users)
    locations = set(user['location'] for user in users)

    print("\nFilter by user attribute:")
    print("0. No filter")
    print("1. Gender")
    print("2. Age")
    print("3. Location")
    filter_choice = int(input("Select an option: "))
    
    filter_function = None
    if filter_choice == 0:
        return None
    elif filter_choice == 1:
        print("\nAvailable genders:")
        for idx, gender in enumerate(genders, 1):
            print(f"{idx}. {gender}")
        gender_choice = int(input("Select gender: "))
        selected_gender = list(genders)[gender_choice - 1]
        filter_function = lambda post: next((user for user in users if user['user_id'] == post['user_id']), None)['gender'] == selected_gender
    elif filter_choice == 2:
        print("\nAvailable ages:")
        for idx, age in enumerate(ages, 1):
            print(f"{idx}. {age}")
        age_choice = int(input("Select age: "))
        selected_age = list(ages)[age_choice - 1]
        filter_function = lambda post: next((user for user in users if user['user_id'] == post['user_id']), None)['age'] == selected_age
    elif filter_choice == 3:
        print("\nAvailable locations:")
        for idx, location in enumerate(locations, 1):
            print(f"{idx}. {location}")
        location_choice = int(input("Select location: "))
        selected_location = list(locations)[location_choice - 1]
        filter_function = lambda post: next((user for user in users if user['user_id'] == post['user_id']), None)['location'] == selected_location

    return filter_function

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

def main():
    create_db()
    reset_db()

    posts = get_posts_data()

    print("\nDatabase initialized and reset.\n")

    print_posts_and_comments()

    print(f"There are {len(posts)} posts in the database.")

    # Ask for filters
    print("\nFilter options:")
    print("0. No filter")
    print("1. Include keyword")
    print("2. Exclude keyword")
    print("3. Filter by user attribute")

    filter_choice = int(input("Select filter option: "))

    keyword_include = None
    keyword_exclude = None
    user_filter = None

    if filter_choice == 0:
        pass
    elif filter_choice == 1:
        keyword_include = input("Enter keyword to include: ")
    elif filter_choice == 2:
        keyword_exclude = input("Enter keyword to exclude: ")
    elif filter_choice == 3:
        user_filter = get_user_filter_option()

    # Get trending posts and report
    trending_posts, trend_report = get_trending_posts(keyword_include, keyword_exclude, user_filter)

    # Print trending posts
    print("\nTrending Posts:")
    for post in trending_posts:
        print(f"Post ID: {post['post_id']}, Trend Score: {trend_report[post['post_id']]}")

    generate_word_cloud(trending_posts)

if __name__ == "__main__":
    main()
