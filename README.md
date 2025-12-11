# Notes API - Week 1 Project

A simple CRUD API for managing notes, built with FastAPI and PostgreSQL.

## Features

- ✅ Create, Read, Update, Delete notes
- ✅ PostgreSQL database with SQLModel ORM
- ✅ Automatic API documentation (Swagger/ReDoc)
- ✅ Input validation with Pydantic
- ✅ Proper HTTP status codes

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLModel
- **Validation:** Pydantic

## Installation

1. Clone the repository
```bash
git clone https://github.com/abanoub-wageeh/fastapi_week_1_challenge
cd fastapi_week_1_challenge
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up database
- Create a PostgreSQL database
- Update `DATABASE_URL` in `database.py`

5. Run the server
```bash
uvicorn main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notes` | Get all notes |
| GET | `/notes/{id}` | Get note by ID |
| POST | `/notes` | Create new note |
| PUT | `/notes/{id}` | Update note |
| DELETE | `/notes/{id}` | Delete note |

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs

## Example Usage

### Create a note
```bash
POST /notes
{
  "title": "My First Note",
  "content": "This is the content"
}
```

### Update a note
```bash
PUT /notes/1
{
  "title": "Updated Title"
}
```

## Project Structure

```
notes-api/
├── main.py           # FastAPI app initialization
├── database.py       # Database models and connection
├── shemas.py         # Pydantic schemas for validation
├── routes/
│   └── notes.py      # Note endpoints
└── requirements.txt  # Python dependencies
```

## What I Learned

- FastAPI basics (routing, dependency injection, validation)
- SQLModel for type-safe database operations
- Separating database models from API schemas
- RESTful API design principles
- HTTP status codes and error handling

## Next Steps

- Add user authentication with JWT
- Implement role-based access control
- Add user ownership to notes
