# 🌐 Social Media Platform

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Django](https://img.shields.io/badge/django-4.2%2B-green.svg)

A modern, full-featured social media application built with a robust Django backend and a sleek, responsive frontend.

---

## ✨ Features

### 👤 User Core
- **Advanced Profiles**: Customize your profile with pictures, bios, and personal info.
- **Secure Auth**: Full registration, login, and secure password management.
- **Follow System**: Build your network by following other users and managing your followers.

### 📝 Content & Interaction
- **Dynamic Posts**: Share text, images, and videos with your audience.
- **Micro-Interactions**: Like and comment on posts with real-time feedback.
- **Tagging**: Categorize content with hashtags for better discoverability.
- **Trending**: Stay updated with the most popular content on the platform.

### ✉️ Messaging
- **Direct Messaging**: A fully integrated chat system to communicate with your followers instantly.
- **Real-time Notifications**: Get alerted for new followers, likes, and comments.

---

## 📸 Screenshots

| Login Page | Main Feed |
| :---: | :---: |
| ![Login](./screenshots/login.png) | ![Feed](./screenshots/feed.png) |

| User Profile | Messaging |
| :---: | :---: |
| ![Profile](./screenshots/profile.png) | ![Messages](./screenshots/messages.png) |

---

## 🛠️ Tech Stack

- **Backend**: [Django](https://www.djangoproject.com/) (Python)
- **Database**: SQLite (Development)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Storage**: Pillow for image/video processing

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone <repository-url>
cd Social_Media_Apps
```

### 2. Setup Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations & Start Server
```bash
python manage.py migrate
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`

---

## 📁 Project Structure

```text
Social_Media_Apps/
├── core/                 # Main application logic (models, views, forms)
├── socialmedia/          # Project settings & configuration
├── templates/            # HTML templates organized by module
├── static/               # CSS, JS, and image assets
├── media/                # User-uploaded content (images, videos)
├── screenshots/          # Documentation assets
└── manage.py             # Django management CLI
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Developed with ❤️ by Spandan Gowda*
