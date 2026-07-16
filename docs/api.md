# Library API Specification

This document details the REST endpoints available for managing books in the library system.

---

## Books Management

### Create Book
Add a new book record to the system catalog.

* **Endpoint**: `POST /books/`
* **Python Controller**: `create_book`
* **Input Schema**: `BookCreate`
* **Fields**:
  * `isbn` (string)
  * `title` (string)
  * `genre` (string)
  * `publish_date` (date)
  * `book_id` (integer)

### List Books
Retrieve a list of all book records registered in the system.

* **Endpoint**: `GET /books/`
* **Python Controller**: `list_books`

### Get Book Detail
Retrieve a specific book record by its unique ID.

* **Endpoint**: `GET /books/{book_id}`
* **Python Controller**: `get_book`
