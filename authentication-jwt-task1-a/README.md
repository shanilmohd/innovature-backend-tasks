
# Authentication System using Flask

A user authentication system using JWT. API is developed using flask

## Authentication

Some endpoints require authentication. You need to include a valid JWT token in the `Authorization` header of your request.

## Endpoints


### Get All Users

- **URL:** `/getuser`
- **Method:** `GET`
- **Description:** Get a list of all users.
- **Authentication Required:** Yes

### Token refresh

- **URL:** `/refresh`
- **Method:** `POST`
- **Description:** Token refresh.
- **Authentication Required:** Yes

### Login

- **URL:** `/login`
- **Method:** `POST`
- **Description:** login.
- **Authentication Required:** No

### Sign up

- **URL:** `/signup`
- **Method:** `POST`
- **Description:** Register new user.
- **Authentication Required:** No

#
