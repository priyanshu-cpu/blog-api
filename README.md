# FastAPI Blog API

A simple blog backend built with **FastAPI** and **SQLAlchemy**, featuring JWT-based user authentication and full CRUD operations on blog posts.

## Features

- User registration and login with hashed passwords (`pwdlib`)
- JWT authentication (`python-jose`) via a custom `Header`-based token check
- Create, read, update, and delete blog posts
- Ownership checks — users can only edit/delete their own posts
- SQLAlchemy ORM models with a one-to-many relationship (`Users` → `BlogData`)
- Pydantic schemas for request validation and response formatting

## Project Structure

```
.
├── main.py       # FastAPI app, routes, auth dependency
├── models.py     # SQLAlchemy ORM models (Users, BlogData)
├── schemas.py    # Pydantic request/response schemas
├── database.py   # DB engine, session, and Base setup
├── helper.py     # JWT token creation
└── .env          # Environment variables (not committed)
```

## Requirements

- Python 3.10+
- A SQL database reachable via a SQLAlchemy connection string (e.g. PostgreSQL, MySQL, SQLite)

### Dependencies

```
fastapi
uvicorn
sqlalchemy
python-dotenv
python-jose
pwdlib
pydantic[email]
```

Install them with:

```bash
pip install fastapi uvicorn sqlalchemy python-dotenv python-jose pwdlib "pydantic[email]"
```

> Note: depending on your database, you'll also need a driver (e.g. `psycopg2-binary` for PostgreSQL).

## Environment Variables

Create a `.env` file in the project root with the following:

```env
DB_URL=your_database_connection_string
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Running the App

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

## API Endpoints

| Method | Endpoint              | Auth Required | Description                          |
|--------|------------------------|:--------------:|--------------------------------------|
| GET    | `/`                    | No             | Health check / home route            |
| POST   | `/register`            | No             | Register a new user                  |
| POST   | `/login`               | No             | Log in and receive a JWT token       |
| POST   | `/create-blog`         | Yes            | Create a new blog post               |
| GET    | `/blogs`               | Yes            | List all blog posts                  |
| GET    | `/blogs/{blog_id}`     | Yes            | Get a single blog post by ID         |
| PUT    | `/update-blog/{blog_id}` | Yes          | Update a blog post (owner only)      |
| DELETE | `/blogs/{blog_id}`     | Yes            | Delete a blog post (owner only)      |

### Authentication

Protected routes expect the JWT token in a `token` header (not `Authorization: Bearer`):

```
token: <your_jwt_token>
```

## Known Issues / Suggested Improvements

A few things worth addressing before using this in production:

- **Bare `except` in `verify_token`**: catches all exceptions silently, which can mask real bugs. Consider catching `jwt.JWTError` specifically.
- **Token passed via custom header**: consider switching to the standard `Authorization: Bearer <token>` scheme with FastAPI's `OAuth2PasswordBearer` for better client/tool compatibility.
- **`/login` returns a raw token string**: consider wrapping it in a JSON object, e.g. `{"access_token": token, "token_type": "bearer"}`.
- **`UserOut.email` is typed as required `str`**, but `Users.email` in the model is nullable — these should be reconciled.
- **No password complexity or input length validation** on registration.
- **`jwt.encode` argument order**: verify against your `python-jose` version, as positional args for algorithm can be error-prone — consider using keyword arguments.

## License

Add your license of choice here.
