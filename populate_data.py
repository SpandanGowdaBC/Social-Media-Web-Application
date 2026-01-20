"""
Data Population Script for Social Media Application
This script creates realistic test data including users, posts, likes, comments, follows, and messages.
"""

import os
import django
import random
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialmedia.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile, Post, Like, Comment, Follow, Tag, Message

# Sample data
USERS_DATA = [
    {
        'username': 'sarah_tech',
        'email': 'sarah@example.com',
        'first_name': 'Sarah',
        'last_name': 'Johnson',
        'bio': '💻 Software Engineer | Tech Enthusiast | Coffee Lover ☕ | Building cool stuff with Python & Django',
    },
    {
        'username': 'mike_travels',
        'email': 'mike@example.com',
        'first_name': 'Mike',
        'last_name': 'Anderson',
        'bio': '🌍 Travel Blogger | Adventure Seeker | Photography 📸 | Exploring the world one city at a time',
    },
    {
        'username': 'emma_designs',
        'email': 'emma@example.com',
        'first_name': 'Emma',
        'last_name': 'Williams',
        'bio': '🎨 UI/UX Designer | Creative Mind | Design Thinking | Making the web beautiful',
    },
    {
        'username': 'alex_fitness',
        'email': 'alex@example.com',
        'first_name': 'Alex',
        'last_name': 'Martinez',
        'bio': '💪 Fitness Coach | Nutrition Expert | Wellness Advocate | Helping you achieve your fitness goals',
    },
    {
        'username': 'lisa_foodie',
        'email': 'lisa@example.com',
        'first_name': 'Lisa',
        'last_name': 'Chen',
        'bio': '🍕 Food Blogger | Recipe Creator | Culinary Explorer | Sharing delicious recipes and food adventures',
    },
]

POSTS_DATA = [
    {
        'author': 'sarah_tech',
        'content': 'Just deployed my first Django application! 🚀 The feeling of seeing your code live is incredible. #Django #WebDev #Python',
        'tags': ['Django', 'WebDev', 'Python'],
    },
    {
        'author': 'mike_travels',
        'content': 'Sunset in Santorini never gets old 🌅 One of the most beautiful places I\'ve ever visited. Highly recommend!',
        'tags': ['Travel', 'Santorini', 'Sunset'],
    },
    {
        'author': 'emma_designs',
        'content': 'Working on a new design system for our app. The key is consistency and simplicity! 🎨 #UIDesign #UX #DesignSystem',
        'tags': ['UIDesign', 'UX', 'DesignSystem'],
    },
    {
        'author': 'alex_fitness',
        'content': 'Remember: Progress, not perfection! 💪 Every workout counts, no matter how small. Keep pushing! #Fitness #Motivation',
        'tags': ['Fitness', 'Motivation'],
    },
    {
        'author': 'lisa_foodie',
        'content': 'Just made the most amazing homemade pasta! 🍝 Recipe coming soon on my blog. Who else loves Italian food?',
        'tags': ['Food', 'Cooking', 'Italian'],
    },
    {
        'author': 'sarah_tech',
        'content': 'Learning React hooks today. The useState and useEffect hooks are game changers! Any tips for a beginner? #React #JavaScript',
        'tags': ['React', 'JavaScript'],
    },
    {
        'author': 'mike_travels',
        'content': 'Pro travel tip: Always pack a portable charger! You never know when you\'ll need it. 🔋 #TravelTips',
        'tags': ['TravelTips'],
    },
    {
        'author': 'emma_designs',
        'content': 'Color psychology in design is fascinating! Did you know blue evokes trust and calmness? 🔵 #Design #ColorTheory',
        'tags': ['Design', 'ColorTheory'],
    },
    {
        'author': 'alex_fitness',
        'content': 'Meal prep Sunday! 🥗 Preparing healthy meals for the week ahead. Consistency is key to reaching your goals.',
        'tags': ['MealPrep', 'HealthyEating'],
    },
    {
        'author': 'lisa_foodie',
        'content': 'Trying out a new vegan chocolate cake recipe today! 🍰 Can\'t wait to share the results. #Vegan #Baking',
        'tags': ['Vegan', 'Baking'],
    },
    {
        'author': 'sarah_tech',
        'content': 'Debugging is like being a detective in a crime movie where you are also the murderer 😅 #ProgrammerHumor #Coding',
        'tags': ['ProgrammerHumor', 'Coding'],
    },
    {
        'author': 'mike_travels',
        'content': 'Just booked my next adventure to Tokyo! 🇯🇵 So excited to explore Japanese culture and cuisine. Any recommendations?',
        'tags': ['Tokyo', 'Japan', 'Travel'],
    },
    {
        'author': 'emma_designs',
        'content': 'Finished a 30-day UI challenge! Created 30 different interfaces. Growth comes from consistent practice! 🎯',
        'tags': ['UIChallenge', 'Design'],
    },
    {
        'author': 'alex_fitness',
        'content': 'Morning run complete! ✅ 5km in 28 minutes. Starting the day with energy and positivity. #Running #MorningRoutine',
        'tags': ['Running', 'MorningRoutine'],
    },
    {
        'author': 'lisa_foodie',
        'content': 'Found the cutest little café in downtown! ☕ Their cappuccino is to die for. Supporting local businesses! #Coffee #LocalBusiness',
        'tags': ['Coffee', 'LocalBusiness'],
    },
]

COMMENTS_DATA = [
    "This is amazing! Great work! 🎉",
    "Love this! Keep it up! 💯",
    "Absolutely beautiful! 😍",
    "Thanks for sharing! Very helpful! 🙏",
    "This is so inspiring! ✨",
    "Great content! Looking forward to more! 👏",
    "Wow, this is incredible! 🔥",
    "I needed to see this today! Thank you! ❤️",
    "Fantastic post! Very informative! 📚",
    "This resonates with me so much! 💭",
    "Amazing work! Keep inspiring! 🌟",
    "This is exactly what I was looking for! 🎯",
    "Love your perspective on this! 💡",
    "So true! Thanks for the reminder! ✅",
    "This made my day! 😊",
]

MESSAGES_DATA = [
    "Hey! How are you doing?",
    "Thanks for the follow! Love your content! 😊",
    "Would love to collaborate sometime!",
    "Great post! Really enjoyed reading it.",
    "Do you have any tips for beginners?",
    "Your work is so inspiring! Keep it up! 🌟",
    "I tried your recommendation and it worked perfectly!",
    "Looking forward to your next post!",
    "Thanks for the advice! It really helped! 🙏",
    "We should connect sometime!",
]


def clear_existing_data():
    """Clear existing test data (optional - be careful!)"""
    print("⚠️  Clearing existing data...")
    # Comment out if you want to keep existing data
    # Message.objects.all().delete()
    # Follow.objects.all().delete()
    # Comment.objects.all().delete()
    # Like.objects.all().delete()
    # Post.objects.all().delete()
    # Tag.objects.all().delete()
    # User.objects.exclude(is_superuser=True).delete()
    print("✓ Data cleared (skipped to preserve existing data)")


def create_users():
    """Create test users with profiles"""
    print("\n📝 Creating users...")
    users = []
    
    for user_data in USERS_DATA:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
            }
        )
        
        if created:
            user.set_password('password123')  # Default password for all test users
            user.save()
            print(f"  ✓ Created user: {user.username}")
        else:
            print(f"  → User already exists: {user.username}")
        
        # Update profile
        profile = user.profile
        profile.bio = user_data['bio']
        profile.save()
        
        users.append(user)
    
    return users


def create_follows(users):
    """Create follow relationships between users"""
    print("\n👥 Creating follow relationships...")
    
    follow_pairs = [
        ('sarah_tech', 'mike_travels'),
        ('sarah_tech', 'emma_designs'),
        ('sarah_tech', 'alex_fitness'),
        ('mike_travels', 'sarah_tech'),
        ('mike_travels', 'lisa_foodie'),
        ('emma_designs', 'sarah_tech'),
        ('emma_designs', 'lisa_foodie'),
        ('alex_fitness', 'sarah_tech'),
        ('alex_fitness', 'lisa_foodie'),
        ('lisa_foodie', 'mike_travels'),
        ('lisa_foodie', 'emma_designs'),
        ('lisa_foodie', 'alex_fitness'),
    ]
    
    for follower_username, following_username in follow_pairs:
        follower = User.objects.get(username=follower_username)
        following = User.objects.get(username=following_username)
        
        follow, created = Follow.objects.get_or_create(
            follower=follower,
            following=following
        )
        
        if created:
            print(f"  ✓ {follower_username} follows {following_username}")


def create_posts(users):
    """Create posts with tags"""
    print("\n📄 Creating posts...")
    posts = []
    
    for post_data in POSTS_DATA:
        author = User.objects.get(username=post_data['author'])
        
        # Create post with a timestamp in the past few days
        days_ago = random.randint(0, 7)
        hours_ago = random.randint(0, 23)
        created_time = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
        
        post = Post.objects.create(
            author=author,
            content=post_data['content'],
            created_at=created_time
        )
        
        # Add tags
        for tag_name in post_data.get('tags', []):
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)
            tag.usage_count += 1
            tag.save()
        
        posts.append(post)
        print(f"  ✓ Created post by {author.username}")
    
    return posts


def create_likes(users, posts):
    """Create likes on posts"""
    print("\n❤️  Creating likes...")
    
    for post in posts:
        # Each post gets 2-5 likes from random users (not the author)
        num_likes = random.randint(2, 5)
        potential_likers = [u for u in users if u != post.author]
        likers = random.sample(potential_likers, min(num_likes, len(potential_likers)))
        
        for user in likers:
            like, created = Like.objects.get_or_create(
                user=user,
                post=post
            )
            if created:
                print(f"  ✓ {user.username} liked post by {post.author.username}")


def create_comments(users, posts):
    """Create comments on posts"""
    print("\n💬 Creating comments...")
    
    for post in posts:
        # Each post gets 1-4 comments
        num_comments = random.randint(1, 4)
        
        for _ in range(num_comments):
            commenter = random.choice([u for u in users if u != post.author])
            comment_text = random.choice(COMMENTS_DATA)
            
            # Create comment with timestamp after post creation
            hours_after = random.randint(1, 48)
            comment_time = post.created_at + timedelta(hours=hours_after)
            
            comment = Comment.objects.create(
                user=commenter,
                post=post,
                content=comment_text,
                created_at=comment_time
            )
            print(f"  ✓ {commenter.username} commented on post by {post.author.username}")


def create_messages(users):
    """Create direct messages between users"""
    print("\n✉️  Creating messages...")
    
    # Create conversations between users who follow each other
    message_pairs = [
        ('sarah_tech', 'mike_travels'),
        ('sarah_tech', 'emma_designs'),
        ('mike_travels', 'lisa_foodie'),
        ('emma_designs', 'lisa_foodie'),
        ('alex_fitness', 'lisa_foodie'),
    ]
    
    for sender_username, receiver_username in message_pairs:
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)
        
        # Send 2-3 messages in each direction
        for _ in range(random.randint(2, 3)):
            message_text = random.choice(MESSAGES_DATA)
            days_ago = random.randint(0, 5)
            hours_ago = random.randint(0, 23)
            message_time = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
            
            Message.objects.create(
                sender=sender,
                receiver=receiver,
                content=message_text,
                created_at=message_time,
                is_read=random.choice([True, False])
            )
            print(f"  ✓ Message from {sender_username} to {receiver_username}")
        
        # Send some messages back
        for _ in range(random.randint(1, 2)):
            message_text = random.choice(MESSAGES_DATA)
            days_ago = random.randint(0, 5)
            hours_ago = random.randint(0, 23)
            message_time = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
            
            Message.objects.create(
                sender=receiver,
                receiver=sender,
                content=message_text,
                created_at=message_time,
                is_read=random.choice([True, False])
            )
            print(f"  ✓ Message from {receiver_username} to {sender_username}")


def main():
    """Main function to populate all data"""
    print("=" * 60)
    print("🚀 SOCIAL MEDIA APP - DATA POPULATION SCRIPT")
    print("=" * 60)
    
    # clear_existing_data()  # Uncomment to clear existing data
    
    users = create_users()
    create_follows(users)
    posts = create_posts(users)
    create_likes(users, posts)
    create_comments(users, posts)
    create_messages(users)
    
    print("\n" + "=" * 60)
    print("✅ DATA POPULATION COMPLETE!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"  • Users: {User.objects.count()}")
    print(f"  • Posts: {Post.objects.count()}")
    print(f"  • Likes: {Like.objects.count()}")
    print(f"  • Comments: {Comment.objects.count()}")
    print(f"  • Follows: {Follow.objects.count()}")
    print(f"  • Messages: {Message.objects.count()}")
    print(f"  • Tags: {Tag.objects.count()}")
    print(f"\n🔑 Test User Credentials:")
    print(f"  Username: Any of the created users (e.g., sarah_tech)")
    print(f"  Password: password123")
    print("\n")


if __name__ == '__main__':
    main()
