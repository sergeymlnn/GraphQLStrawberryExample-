from enum import Enum
from functools import wraps
from typing import Optional, List

import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.db import books


def dict_to_book(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    book = func(*args, **kwargs)
    if isinstance(book, dict):
      return Book(**{**book, "author": Author(**book["author"])})
    return [Book(**{**_book, "author": Author(**_book["author"])}) for _book in book]
  return wrapper


@strawberry.type
class Author:
  """"""
  id: strawberry.ID
  firstName: str
  lastName: str


@strawberry.enum
class BookStatus(Enum):
  """"""
  AVAILABLE = "Available"
  UNAVAILABLE = "Unavailable"
  INSTOCK = "Instock"
  SHIPPING = "Shipping"


@strawberry.input
class AuthorInput:
  """"""
  firstName: str = ""
  lastName: str = ""


@strawberry.input
class BookInput:
  """"""
  title: str
  status: BookStatus
  author: Optional[AuthorInput] = None
  description: Optional[str] = None


@strawberry.type
class Book:
  """"""
  id: strawberry.ID
  title: str
  status: BookStatus
  author: Author
  description: Optional[str] = None


@dict_to_book
def get_book_by_id(id: strawberry.ID) -> Book:
  """Returns full information about book using book id"""
  book = next(filter(lambda b: b["id"] == id, books), None)
  if not book:
    raise ValueError(f"Book with ID {id} not found")
  return book


@dict_to_book
def get_all_books() -> List[Book]:
  """Returns a list with information about all available books"""
  return [book for book in books]


@strawberry.type
class Query:
  """"""
  book: Book = strawberry.field(
    description="Information about specific book by its id",
    resolver=get_book_by_id
  )
  books: List[Book] = strawberry.field(
    description="Information about all books",
    resolver=get_all_books
  )


@strawberry.type
class Mutation:
  """"""
  @strawberry.mutation
  @dict_to_book
  def create_book(self, input: BookInput) -> Book:
    """Creates a new book"""
    book_id = len(books)
    book = {**input.__dict__, "id": book_id, "author": {**input.author.__dict__, "id": book_id}}
    books.append(book)
    return book

  @strawberry.mutation
  @dict_to_book
  def update_book(self, id: str, input: BookInput) -> Book:
    """Updates full or partial information about book with the specified book id"""
    book = books[int(id)]
    book_data = {k: v for k, v in input.__dict__.items() if v}
    book_author_data = {k: v for k, v in input.author.__dict__.items() if v}
    book = {**book, **book_data, "author": {**book["author"], **book_author_data}}
    books[int(id)] = book
    return book

  @strawberry.mutation
  @dict_to_book
  def delete_book(self, id: str) -> Book:
    """Deletes a book by the specified book id"""
    try:
      book = books.pop(int(id))
    except IndexError:
      raise ValueError(f"Book with ID {id} not found")
    return book


schema = strawberry.Schema(Query, Mutation)
graphql_app = GraphQLRouter(schema)
app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
