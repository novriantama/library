import os
import unittest
from datetime import date
# pyrefly: ignore [missing-import]
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set database URL for test
os.environ["DATABASE_URL"] = "sqlite:///./test_library.db"

from app.main import app
from app.infrastructure.database import Base, get_db

# Create a test database engine
engine = create_engine("sqlite:///./test_library.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Enforce foreign keys for tests
from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

class TestLibraryAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=engine)
        if os.path.exists("./test_library.db"):
            os.remove("./test_library.db")

    def setUp(self):
        # Clear tables between tests to keep isolation
        db = TestingSessionLocal()
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()
        db.close()

    # --- AUTHOR TESTS ---

    def test_create_author_success(self):
        response = self.client.post("/api/v1/authors/", json={
            "first_name": "J.K.",
            "last_name": "Rowling"
        })
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["first_name"], "J.K.")
        self.assertEqual(data["last_name"], "Rowling")
        self.assertIn("author_id", data)

    def test_create_author_validation_fails(self):
        # Empty first_name
        response = self.client.post("/api/v1/authors/", json={
            "first_name": "",
            "last_name": "Rowling"
        })
        self.assertEqual(response.status_code, 422)

        # first_name too long (>50 characters)
        response = self.client.post("/api/v1/authors/", json={
            "first_name": "A" * 51,
            "last_name": "Rowling"
        })
        self.assertEqual(response.status_code, 422)

    def test_get_author_not_found(self):
        response = self.client.get("/api/v1/authors/999")
        self.assertEqual(response.status_code, 404)

    def test_update_author_success(self):
        # Create first
        res = self.client.post("/api/v1/authors/", json={"first_name": "John", "last_name": "Doe"})
        author_id = res.json()["author_id"]

        # Update
        response = self.client.put(f"/api/v1/authors/{author_id}", json={
            "first_name": "Johnny",
            "last_name": "Doe"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["first_name"], "Johnny")

    def test_update_author_not_found(self):
        response = self.client.put("/api/v1/authors/999", json={
            "first_name": "Johnny",
            "last_name": "Doe"
        })
        self.assertEqual(response.status_code, 404)

    def test_delete_author_success(self):
        res = self.client.post("/api/v1/authors/", json={"first_name": "John", "last_name": "Doe"})
        author_id = res.json()["author_id"]

        response = self.client.delete(f"/api/v1/authors/{author_id}")
        self.assertEqual(response.status_code, 204)

        # Verify it's gone
        response = self.client.get(f"/api/v1/authors/{author_id}")
        self.assertEqual(response.status_code, 404)

    # --- BOOK TESTS ---

    def test_create_book_success(self):
        response = self.client.post("/api/v1/books/", json={
            "isbn": "9780747532699",
            "title": "Harry Potter and the Philosopher's Stone",
            "genre": "Fantasy",
            "publish_date": "1997-06-26"
        })
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["isbn"], "9780747532699")
        self.assertEqual(data["title"], "Harry Potter and the Philosopher's Stone")

    def test_create_book_validation_fails(self):
        # ISBN must be exactly 13 digits
        response = self.client.post("/api/v1/books/", json={
            "isbn": "1234567890",  # 10 digits
            "title": "Invalid ISBN Book",
            "genre": "Fiction"
        })
        self.assertEqual(response.status_code, 422)

        # ISBN must be digits only
        response = self.client.post("/api/v1/books/", json={
            "isbn": "978074753269A",  # Contains letter
            "title": "Invalid ISBN Book",
            "genre": "Fiction"
        })
        self.assertEqual(response.status_code, 422)

    def test_create_book_duplicate_isbn(self):
        # Create one
        self.client.post("/api/v1/books/", json={
            "isbn": "9780747532699",
            "title": "First Book",
            "genre": "Fantasy"
        })

        # Try to create another with same ISBN
        response = self.client.post("/api/v1/books/", json={
            "isbn": "9780747532699",
            "title": "Duplicate ISBN Book",
            "genre": "Fiction"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("already exists", response.json()["detail"])

    # --- BOOK-AUTHOR TESTS ---

    def test_assign_author_to_book_success(self):
        # Create Author
        res_a = self.client.post("/api/v1/authors/", json={"first_name": "J.K.", "last_name": "Rowling"})
        author_id = res_a.json()["author_id"]

        # Create Book
        res_b = self.client.post("/api/v1/books/", json={
            "isbn": "9780747532699",
            "title": "Harry Potter",
            "genre": "Fantasy"
        })
        book_id = res_b.json()["book_id"]

        # Assign
        response = self.client.post("/api/v1/book-authors/", json={
            "book_id": book_id,
            "author_id": author_id,
            "role": "Lead Author"
        })
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["book_id"], book_id)
        self.assertEqual(data["author_id"], author_id)
        self.assertEqual(data["role"], "Lead Author")

    def test_assign_author_to_book_not_found(self):
        # Try to assign to non-existent book/author
        response = self.client.post("/api/v1/book-authors/", json={
            "book_id": 999,
            "author_id": 999,
            "role": "Lead Author"
        })
        self.assertEqual(response.status_code, 404)

    def test_cascade_delete_author(self):
        # Create Author
        res_a = self.client.post("/api/v1/authors/", json={"first_name": "J.K.", "last_name": "Rowling"})
        author_id = res_a.json()["author_id"]

        # Create Book
        res_b = self.client.post("/api/v1/books/", json={
            "isbn": "9780747532699",
            "title": "Harry Potter",
            "genre": "Fantasy"
        })
        book_id = res_b.json()["book_id"]

        # Assign
        self.client.post("/api/v1/book-authors/", json={
            "book_id": book_id,
            "author_id": author_id,
            "role": "Lead Author"
        })

        # Verify assignment exists
        res_rel = self.client.get(f"/api/v1/book-authors/{book_id}/{author_id}")
        self.assertEqual(res_rel.status_code, 200)

        # Delete Author
        self.client.delete(f"/api/v1/authors/{author_id}")

        # Verify assignment was cascade deleted
        res_rel_after = self.client.get(f"/api/v1/book-authors/{book_id}/{author_id}")
        self.assertEqual(res_rel_after.status_code, 404)

    # --- USER TESTS ---

    def test_create_user_success(self):
        response = self.client.post("/api/v1/users/", json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123"
        })
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["email"], "testuser@example.com")
        self.assertIn("user_id", data)
        self.assertNotIn("password", data)
        self.assertNotIn("password_hash", data)

        # Query the database directly to verify password encryption
        from app.infrastructure.orm import UserORM
        db = TestingSessionLocal()
        user_orm = db.query(UserORM).filter_by(username="testuser").first()
        db.close()
        
        self.assertIsNotNone(user_orm)
        # The password_hash must be hashed (encrypted) using bcrypt, so it shouldn't match plaintext
        self.assertNotEqual(user_orm.password_hash, "securepassword123")
        # Bcrypt hash starts with $2b$ or $2a$
        self.assertTrue(user_orm.password_hash.startswith("$2b$") or user_orm.password_hash.startswith("$2a$"))

    def test_create_user_validation_fails(self):
        # Invalid email format
        response = self.client.post("/api/v1/users/", json={
            "username": "testuser",
            "email": "not-an-email",
            "password": "securepassword123"
        })
        self.assertEqual(response.status_code, 422)

        # Username with invalid characters
        response = self.client.post("/api/v1/users/", json={
            "username": "user-with-dash",
            "email": "testuser@example.com",
            "password": "securepassword123"
        })
        self.assertEqual(response.status_code, 422)

        # Password too short (< 6 characters)
        response = self.client.post("/api/v1/users/", json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "123"
        })
        self.assertEqual(response.status_code, 422)

    def test_create_user_duplicate_constraints(self):
        # Create first user
        self.client.post("/api/v1/users/", json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123"
        })

        # Try to create user with duplicate username
        response = self.client.post("/api/v1/users/", json={
            "username": "testuser",
            "email": "other@example.com",
            "password": "securepassword123"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("already exists", response.json()["detail"])

        # Try to create user with duplicate email
        response = self.client.post("/api/v1/users/", json={
            "username": "otheruser",
            "email": "testuser@example.com",
            "password": "securepassword123"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("already exists", response.json()["detail"])

    def test_update_user_success(self):
        res = self.client.post("/api/v1/users/", json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123"
        })
        user_id = res.json()["user_id"]

        # Update without changing password
        response = self.client.put(f"/api/v1/users/{user_id}", json={
            "username": "updateduser",
            "email": "updated@example.com"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "updateduser")

        # Verify password_hash remains unchanged
        from app.infrastructure.orm import UserORM
        db = TestingSessionLocal()
        user_orm_1 = db.query(UserORM).filter_by(user_id=user_id).first()
        db.close()

        # Update and change password
        response = self.client.put(f"/api/v1/users/{user_id}", json={
            "username": "updateduser",
            "email": "updated@example.com",
            "password": "newsecurepassword123"
        })
        self.assertEqual(response.status_code, 200)

        # Verify password_hash changed
        db = TestingSessionLocal()
        user_orm_2 = db.query(UserORM).filter_by(user_id=user_id).first()
        db.close()
        
        self.assertNotEqual(user_orm_1.password_hash, user_orm_2.password_hash)

    def test_delete_user_success(self):
        res = self.client.post("/api/v1/users/", json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123"
        })
        user_id = res.json()["user_id"]

        response = self.client.delete(f"/api/v1/users/{user_id}")
        self.assertEqual(response.status_code, 204)

        # Verify it's gone
        response = self.client.get(f"/api/v1/users/{user_id}")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()

