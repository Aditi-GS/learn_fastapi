# learn_fastapi
### Note: Each Heading is also a git tag name. (e.g: Part-1)
## Part 1
1. venv: virtual environments 
    - version control over different libraries
    - separate command line
    - separate interpreter

    py - 3 venv <venv_alias_name>

    - <venv_alias_name>/Scripts/activate.bat    =>  enable it in terminal
    - pip install commands results (any library installation) stored in <venv_alias_name>/Lib

2. pip install fastapi[all]
    - [all] =>  installs dependencies as well
    - pip freeze    =>  displays those additionally installed libs

3. FastAPI() creates an instance of the app

4. @app.<http_method>("/<endpoint_path>") above the function that actually performs what the endpoint is supposed to do

5. uvicorn <file_where_the_app_instance>:<app_instance_name> starts a server on local host

6. Same command above but with tag "--reload" starts a live server (don't have to restart the server after every change)

7. If change includes change to the file name or the instance name itself then post reload in above step, it will throw : 

    ERROR: Error loading ASGI app. Attribute "instance" not found in module "main".

8. Default port = 8000

### What is DECORATOR in python ?
[James Powell: So you want to be a Python expert? | PyData Seattle 2017](https://www.youtube.com/watch?v=cKPlPJyQrt4&t=3099s)

[python_decorator_guide.md](https://gist.github.com/Zearin/2f40b7b9cfc51132851a)

## Part 2
1. Order your endpoints in the correct order

Example: 
```python
@app.get("/posts/{id}")
def get_post_by_id(id: int):
    post = find_post_by_id(id)
    return post

@app.get("/posts/latest")

def get_latest_post():
    post = my_posts[-1]
    return post
```

Here `/posts/{id}` will be considered first before `/posts/latest`

Because of this, when we fire `/posts/latest` call the `latest` part in the endpoint will be considered as the path param `{id}` and you will end up getting this error: 

```json
{
    "detail": [
        {
            "type": "int_parsing",
            "loc": [
                "path",
                "id"
            ],
            "msg": "Input should be a valid integer, unable to parse string as an integer",
            "input": "latest"
        }
    ]
}
```

2. Always include the Correct Response Codes for both successful and failed operations

3. When HTTP status code = 204 (No-Content) (used for delete) and you also return any kind of text or message => violates Content-Length (as No Content should be returned)

4. Why use Parameterized Queries instead of simple String Formatting ?

Example: 
Parameterized Query:
```python
query = """SELECT * FROM users WHERE username = %s AND password = %s"""
cursor.execute(query, (username, password))
```

String Formatting:
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)
```

Now if someone gives password's value as `'' OR '1' = '1'` then the query becomes:
```sql
SELECT * FROM users WHERE username = admin AND password = '' OR '1' = '1'
```

Which will result in all records being returned !!!
This is called `SQL INJECTION`
With parameterized queries `%s`, the input value is treated only as DATA, not as SQL Code. So even if `'' OR '1' = '1'` is passed, it will treated as a string instead.

5. When passing a single value for a parameter in a query, make sure to add `,`
Why ?

Example:
```python
    query = """SELECT * FROM posts WHERE id=%s"""
    cursor.execute(query, vars=(id,))
```

Without `,` i.e., `vars=(id)`, in python `(number)` is treated as an integer. But `vars` argument
only takes `tuples` as input. Adding a comma when a single value has to passed, makes it a tuple.

## Part 3

1. ORM = Object Relational Mappers
- Abstraction between us and DB
- Still can't talk to DB directly -> instead interacts with DB driver (e.g psycopg2)
- Can create tables, queries via Python directly (no need of SQL and tables existence)

2. SQLModel in FastAPI = SQLAlchemy (ORM) + Pydantic

3. DROP Table = Deletes the entire table => the records/rows + the structure/schema
   TRUNCATE Table = Deletes only the data => the records/rows BUT retains the structure/schema

4. Default port for postgres = 5432

5. ** before a pydantic_model.model_dump() = unpacks the values in the pydantic-model-converted-dictonary

6. If you update a column or create a new one in your table definition, even with `uvicorn --reload`, the column won't be reflected in the DB. This is because `uvicorn` command only reloads the server code/FastAPI application instance but not the DB (since it doesn't interact with it directly, but instead via ORM)

So how come the table was created at the start ?

```python
models.Base.metadata.create_all(bind=engine)
```

The `create_all()` function is the one that creates the table the first time.
This only creates tables if it doesn't exist. If it does, then it does nothing.
So, if the table properties are updated, then it won't reflect after `--reload`

7. `id = Column(type_=Integer, primary_key=True, nullable=False)` why `id` auto-increments even though I didn't specify ?

When a field is `Integer + PK`, SQLAlchemy automatically configures this as an auto-incrementing sequence in PostgreSQL.
So internally:
    `id SERIAL PRIMARY KEY` == `id INTEGER NOT NULL DEFAULT nextval('posts_id_seq')`

8. If there are extra fields that are passed in the body, which are not included in the Pydantic Schema, those fields are ignored/silently dropped without raising any errors coz `extra = "ignore"` is the default behavior.
To avoid this, add `model_config = ConfigDict(extra="forbid")`, which will throw: 

`422 Unprocessable Content`
```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": [
                "body",
                "<field_name>"
            ],
            "msg": "Extra inputs are not permitted",
            "input": 1
        }
    ]
}
```

9. Pydantic Models = Schema Models (Contracts -> Structuring + Config of Data to recieve and/or send)
   SQLAlchemy Models = Table Definitions