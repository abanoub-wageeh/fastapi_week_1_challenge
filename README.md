# Notes API - Week 2 Project

An advanced RESTful API for managing notes, built with FastAPI and PostgreSQL. This project builds upon the Week 1 foundation by adding secure authentication, user management, and role-based access control.

## Features

### Core (Week 1)
- ✅ Create, Read, Update, Delete notes
- ✅ PostgreSQL database with SQLModel ORM
- ✅ Automatic API documentation (Swagger/ReDoc)
- ✅ Input validation with Pydantic
- ✅ Proper HTTP status codes

### New in Week 2
- ✅ **JWT Authentication**: Secure Signup/Login with Access & Refresh tokens
- ✅ **Email Verification**: User account verification via SMTP
- ✅ **User Ownership**: Users can only manage their own notes
- ✅ **Role-Based Access Control (RBAC)**: Admin role with full access
- ✅ **Password Hashing**: Secure password storage using argon2/bcrypt
- ✅ **Token Management**: Endpoints to refresh and revoke tokens

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLModel
- **Authentication:** PyJWT (JSON Web Tokens)
- **Security:** Pwdlib (Password Hashing)
- **Validation:** Pydantic

## Installation

1. Clone the repository
```bash
git clone https://github.com/abanoub-wageeh/fastapi_week_1_challenge
cd fastapi_week_1_challenge
```

2. Create virtual environment
```bash
python -m venv env
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=15
APP_PASSWORD=your_email_app_password
```

5. Run the server
```bash
uvicorn main:app --reload
```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/sign_up` | Register a new user |
| POST | `/login` | Login to get access/refresh tokens |
| POST | `/refresh` | Refresh access token |
| PUT | `/revoke` | Revoke refresh token (Logout) |
| GET | `/verify_account` | Verify email address |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/myprofile` | Get current user details |
| PUT | `/user` | Update current user |
| DELETE | `/user` | Delete current user |
| GET | `/users` | Get all users |

### Notes (Protected)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notes` | Get current user's notes |
| POST | `/notes` | Create a new note |
| GET | `/notes/{id}` | Get specific note |
| PUT | `/notes/{id}` | Update specific note |
| DELETE | `/notes/{id}` | Delete specific note |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/notes` | Get all notes (Admin only) |
| POST | `/admin/notes` | Create note (Admin only) |
| PUT | `/admin/notes/{id}` | Update any note |
| DELETE | `/admin/notes/{id}` | Delete any note |

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs

## Project Structure

```
notes-api/
├── main.py           # FastAPI app initialization
├── database.py       # Database connection
├── models.py         # Database models (User, Note)
├── schemas.py        # Pydantic schemas (renamed from shemas.py)
├── oauth2.py         # Auth logic and dependencies
├── utils.py          # Utility functions (hashing, email)
├── routes/
│   ├── notes.py      # Note routes
│   ├── auth.py       # Authentication routes
│   ├── users.py      # User management routes
│   └── admin.py      # Admin routes
└── requirements.txt  # Python dependencies
```

## What I Learned (Week 2)

- **Authentication Flow**: Implementing JWT access and refresh tokens from scratch.
- **Security**: Hashing passwords and verifying emails before allowing access.
- **Authorization**: Using `Depends` to inject current user and verify roles/ownership.
- **Database Relationships**: Linking `Users` and `Notes` with Foreign Keys in SQLModel.
- **Code Organization**: Splitting routes, models, and schemas for better maintainability.