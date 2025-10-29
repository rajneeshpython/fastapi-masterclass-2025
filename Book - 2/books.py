from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(default=None, description="ID is not needed on create")
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=200)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Python",
                "author": "Rajneesh Kumar",
                "description": "Learn Python programming from basics to advanced concepts",
                "rating": 5,
                "published_date": 2025
            }
        }
    }


BOOKS = [
    Book(id=1, title="Python", author="Ravi Sharma", description="Learn Python programming from basics to advanced concepts", rating=5,published_date=2025),
    Book(id=2, title="Django", author="Priya Iyer", description="A complete guide to building web apps using Django", rating=4, published_date=2020),
    Book(id=3, title="Database", author="Amit Verma", description="Master relational and NoSQL databases with examples", rating=2, published_date=2000),
    Book(id=4, title="API", author="Neha Singh", description="Building RESTful APIs using FastAPI and Django REST Framework", rating=5, published_date=2022),
    Book(id=5, title="Design", author="Arjun Mehta", description="Understand software design principles and clean coding", rating=3, published_date=2022),
    Book(id=6, title="Database", author="Amit Verma", description="Master relational and NoSQL databases with examples", rating=2, published_date=2022),
    Book(id=7, title="API", author="Neha Singh", description="Building RESTful APIs using FastAPI and Django REST Framework", rating=5, published_date=2022),
    Book(id=8, title="Database", author="Amit Verma", description="Master relational and NoSQL databases with examples", rating=2, published_date=2000),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/published/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(request_book: BookRequest):
    new_book = Book(**request_book.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = BOOKS[-1].id + 1 if len(BOOKS) > 0 else 1
    return book


@app.put("/books/update-book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(**book.model_dump())
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail="Book not found")