
Finally, create a **summary file**:
- `CRUD_operations.md`
```markdown
# CRUD Operations on Book Model

## Create
- Command: `Book.objects.create(title="1984", author="George Orwell", publication_year=1949)`
- Output: `<Book: 1984 by George Orwell (1949)>`

## Retrieve
- Command: `Book.objects.get(title="1984")`
- Output: `('1984', 'George Orwell', 1949)`

## Update
- Command: `book.title = "Nineteen Eighty-Four"; book.save()`
- Output: `'Nineteen Eighty-Four'`

## Delete
- Command: `book.delete()`
- Output: `<QuerySet []>`
