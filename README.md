# Real-Time Chat Application

A Django-based real-time chat application using WebSockets and Channels, featuring private messaging and online user tracking.

## Features

- Real-time private messaging
- Online user status tracking
- User authentication
- Responsive design
- Message history
- Room-based chat system

## Technology Stack

- Django 5.1.5
- Django Channels
- Redis
- WebSockets
- Bootstrap 4
- SQLite3

## Prerequisites

- Python 3.8+
- Redis Server
- Virtual Environment

## Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/chat-project.git
cd chat-project
```

2. Create and activate virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
```

5. Start Redis Server
```bash
# Linux/Mac
redis-server

# Windows
redis-server.exe
```

6. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create superuser (optional)
```bash
python manage.py createsuperuser
```

8. Collect static files
```bash
python manage.py collectstatic
```

9. Run the development server
```bash
python -m daphne -b 127.0.0.1 -p 8000 chat_project.asgi:application
```

## Project Structure

```
chat_project/
├── chat/                    # Main app directory
│   ├── static/             # Static files
│   │   ├── css/           # CSS files
│   │   └── js/            # JavaScript files
│   ├── templates/         # HTML templates
│   ├── consumers.py       # WebSocket consumers
│   ├── models.py          # Database models
│   ├── routing.py         # WebSocket routing
│   ├── urls.py            # URL patterns
│   └── views.py           # View functions
├── chat_project/          # Project settings
├── manage.py
├── requirements.txt
└── README.md
```

## Key Design Decisions

1. **Room-based Chat System**
   - Unique room names generated from sorted usernames
   - Rooms created automatically when users start chatting
   - Messages linked to rooms for better organization

2. **Online User Tracking**
   - Redis cache for storing online user status
   - Real-time updates using WebSocket connections
   - Automatic cleanup on disconnect

3. **Message Storage**
   - Persistent storage in SQLite database
   - Messages linked to both sender and receiver
   - Timestamp-based ordering

## Testing

   - Register two different users
   - Log in with different browsers/incognito windows
   - Start a chat between users
   - Check real-time message delivery
   - Verify online status updates
   - Test disconnection handling


## Common Issues

1. **WebSocket Connection Failed**
   - Ensure Redis server is running
   - Check ALLOWED_HOSTS in settings
   - Verify correct WebSocket URL

2. **Messages Not Appearing**
   - Check database migrations
   - Verify room creation
   - Check WebSocket connection status

3. **Static Files Not Loading**
   - Run collectstatic
   - Check STATIC_URL and STATIC_ROOT settings
   - Verify file paths

## Security Considerations

1. User Authentication
   - All chat routes require authentication
   - WebSocket connections verified
   - Session-based user tracking

2. Message Privacy
   - Messages visible only to participants
   - Room access restricted to members
   - User validation on connect

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django Channels documentation
- Bootstrap team
- Redis documentation
