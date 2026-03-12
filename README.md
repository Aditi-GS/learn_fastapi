# learn_fastapi
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