// Main JavaScript for Social Media Platform

document.addEventListener('DOMContentLoaded', function() {
    // Like functionality
    const likeButtons = document.querySelectorAll('.like-btn');
    likeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const postId = this.getAttribute('data-post-id');
            likePost(postId, this);
        });
    });
    
    // Follow functionality
    const followButtons = document.querySelectorAll('.follow-btn');
    followButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const username = this.getAttribute('data-username');
            followUser(username, this);
        });
    });
    
    // Auto-hide messages
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
    
    // Follow buttons in lists
    const followButtonsList = document.querySelectorAll('.follow-btn-list');
    followButtonsList.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const username = this.getAttribute('data-username');
            followUser(username, this);
        });
    });
});

// Like/Unlike Post
function likePost(postId, buttonElement) {
    const url = `/post/${postId}/like/`;
    const csrftoken = getCookie('csrftoken');
    
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error(data.error);
            return;
        }
        
        // Update button state
        if (data.is_liked) {
            buttonElement.classList.add('liked');
            if (buttonElement.querySelector('svg')) {
                buttonElement.querySelector('svg').setAttribute('fill', '#ed4956');
                buttonElement.querySelector('svg').setAttribute('stroke', '#ed4956');
            }
        } else {
            buttonElement.classList.remove('liked');
            if (buttonElement.querySelector('svg')) {
                buttonElement.querySelector('svg').setAttribute('fill', 'none');
                buttonElement.querySelector('svg').setAttribute('stroke', 'currentColor');
            }
        }
        
        // Update likes count
        const likesCountElement = document.querySelector(`.likes-count[data-post-id="${postId}"]`);
        if (likesCountElement) {
            likesCountElement.textContent = data.likes_count;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Follow/Unfollow User
function followUser(username, buttonElement) {
    const url = `/follow/${username}/`;
    const csrftoken = getCookie('csrftoken');
    
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error(data.error);
            return;
        }
        
        // Update button text
        if (data.is_following) {
            buttonElement.textContent = 'Unfollow';
            buttonElement.classList.add('btn-outline');
            buttonElement.classList.remove('btn-primary');
        } else {
            buttonElement.textContent = 'Follow';
            buttonElement.classList.add('btn-primary');
            buttonElement.classList.remove('btn-outline');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Get CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
