from tools.database import create_db, reset_db, get_posts_data, get_views_data, get_users_data, get_comments_data
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# provides trending posts with the options of filtering
def get_trending_posts(include_keyword=None, exclude_keyword=None, user_filter=None):
    # get needed data
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
        trend_report[post_id] = 0.5*(post_views) + post_comments
    
    # modify trend report if include filter is applied
    if include_keyword:
        posts = [p for p in posts if include_keyword.lower() in p['content'].lower()]
        print(f"\nAfter include filter: {len(posts)} posts")

    # modify trend report if exclude filter is applied
    if exclude_keyword:
        posts = [p for p in posts if exclude_keyword.lower() not in p['content'].lower()]
        print(f"\nAfter exclude filter: {len(posts)} posts")

    # modify trend report if user filter is applied
    if user_filter:
        posts = [p for p in posts if user_filter(p)]
        print(f"\nAfter user filter: {len(posts)} posts")

    return posts, trend_report


# helper function to get user filter option
def filter_options():
    # get needed data
    users = get_users_data()
    genders = set(user['gender'] for user in users)
    ages = set(user['age'] for user in users)
    locations = set(user['location'] for user in users)

    # choices for user filter
    print("\nFilter by user attribute:")
    print("0. No filter")
    print("1. Gender")
    print("2. Age")
    print("3. Location")
    filter_choice = int(input("Select an option: "))
    
    # apply filter based on user choice
    filter_function = None

    # no filter
    if filter_choice == 0:
        return None
    
    # filter by gender
    elif filter_choice == 1:
        # print available genders and get user choice
        print("\nAvailable genders:")
        for index, gender in enumerate(genders, 1):
            print(f"{index}. {gender}")
        gender_choice = int(input("Select gender: "))
        selected_gender = list(genders)[gender_choice - 1]

        # apply gender filter
        filter_function = lambda post: next((u for u in users if u['user_id'] == post['user_id']), None)['gender'] == selected_gender

    # filter by age
    elif filter_choice == 2:
        # print available ages and get user choice for min and max age
        print("\nAvailable ages:")
        for index, age in enumerate(ages, 1):
            print(f"{index}. {age}")
        min_age = int(input("\nEnter minimum age: "))
        max_age = int(input("Enter maximum age: "))

        # apply age filter
        filter_function = lambda post: min_age <= next((u for u in users if u['user_id'] == post['user_id']), None)['age'] <= max_age

    # filter by location
    elif filter_choice == 3:
        # print available locations and get user choice
        print("\nAvailable locations:")
        for index, location in enumerate(locations, 1):
            print(f"{index}. {location}")
        location_choice = int(input("Select location: "))
        selected_location = list(locations)[location_choice - 1]

        # apply location filter
        filter_function = lambda post: next((u for u in users if u['user_id'] == post['user_id']), None)['location'] == selected_location

    return filter_function

# prints posts and their comments
def print_posts_and_comments():
    posts = get_posts_data()
    comments = get_comments_data()
    users = get_users_data()

    for post in posts:
        # get user info from database
        user_id = post['user_id']
        user = next((u for u in users if u['user_id'] == user_id), None)
        user_name = user['user_name'] if user else 'Unknown User'
        age = user['age'] if user else 'Unknown Age'

        print(f"Post ID: {post['post_id']}, User: {user_name}, Age: {age}, Date: {post['post_date']} \nContent: {post['content']}")
        
        post_comments = [comment for comment in comments if comment['post_id'] == post['post_id']]
        
        if post_comments:
            print(f"  Comments:")
            for comment in post_comments:
                user_id = post['user_id']
                user = next((u for u in users if u['user_id'] == user_id), None)
                user_name = user['user_name'] if user else 'Unknown User'
                print(f"    Comment ID: {comment['comment_id']}, Use {user_name}, Date: {comment['comment_date']} \n    Content: {comment['content']}")
        else:
            print("  No comments.")
        
        print("\n" + "-"*50 + "\n")

# https://www.geeksforgeeks.org/generating-word-cloud-python/
# makes a word cloud using the post content as text
def generate_word_cloud(posts):
    text = " ".join(post['content'] for post in posts)
    text = re.sub(r'\W+', ' ', text)

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

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

    include_keyword = None
    exclude_keyword = None
    user_filter = None

    if filter_choice == 0:
        pass
    elif filter_choice == 1:
        include_keyword = input("Enter keyword to include: ")
    elif filter_choice == 2:
        exclude_keyword = input("Enter keyword to exclude: ")
    elif filter_choice == 3:
        user_filter = filter_options()

    # Get trending posts and report
    trending_posts, trend_report = get_trending_posts(include_keyword, exclude_keyword, user_filter)

    # Print trending posts
    print("\nTrending Posts:")
    for post in trending_posts:
        print(f"Post ID: {post['post_id']}, Trend Score: {trend_report[post['post_id']]}")

    generate_word_cloud(trending_posts)

if __name__ == "__main__":
    main()
