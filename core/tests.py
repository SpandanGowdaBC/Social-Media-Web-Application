from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import UserProfile, Post, Like, Comment, Follow, Notification, Tag, Message


class SocialMediaTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password123')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password123')

    def test_01_user_signup_and_profile_creation(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password123!',
            'password2': 'password123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        newuser = User.objects.get(username='newuser')
        self.assertTrue(hasattr(newuser, 'profile'))

    def test_02_edit_profile(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('edit_profile'), {
            'bio': 'Software Engineer & Tech Enthusiast'
        })
        self.assertEqual(response.status_code, 302)
        self.user1.profile.refresh_from_db()
        self.assertEqual(self.user1.profile.bio, 'Software Engineer & Tech Enthusiast')

    def test_03_create_post(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('create_post'), {
            'content': 'Hello world! #tech #django',
            'tags_input': '#tech #django'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.content, 'Hello world! #tech #django')

    def test_04_feed_view(self):
        self.client.login(username='user1', password='password123')
        Follow.objects.create(follower=self.user1, following=self.user2)
        Post.objects.create(author=self.user2, content='Post from followed user')
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post from followed user')

    def test_05_like_post_toggle(self):
        self.client.login(username='user1', password='password123')
        post = Post.objects.create(author=self.user2, content='Awesome post')
        # Like
        response = self.client.post(reverse('like_post', args=[post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['is_liked'])
        post.refresh_from_db()
        self.assertEqual(post.likes_count, 1)

    def test_06_comment_on_post(self):
        self.client.login(username='user1', password='password123')
        post = Post.objects.create(author=self.user2, content='Post needing comments')
        response = self.client.post(reverse('post_detail', args=[post.id]), {
            'content': 'Great post!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.filter(post=post).count(), 1)

    def test_07_follow_unfollow_user(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('follow_user', args=[self.user2.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['is_following'])
        self.assertTrue(Follow.objects.filter(follower=self.user1, following=self.user2).exists())

    def test_08_notifications_generation(self):
        self.client.login(username='user1', password='password123')
        post = Post.objects.create(author=self.user2, content='Post to like')
        self.client.post(reverse('like_post', args=[post.id]))
        self.assertTrue(Notification.objects.filter(user=self.user2, notification_type='like').exists())

    def test_09_direct_messaging_send_and_get(self):
        Follow.objects.create(follower=self.user1, following=self.user2)
        Follow.objects.create(follower=self.user2, following=self.user1)
        self.client.login(username='user1', password='password123')
        # Send message
        response_send = self.client.post(reverse('send_message', args=[self.user2.username]), {
            'content': 'Hey user2!'
        })
        self.assertEqual(response_send.status_code, 200)
        self.assertTrue(response_send.json()['success'])

        # Get messages
        response_get = self.client.get(reverse('get_messages', args=[self.user2.username]))
        self.assertEqual(response_get.status_code, 200)
        messages = response_get.json()['messages']
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['content'], 'Hey user2!')

    def test_10_explore_page_and_tags(self):
        tag = Tag.objects.create(name='python', slug='python')
        post = Post.objects.create(author=self.user1, content='Python rocks!')
        post.tags.add(tag)
        self.client.login(username='user2', password='password123')
        response_explore = self.client.get(reverse('explore'))
        self.assertEqual(response_explore.status_code, 200)
        response_tag = self.client.get(reverse('tag_posts', args=['python']))
        self.assertEqual(response_tag.status_code, 200)
        self.assertContains(response_tag, 'Python rocks!')
