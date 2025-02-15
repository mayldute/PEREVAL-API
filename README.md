This project implements a REST API for working with pass data. The API allows users to add, retrieve, update pass information, and interact with user data and images. The project uses FastAPI to create the API and SQLAlchemy with PostgreSQL to work with the database.

API Features

The API provides the following features:

- Adding a new pass.
- Retrieving a pass by ID.
- Updating pass data.
- Retrieving passes by user email.
- Working with pass images.

Technologies

- FastAPI – for creating the API.
- SQLAlchemy – for working with the database.
- PostgreSQL – for data storage.
- Pydantic – for data validation.
- Swagger – for auto-generating API documentation.

How to Deploy the Project

1. Install Dependencies
To install the dependencies, run the command:

```bash
pip install -r requirements.txt
```

2. Configure PostgreSQL
Before starting the project, configure the connection to PostgreSQL:

- Ensure you have PostgreSQL installed. If not, download and install it from the official site: PostgreSQL Downloads.
- Create a database for the project:
  ```sql
  CREATE DATABASE pereval_db;
  ```
- Ensure the project configuration file has the correct connection parameters:
  The project uses environment variables for database connection configuration. Ensure you have set up the environment variables for connecting to PostgreSQL:

  Create a `.env` file:
  ```env
  FSTR_DB_HOST = "host"
  FSTR_DB_PORT = "port"
  FSTR_DB_LOGIN = "login"
  FSTR_DB_PASS = "password"
  FSTR_DB_NAME = "database_name"
  ```

3. Start the Server
To start the server, use the command:

```bash
uvicorn main:app --reload
```

After that, the server will be available at `http://localhost:8000`.

Deployment Using Docker

1. Clone the Repository
First, clone the repository to your machine:

```bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```

2. Build the Docker Container
To build the Docker container with your application, run the following command in the project's root folder:

```bash
docker build -t pereval-api .
```

3. Run the Container
After building the container, run it using the following command:

```bash
docker run -d -p 8000:8000 pereval-api
```

This will create and run the container, which will be available at `http://localhost:8000`.

How to Use the API

1. Adding a New Pass
`POST /submitData`

Adds a new pass.

Example request:

```bash
curl -X 'POST' 'http://localhost:8000/submitData' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{
  "beauty_title": "pass",
  "title": "Phia",
  "other_titles": "Triev",
  "connect": "",
  "add_time": "2025-02-15T20:15:25.211Z",
  "user": {
    "email": "qwerty@mail.ru",
    "phone": "+7 555 55 55",
    "fam": "Pupkin",
    "name": "Vasily",
    "otc": "Ivanovich"
  },
  "coords": {
    "latitude": 45.3842,
    "longitude": 7.1525,
    "height": 1200
  },
  "winter_level": "",
  "summer_level": "1A",
  "autumn_level": "1A",
  "spring_level": "",
  "images": [{"img_title":"Saddle", "img":"<image1>"}, {"img_title":"Ascent", "img":"<image2>"}]
}'
```

Example response:

```json
{
  "status": 200,
  "message": "Pass successfully created",
  "id": 2
}
```

2. Retrieving a Pass by ID
`GET /submitData/{id}`

Returns information about the pass with the specified ID.

Example request:

```bash
curl -X 'GET' 'http://localhost:8000/submitData/1' -H 'accept: application/json'
```

Example response:

```json
{
  "beauty_title": "pass",
  "title": "Phia",
  "other_titles": "Triev",
  "connect": "",
  "add_time": "2025-02-15T20:15:25.211Z",
  "user": {
    "email": "qwerty@mail.ru",
    "phone": "+7 555 55 55",
    "fam": "Pupkin",
    "name": "Vasily",
    "otc": "Ivanovich",
    "id": 7
  },
  "coords": {
    "latitude": 45.3842,
    "longitude": 7.1525,
    "height": 1200,
    "id": 6
  },
  "winter_level": "",
  "summer_level": "1A",
  "autumn_level": "1A",
  "spring_level": "",
  "images": [],
  "id": 2,
  "status": "new"
}
```

3. Updating a Pass
`PATCH /submitData/{id}`

Updates the information about the pass with the specified ID if the pass status is "new".

Example request:

```bash
curl -X 'PATCH' 'http://localhost:8000/submitData/1' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{
  "title": "Updated Lenin Peak",
  "beauty_title": "Updated Title",
  "coords": {"latitude": 39.800, "longitude": 42.850, "height": 7200}
}'
```

Example response:

```json
{
  "state": 1,
  "message": "Pass successfully updated"
}
```

4. Retrieving Passes by User Email
`GET /submitData/`

Returns a list of passes for the user by their email.

Example request:

```bash
curl -X 'GET' 'http://localhost:8000/submitData/?user_email=user@example.com' -H 'accept: application/json'
```

Example response:

```json
[
  {
    "beauty_title": "pass",
    "title": "Phia",
    "other_titles": "Triev",
    "connect": "",
    "add_time": "2025-02-15T20:15:25.211Z",
    "user": {
      "email": "qwerty@mail.ru",
      "phone": "+7 555 55 55",
      "fam": "Pupkin",
      "name": "Vasily",
      "otc": "Ivanovich",
      "id": 7
    },
    "coords": {
      "latitude": 45.3842,
      "longitude": 7.1525,
      "height": 1200,
      "id": 6
    },
    "winter_level": "",
    "summer_level": "1A",
    "autumn_level": "1A",
    "spring_level": "",
    "images": [],
    "id": 2,
    "status": "new"
  }
]
```

Swagger Documentation

FastAPI automatically generates API documentation using Swagger. To view it, simply go to the following URL:

`http://localhost:8000/docs`

This page provides a visual interface for testing the API.

Test Coverage

The project includes unit tests to verify the functionality of database interaction methods and API testing. The tests include:

- Correctness of CRUD operations
- Proper error handling
- Testing all API endpoints
- Tests for creating users and coordinates, as well as adding pass images.

To run the tests, use the command:

```bash
pytest
```
