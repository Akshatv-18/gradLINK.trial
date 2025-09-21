# GRADLINK - Alumni Networking Platform

A comprehensive Django-based alumni networking platform that connects graduates, students, universities, and companies for professional growth and networking.

## Features

### 🎓 Alumni Directory
- Searchable database of graduates
- Advanced filtering by university, graduation year, industry
- Professional profiles with skills and experience
- Connection requests and networking

### 💼 Job Board
- Job posting and application system
- Advanced search and filtering
- Company profiles and job categories
- Application tracking

### 📅 Events & Meetups
- Event creation and management
- Registration system with capacity limits
- Virtual and in-person events
- Event categories and filtering

### 💬 Community Feed
- Social media-style posts and updates
- Like and comment system
- Private messaging between users
- Content categorization with tags

### 🔐 Authentication & Profiles
- Custom user model with multiple user types
- Comprehensive profile management
- University affiliations
- Mentorship matching system

## Technology Stack

- **Backend**: Django 4.2.7, Python
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Django's built-in auth system
- **File Storage**: Local file system (configurable for cloud storage)

## Installation

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   \`\`\`bash
   git clone <repository-url>
   cd gradlink-django
   \`\`\`

2. **Create virtual environment**
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

3. **Install dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Database Setup**
   \`\`\`bash
   # Create MySQL database
   mysql -u root -p
   CREATE DATABASE gradlink_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   exit
   
   # Run the database creation script
   mysql -u root -p gradlink_db < scripts/create_database.sql
   \`\`\`

5. **Configure settings**
   - Update `gradlink/settings.py` with your database credentials
   - Set your `SECRET_KEY` for production
   - Configure email settings if needed

6. **Run migrations**
   \`\`\`bash
   python manage.py makemigrations
   python manage.py migrate
   \`\`\`

7. **Create superuser**
   \`\`\`bash
   python manage.py createsuperuser
   \`\`\`

8. **Load sample data (optional)**
   \`\`\`bash
   mysql -u root -p gradlink_db < scripts/seed_data.sql
   \`\`\`

9. **Collect static files**
   \`\`\`bash
   python manage.py collectstatic
   \`\`\`

10. **Run the development server**
    \`\`\`bash
    python manage.py runserver
    \`\`\`

Visit `http://localhost:8000` to access the application.

## Project Structure

\`\`\`
gradlink-django/
├── gradlink/                 # Main project directory
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── accounts/                # User authentication and profiles
├── alumni/                  # Alumni directory and networking
├── jobs/                    # Job board functionality
├── events/                  # Events and meetups
├── community/               # Community feed and messaging
├── core/                    # Core app with homepage and dashboard
├── templates/               # HTML templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploaded files
├── scripts/                 # Database scripts
└── requirements.txt         # Python dependencies
\`\`\`

## Key Models

### User & Profiles
- `User`: Extended Django user model with user types
- `UserProfile`: Detailed profile information
- `University`: University information

### Alumni Networking
- `Connection`: User connections and networking
- `MentorshipRequest`: Mentorship matching system
- `AlumniDirectory`: Public alumni listings

### Jobs
- `Job`: Job postings with detailed information
- `JobApplication`: Application tracking
- `JobCategory`: Job categorization

### Events
- `Event`: Event information and management
- `EventRegistration`: Event registration system
- `EventCategory`: Event categorization

### Community
- `Post`: Community posts and updates
- `Comment`: Post comments and replies
- `Message`: Private messaging system
- `PostLike`: Post engagement tracking

## Configuration

### Environment Variables
Create a `.env` file in the project root:

\`\`\`env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_NAME=gradlink_db
DATABASE_USER=your-db-user
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=localhost
DATABASE_PORT=3306
EMAIL_HOST=your-smtp-host
EMAIL_PORT=587
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-email-password
\`\`\`

### Production Deployment

1. Set `DEBUG = False` in settings
2. Configure proper database settings
3. Set up static file serving (nginx/Apache)
4. Configure email backend
5. Set up SSL certificates
6. Configure media file storage (AWS S3, etc.)

## API Endpoints

The application includes AJAX endpoints for:
- Like/unlike posts: `/community/like/<post_id>/`
- Connection requests: `/alumni/connect/<user_id>/`
- Event registration: `/events/<event_id>/register/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact the development team or create an issue in the repository.
