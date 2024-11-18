from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Sample data structure
social_media_data = {
    "users": [
        {
            "posts": [
                {"content": "As a doctor, I am constantly inspired by the resilience of my patients. Each day brings new challenges, but also incredible opportunities to make a difference in someone's life."},
                {"content": "Teaching young minds is both a privilege and a responsibility. I love finding creative ways to make learning fun and impactful for my students."},
                {"content": "Loving my new Apple gadget!"},
                {"content": "Engineering has taught me to think critically and solve problems effectively. Today, I'm working on an innovative project that could positively impact millions."},
                {"content": "Nursing is not just a job—it's a calling. Helping patients recover and seeing their smiles reminds me why I chose this path."},
                {"content": "Life as a student is a whirlwind of exams, friendships, and endless possibilities. I'm excited about what the future holds!"},
                {"content": "Designing is my passion. I love creating visuals that not only look good but also tell a compelling story."},
                {"content": "Entrepreneurship is a journey of constant learning and adapting. I'm excited to share some new insights from my latest venture."},
                {"content": "Innovation is the driving force of progress. Today, I want to share some thoughts on sustainable energy solutions for a better tomorrow."},
                {"content": "Martial arts taught me discipline and perseverance. These lessons have shaped who I am both on and off the screen."},
                {"content": "Music is my sanctuary. Through every note and lyric, I strive to connect with people and share my story."},
            ]
        },
    ]
}

def extract_posts(data):
    """
    Extract all posts from the data.
    
    :param data: Dictionary with social media data.
    :return: List of all post content strings.
    """
    all_posts = []
    for user in data["users"]:
        for post in user["posts"]:
            all_posts.append(post["content"])
    return all_posts

def generate_wordcloud(posts):
    """
    Generate and display a word cloud from the list of post contents.
    
    :param posts: List of post content strings.
    """
    if not posts:
        print("No posts found!")
        return

    # Combine all posts into a single string
    text = " ".join(posts)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    
    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

# Example Usage
# Extract all posts (no filtering by keywords)
all_posts = extract_posts(social_media_data)

# Generate the word cloud
generate_wordcloud(all_posts)
