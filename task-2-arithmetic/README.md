
# An API for arithmetic operations

An API for arithmetic operations using flask

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

### Subtraction

- **URL:** `/subtract`
- **Method:** `GET`
- **Description:** Takes 2 params(x,y) as input and returns x-y as result.
- **Authentication Required:** Yes

### Addition

- **URL:** `/add`
- **Method:** `GET`
- **Description:** Takes 2 params(x,y) as input and returns x+y as result.
- **Authentication Required:** Yes

### Multiplication

- **URL:** `/multiply`
- **Method:** `GET`
- **Description:** Takes 2 params(x,y) as input and returns xy as result.
- **Authentication Required:** Yes

### Division

- **URL:** `/divide`
- **Method:** `GET`
- **Description:** Takes 2 params(x,y) as input and returns x/y as result.
- **Authentication Required:** Yes




#
