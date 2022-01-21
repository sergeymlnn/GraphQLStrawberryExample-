### Installation & Usage

```
python3 -m venv venv 
source venv/bin/activate
python -m pip install 'uvicorn[standard]' fastapi strawberry-graphql
uvicorn app.main:app --reload
```

### Testing Queries
```
query GetBooks {
  books{
    id
    title
    status
    author {
      firstName
      lastName
    }
  }
}

query GetBook {
  book(id: "2"){
    title
    status
    author {
      id
      firstName
      lastName
    }
  }
}


mutation CreateBook {
  createBook(input: {
    	title: "New Book !!!",
    	description: "This new book is about ...",
    	status: INSTOCK,
    	author: {
        firstName: "Markus",
        lastName: "John"
      }
  }) {
    id
    title
    status
    author {
    	firstName
      lastName
    }
  }
}

mutation UpdateBook {
  updateBook(id: "2", input: {
    title:"Goodbye, Hollywood",
    status: AVAILABLE,
    author: {
      lastName: "Mariues"
    }
  }) {
    title
    author {
      firstName
      lastName
    }
  }
}


mutation DeleteBook {
  deleteBook(id: "2") {
    title
    description
  }
}
```
