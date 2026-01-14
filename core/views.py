from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from datetime import datetime, timezone
from .models import UserProfile, Post, Like, Comment, Follow, Notification, Tag, Message
from .forms import UserRegistrationForm, UserProfileForm, PostForm, CommentForm


def signup(request):
    if request.user.is_authenticated:
        return redirect('feed')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('feed')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/signup.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = 'login'
    http_method_names = ['get', 'post']


@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_profile = profile_user.profile
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    
    # Check if current user follows this profile
    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()
    
    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'profile_user': profile_user,
        'user_profile': user_profile,
        'posts': page_obj,
        'is_following': is_following,
        'post_count': posts.count(),
    }
    
    return render(request, 'core/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'registration/profile_edit.html', {'form': form})


@login_required
def feed(request):
    # Get posts from users that the current user follows
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    posts = Post.objects.filter(
        Q(author__in=following_users) | Q(author=request.user)
    ).select_related('author', 'author__profile').prefetch_related(
        'post_likes', 'post_comments', 'tags'
    ).order_by('-created_at')
    
    # Get liked post IDs for the current user
    liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'liked_post_ids': liked_post_ids,
    }
    
    return render(request, 'core/feed.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            
            # Handle tags
            tags_input = form.cleaned_data.get('tags_input', '')
            if tags_input:
                tag_names = [tag.strip('#').strip() for tag in tags_input.split() if tag.strip().startswith('#')]
                for tag_name in tag_names:
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                        post.tags.add(tag)
                        tag.usage_count = tag.posts.count()
                        tag.save()
            
            messages.success(request, 'Post created successfully!')
            return redirect('feed')
    else:
        form = PostForm()
    
    return render(request, 'core/create_post.html', {'form': form})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related('author', 'author__profile').prefetch_related(
        'post_likes', 'post_comments__user', 'post_comments__user__profile', 'tags'
    ), pk=pk)
    
    # Check if user liked this post
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, post=post).exists()
    
    comments = post.post_comments.all()
    comment_form = CommentForm()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            
            # Create notification
            if post.author != request.user:
                Notification.objects.create(
                    user=post.author,
                    notification_type='comment',
                    post=post,
                    comment=comment
                )
            
            messages.success(request, 'Comment added!')
            return redirect('post_detail', pk=post.pk)
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': is_liked,
    }
    
    return render(request, 'core/post_detail.html', context)


@login_required
@require_POST
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()
        is_liked = False
    else:
        is_liked = True
        # Create notification
        if post.author != request.user:
            Notification.objects.create(
                user=post.author,
                notification_type='like',
                post=post
            )
    
    return JsonResponse({
        'is_liked': is_liked,
        'likes_count': post.post_likes.count()
    })


@login_required
@require_POST
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    
    if request.user == user_to_follow:
        return JsonResponse({'error': 'Cannot follow yourself'}, status=400)
    
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )
    
    if not created:
        follow.delete()
        is_following = False
    else:
        is_following = True
        # Create notification
        Notification.objects.create(
            user=user_to_follow,
            notification_type='follow',
            follower=request.user
        )
    
    return JsonResponse({
        'is_following': is_following,
        'followers_count': user_to_follow.profile.followers_count
    })


@login_required
def explore(request):
    # Get trending posts (most liked posts in last 7 days)
    from django.utils import timezone
    from datetime import timedelta
    
    week_ago = timezone.now() - timedelta(days=7)
    posts = Post.objects.filter(
        created_at__gte=week_ago
    ).annotate(
        like_count=Count('post_likes')
    ).order_by('-like_count', '-created_at')
    
    # Popular tags
    popular_tags = Tag.objects.order_by('-usage_count')[:20]
    
    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'popular_tags': popular_tags,
    }
    
    return render(request, 'core/explore.html', context)


@login_required
def view_notifications(request):
    notifications_queryset = Notification.objects.filter(
        user=request.user
    ).select_related('post', 'comment', 'follower').order_by('-created_at')
    
    # Mark as read
    if request.method == 'POST':
        notifications_queryset.update(is_read=True)
        return redirect('view_notifications')
    
    # Get unread count before slicing
    unread_count = notifications_queryset.filter(is_read=False).count()
    
    # Slice the queryset for display
    notifications_list = notifications_queryset[:50]
    
    context = {
        'notifications': notifications_list,
        'unread_count': unread_count,
    }
    
    return render(request, 'core/notifications.html', context)


@login_required
def tag_posts(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).select_related(
        'author', 'author__profile'
    ).prefetch_related('post_likes', 'tags').order_by('-created_at')
    
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'posts': page_obj,
    }
    
    return render(request, 'core/tag_posts.html', context)


@login_required
def followers_list(request, username):
    profile_user = get_object_or_404(User, username=username)
    followers = User.objects.filter(followers__following=profile_user).select_related('profile').order_by('username')
    
    # Check which of these users the current user follows
    following_ids = set(Follow.objects.filter(follower=request.user).values_list('following_id', flat=True))
    
    context = {
        'profile_user': profile_user,
        'users': followers,
        'following_ids': following_ids,
        'list_type': 'followers',
    }
    
    return render(request, 'core/follow_list.html', context)


@login_required
def following_list(request, username):
    profile_user = get_object_or_404(User, username=username)
    following = User.objects.filter(following__follower=profile_user).select_related('profile').order_by('username')
    
    # Check which of these users the current user follows
    following_ids = set(Follow.objects.filter(follower=request.user).values_list('following_id', flat=True))
    
    context = {
        'profile_user': profile_user,
        'users': following,
        'following_ids': following_ids,
        'list_type': 'following',
    }
    
    return render(request, 'core/follow_list.html', context)


@login_required
def chat_list(request):
    # Get all conversations (users you've messaged or who've messaged you)
    messages_sent = Message.objects.filter(sender=request.user).values_list('receiver', flat=True).distinct()
    messages_received = Message.objects.filter(receiver=request.user).values_list('sender', flat=True).distinct()
    all_conversations = set(list(messages_sent) + list(messages_received))
    
    # Get last message for each conversation
    conversations = []
    for user_id in all_conversations:
        other_user = User.objects.get(id=user_id)
        last_message = Message.objects.filter(
            Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
        ).order_by('-created_at').first()
        
        unread_count = Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).count()
        
        conversations.append({
            'user': other_user,
            'last_message': last_message,
            'unread_count': unread_count,
        })
    
    # Sort by last message time
    from datetime import datetime
    conversations.sort(key=lambda x: x['last_message'].created_at if x['last_message'] else datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    
    context = {
        'conversations': conversations,
    }
    
    return render(request, 'core/chat_list.html', context)


@login_required
def chat(request, username):
    other_user = get_object_or_404(User, username=username)
    
    # Only allow chat if users follow each other
    is_following = Follow.objects.filter(follower=request.user, following=other_user).exists()
    follows_me = Follow.objects.filter(follower=other_user, following=request.user).exists()
    
    if not (is_following or follows_me) and request.user != other_user:
        messages.error(request, 'You can only message users you follow.')
        return redirect('profile', username=username)
    
    # Get all messages between current user and other user
    messages_list = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
    ).select_related('sender', 'sender__profile', 'receiver', 'receiver__profile').order_by('created_at')
    
    # Mark messages as read
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    
    context = {
        'other_user': other_user,
        'messages': messages_list,
    }
    
    return render(request, 'core/chat.html', context)


@login_required
@require_POST
def send_message(request, username):
    receiver = get_object_or_404(User, username=username)
    content = request.POST.get('content', '').strip()
    
    if not content:
        return JsonResponse({'error': 'Message cannot be empty'}, status=400)
    
    # Only allow messaging if users follow each other
    is_following = Follow.objects.filter(follower=request.user, following=receiver).exists()
    follows_me = Follow.objects.filter(follower=receiver, following=request.user).exists()
    
    if not (is_following or follows_me) and request.user != receiver:
        return JsonResponse({'error': 'You can only message users you follow'}, status=403)
    
    message = Message.objects.create(
        sender=request.user,
        receiver=receiver,
        content=content
    )
    
    return JsonResponse({
        'success': True,
        'message_id': message.id,
        'content': message.content,
        'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'sender_username': message.sender.username,
    })


@login_required
def get_messages(request, username):
    other_user = get_object_or_404(User, username=username)
    last_message_id = request.GET.get('last_message_id', None)
    
    if last_message_id:
        try:
            last_message_id = int(last_message_id)
            messages_list = Message.objects.filter(
                Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user),
                id__gt=last_message_id
            ).select_related('sender', 'sender__profile').order_by('created_at')
        except (ValueError, TypeError):
            messages_list = Message.objects.none()
    else:
        messages_list = Message.objects.filter(
            Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
        ).select_related('sender', 'sender__profile').order_by('-created_at')[:50]
        messages_list = list(messages_list)
        messages_list.reverse()
    
    messages_data = []
    for msg in messages_list:
        messages_data.append({
            'id': msg.id,
            'content': msg.content,
            'sender_username': msg.sender.username,
            'is_sender': msg.sender == request.user,
            'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'time_display': msg.created_at.strftime('%I:%M %p'),
        })
    
    # Mark messages as read
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    
    return JsonResponse({'messages': messages_data})

