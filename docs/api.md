# Library API Specification

This document details the REST endpoints available for managing books, authors, book-author relationships, users, and authentication in the library system.

---

## Books Management

### Create Book
Add a new book record to the system catalog.

* **Endpoint**: `POST /books/new-book`
* **Python Controller**: `create_book`
* **Input Schema**: `BookCreate`
* **Fields**:
  * `isbn` (string, exactly 13 digits)
  * `title` (string, max 255 chars)
  * `genre` (string, max 255 chars)
  * `publish_date` (date, optional)
  * `book_id` (integer, optional)

### List Books
Retrieve a list of all book records registered in the system.

* **Endpoint**: `GET /books/`
* **Python Controller**: `list_books`

### Get Book Detail
Retrieve a specific book record by its unique ID.

* **Endpoint**: `GET /books/{book_id}`
* **Python Controller**: `get_book`

### Update Book
Update details of an existing book record.

* **Endpoint**: `PUT /books/{book_id}`
* **Python Controller**: `update_book`
* **Input Schema**: `BookUpdate`
* **Fields**:
  * `isbn` (string, exactly 13 digits)
  * `title` (string, max 255 chars)
  * `genre` (string, max 255 chars)
  * `publish_date` (date, optional)

### Delete Book
Delete a book record from the system.

* **Endpoint**: `DELETE /books/{book_id}`
* **Python Controller**: `delete_book`

---

## Authors Management

### Create Author
Add a new author record to the system.

* **Endpoint**: `POST /author/`
* **Python Controller**: `create_author`
* **Input Schema**: `AuthorCreate`
* **Fields**:
  * `first_name` (string, max 50 chars)
  * `last_name` (string, max 50 chars)
  * `author_id` (integer, optional)

### List Authors
Retrieve a list of all author records.

* **Endpoint**: `GET /author/`
* **Python Controller**: `list_authors`

### Get Author Detail
Retrieve a specific author record by ID.

* **Endpoint**: `GET /author/{author_id}`
* **Python Controller**: `get_author`

### Update Author
Update details of an existing author.

* **Endpoint**: `PUT /author/{author_id}`
* **Python Controller**: `update_author`
* **Input Schema**: `AuthorUpdate`
* **Fields**:
  * `first_name` (string, max 50 chars)
  * `last_name` (string, max 50 chars)

### Delete Author
Delete an author record by ID.

* **Endpoint**: `DELETE /author/{author_id}`
* **Python Controller**: `delete_author`

---

## Book Authors Management

### Assign Author to Book
Link an author to a book with an optional specified role.

* **Endpoint**: `POST /book-authors/`
* **Python Controller**: `assign_author_to_book`
* **Input Schema**: `BookAuthorCreate`
* **Fields**:
  * `book_id` (integer)
  * `author_id` (integer)
  * `role` (string, optional, max 50 chars)

### List Book Authors
Retrieve all book-author relationships, optionally filtered by `book_id` or `author_id`.

* **Endpoint**: `GET /book-authors/`
* **Python Controller**: `list_book_authors`

### Get Book Author Relationship
Retrieve a specific book-author relationship by composite keys.

* **Endpoint**: `GET /book-authors/{book_id}/{author_id}`
* **Python Controller**: `get_book_author_relationship`

### Update Book Author Role
Update the role of an author assigned to a book.

* **Endpoint**: `PUT /book-authors/{book_id}/{author_id}`
* **Python Controller**: `update_book_author_role`
* **Input Schema**: `BookAuthorUpdate`
* **Fields**:
  * `role` (string, optional, max 50 chars)

### Remove Author from Book
Remove an author assignment from a book.

* **Endpoint**: `DELETE /book-authors/{book_id}/{author_id}`
* **Python Controller**: `remove_author_from_book`

---

## Users Management

### Create User
Register a new user in the system with encrypted password storage.

* **Endpoint**: `POST /users/`
* **Python Controller**: `create_user`
* **Input Schema**: `UserCreate`
* **Fields**:
  * `username` (string, 3-50 chars, alphanumeric and underscores)
  * `email` (string, valid email format)
  * `password` (string, min 6 chars)
  * `user_id` (integer, optional)

### List Users
Retrieve a list of all registered users.

* **Endpoint**: `GET /users/`
* **Python Controller**: `list_users`

### Get User Detail
Retrieve details of a specific user by ID.

* **Endpoint**: `GET /users/{user_id}`
* **Python Controller**: `get_user`

### Update User
Update user details or update user password.

* **Endpoint**: `PUT /users/{user_id}`
* **Python Controller**: `update_user`
* **Input Schema**: `UserUpdate`
* **Fields**:
  * `username` (string, 3-50 chars, alphanumeric and underscores)
  * `email` (string, valid email format)
  * `password` (string, optional, min 6 chars)

### Delete User
Delete a user record from the system.

* **Endpoint**: `DELETE /users/{user_id}`
* **Python Controller**: `delete_user`

---

## Authentication Management

### Environment Configuration
The JWT authentication mechanism relies on secrets configured in `.env`:
* `JWT_SECRET_KEY`: Secret key used for signing JSON Web Tokens.
* `JWT_ALGORITHM`: Signature algorithm (default: `HS256`).
* `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiration duration in minutes (default: `30`).

### User Login
Authenticate user credentials and receive a signed JWT access token.

* **Endpoint**: `POST /auth/login`
* **Python Controller**: `login`
* **Input Schema**: `UserLogin`
* **Fields**:
  * `username` (string, required)
  * `password` (string, required)
* **Response Schema**: `TokenResponse`
* **Fields**:
  * `access_token` (string)
  * `token_type` (string, e.g., `"bearer"`)

### User Logout
Invalidate user session / log out the current authenticated user.

* **Endpoint**: `POST /auth/logout`
* **Python Controller**: `logout`
* **Headers**: `Authorization: Bearer <access_token>`
* **Response**: Confirmation message of successful logout.
