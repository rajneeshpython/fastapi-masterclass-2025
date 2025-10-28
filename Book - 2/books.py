from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=200)
    rating: int = Field(ge=1, le=5)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Python",
                "author": "Rajneesh Kumar",
                "description": "Learn Python programming from basics to advanced concepts",
                "rating": 5
            }
        }
    }


BOOKS = [
    Book(id=1, title="Python", author="Ravi Sharma", description="Learn Python programming from basics to advanced concepts", rating=5),
    Book(id=2, title="Django", author="Priya Iyer", description="A complete guide to building web apps using Django", rating=4),
    Book(id=3, title="Database", author="Amit Verma", description="Master relational and NoSQL databases with examples", rating=2),
    Book(id=4, title="API", author="Neha Singh", description="Building RESTful APIs using FastAPI and Django REST Framework", rating=5),
    Book(id=5, title="Design", author="Arjun Mehta", description="Understand software design principles and clean coding", rating=3),
    Book(id=6, title="Database", author="Amit Verma", description="Master relational and NoSQL databases with examples", rating=2),
    Book(id=7, title="API", author="Neha Singh", description="Building RESTful APIs using FastAPI and Django REST Framework", rating=5),
    Book(id=8, title="Design", author="Arjun Mehta", description="Understand software design principles and clean coding", rating=3),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return {"message": "Book not found"}


@app.get("/books/")
async def read_book_by_rating(rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book")
async def create_book(request_book: BookRequest):
    new_book = Book(**request_book.model_dump())
    BOOKS.append(find_book_id(new_book))
    return {"message": "Book created successfully"}


def find_book_id(book: Book):
    book.id = BOOKS[-1].id + 1 if len(BOOKS) > 0 else 1
    return book