# Social Media Platform

A full-featured social media application built with Django (Python) backend and HTML/CSS/JavaScript frontend.

## Features

### Core Features
- ✅ User Profiles - Create, view, and edit user profiles with profile pictures and bios
- ✅ Share Posts - Create posts with text, images, and videos
- ✅ Like Posts - Like and unlike posts with real-time updates
- ✅ Comment on Posts - Add comments to posts
- ✅ Image/Video Uploads - Upload images and videos for posts
- ✅ Post Tagging - Tag posts with hashtags

### Optional Features
- ✅ Follow System - Follow and unfollow users, view followers/following lists
- ✅ Notifications - Real-time notifications for likes, comments, and follows
- ✅ Trending Content - Explore page with trending posts and popular tags
- ✅ Messaging - Dynamic chat system to message followers

## Technology Stack

- **Backend**: Django 6.0.1 (Python)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Design**: Modern responsive design with Instagram-style interface

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Social_Media_Apps
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application at `http://127.0.0.1:8000/`

## Project Structure

```
Social_Media_Apps/
├── core/                 # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── forms.py         # Django forms
│   ├── urls.py          # URL routing
│   └── admin.py         # Admin configuration
├── templates/            # HTML templates
│   ├── base.html
│   ├── core/           # Core app templates
│   └── registration/   # Auth templates
├── static/              # Static files
│   ├── css/            # Stylesheets
│   └── js/             # JavaScript files
├── media/               # User uploaded files
├── socialmedia/        # Django project settings
└── manage.py           # Django management script
```

## Features Overview

### User Authentication
- User registration and login
- Profile creation and editing
- Secure password handling

### Social Features
- Follow/unfollow users
- View followers and following lists
- Real-time notifications
- Direct messaging with followers

### Content Management
- Create posts with text, images, or videos
- Tag posts with hashtags
- Like and comment on posts
- View trending content

### User Interface
- Modern, responsive design
- Smooth animations and transitions
- Mobile-friendly layout
- Instagram-style interface

## Usage

1. **Sign Up**: Create a new account
2. **Create Profile**: Add profile picture and bio
3. **Follow Users**: Follow other users to see their posts
4. **Create Posts**: Share text, images, or videos
5. **Interact**: Like and comment on posts
6. **Explore**: Discover trending content
7. **Message**: Chat with users you follow

## Development

This project uses Django's built-in development server. For production deployment, configure:
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Set up proper database (PostgreSQL recommended)
- Configure static file serving
- Set up media file storage (AWS S3 recommended)

## License

This project is developed for educational purposes.
