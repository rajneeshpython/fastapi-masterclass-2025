from fastapi import Body, FastAPI

# Initialize the FastAPI app
app = FastAPI()

# In-memory list of books (acting as a mock database)
BOOKS = [
    {"title": "FastAPI", "author": "Sebastian Ramirez", "category": "technology"},
    {"title": "Django", "author": "William Vincent", "category": "technology"},
    {"title": "Python", "author": "Luciano Ramalho", "category": "technology"},
    {"title": "Sapiens", "author": "Yuval Noah Harari", "category": "history"},
    {"title": "Cosmos", "author": "Carl Sagan", "category": "science"},
    {"title": "Algebra", "author": "Sheldon Axler", "category": "math"},
]


@app.get("/books")
async def get_all_books():
    # Return the complete list of books
    return BOOKS


@app.get("/books/by_category")
async def read_category_by_query(category: str):
    # Filter books by category (case-insensitive)
    books_to_return = [
        book for book in BOOKS
        if book.get("category").casefold() == category.casefold()
    ]
    return books_to_return


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    # Find a book by its title (case-insensitive)
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book
    return {"message": "Book not found"}


@app.get("/books/author/{book_author}")
async def read_author_category_by_query(book_author: str, category: str):
    # Filter books by both author and category (case-insensitive)
    books_to_return = [
        book for book in BOOKS
        if (
            book.get("author").casefold() == book_author.casefold()
            and book.get("category").casefold() == category.casefold()
        )
    ]
    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    # Add a new book to the list
    BOOKS.append(new_book)
    return {"message": "Book added successfully", "book": new_book}


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    # Update an existing book's details
    for book in BOOKS:
        if book.get("title").casefold() == updated_book.get("title").casefold():
            book.update(updated_book)
            return {"message": "Book updated", "book": book}
    return {"message": "Book not found"}


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    # Delete a book by title
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            BOOKS.remove(book)
            return {"message": f"Book '{book_title}' deleted successfully"}
    return {"message": "Book not found"}
