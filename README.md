# learn_fastapi
# Table of Contents
1. [Simple GET + POST](#part-1)
2. [CRUD + Postgres DB](#part-2)
3. [SQLAlchemy (ORM) + Pydantic Models](#part-3)
4. [Routers + Auth](#part-4)
5. [FK + Relationship + Env](#part-5)
6. [Votes + Join + Aggregate](#part-6)

### Note: Each Heading is also a git tag name. (e.g: Part-1)

## Part 1  <a name="part-1"></a>
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

## Part 4

1. Hashing Passwords
2. FastAPI routers (with prefix) = modular
3. Organized look in OpenAPI Spec file using `tags`
#### Authentication : 
4. JWT = JSON Web Tokens <=> Headers (algo + token type) + Token Data (Payload) + SECRET == Signature
5. OAuth2PasswordRequestForm will always have 2 specific fields only = `username` and `password`

## Part 5

1. Foreign Keys (Constraints)
2. Check FK before CRUD + Handle FK violation
3. Relationships only exist on SQLAlchemy ORM side => they are not enforced in DB in anyway 
(i.e, no columns/constraints are created - depicting the relationship that we define)
4. `relationship()` tells SQLAlchemy :
    - the related objects to load
    - navigate between linked models
5. `back_populates` attribute in `relationship()` explicity defines what model/table you are linking the attribute to.
The value of it is the name of the relationship in the other model.

Example: 
```python
class Post(Base):
    ...
    user = relationship("User", back_populates="posts")
    # means that on the other model ("User"), this relationship is called "posts"
class User(Base):
    ...
    posts = relationship("Post", back_populates="user")     
    # means that on the other model ("Post"), this relationship is called "user"
```
When `back_populates` is declared on both sides => keeps both the linked models in sync

6. SQLAlchemy loads the related objects based on the FK defined - it is not necessary to mention which FK to use in order to load the related objects, UNLESS, there are multiple FKs defined => It infers the join condition from the FK.

7. Query Params, Pagination, Keyword Based Search

8. Sensitive info in .env

## Part 6

1. Composite Key = Primary Key that spans multiple columns
2. Aggregate on JOIN results
3. Filter before Join for efficiency => Query Planner optimizes this by default
4. `joinedload` is a SQLAlchemy eager loading strategy for relationships
Example: 
```python
posts_query = db.query(Post, func.count(Votepost_id).label("votes"))\
        .options(joinedload(Post.user))\
        # load related user with post
```
5. Manual reshaping:
```python
class PostWithVotesResponse(BaseModel):
    post: PostResponse
    votes: int
    model_config = ConfigDict(from_attributes=True)
```
```python
@router.get("/", response_model=List[PostWithVotesResponse])
def get_all_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user),
                  limit: int = 5, offset: int = 0, sort: str = "desc", title_contains: Optional[str] = ""):
       
    posts_query = db.query(Post, func.count(Vote.post_id).label("votes"))\
                .options(joinedload(Post.user))\
                .join(Vote, Post.id == Vote.post_id, isouter=True)\
                .group_by(Post.id)\
                .filter(
                    Post.user_id == current_user.id,\
                    Post.title.contains(title_contains)
                )

    if sort == "asc":
        posts_query = posts_query.order_by(Post.id.asc())
    else:
        posts_query = posts_query.order_by(Post.id.desc())

    posts = posts_query.limit(limit).offset(offset).all()        

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Table so empty T_T")
    
    # Reshape (Post, votes) tuples into PostWithVotesResponse
    results = [
        PostWithVotesResponse(post=PostResponse.model_validate(post), votes=votes)
        for post, votes in posts
    ]

    return results
```
Here since the query returns in `(Post, votes)` format (which is not a dict but a SQLAlchemy result row) we will have to reshape using `model_validate()`.
[Why does SQLAlchemy return as "Post" ? = because it goes by the model name that we have defined.]
But instead if change the schema from before to:
```python
class PostWithVotesResponse(BaseModel):
    Post: PostResponse  # capital P => matches the format that is returned after querying
    votes: int
    model_config = ConfigDict(from_attributes=True)
```
then we can `return posts` direclty since Pydantic checks for `row.Post` and maps it automatically.

6. SQL issues when you do Eager Loading: 
```python
def get_all_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user),
                  limit: int = 5, offset: int = 0, sort: str = "desc", title_contains: Optional[str] = ""):
       
    posts_query = db.query(Post, func.count(Vote.post_id).label("votes"))\
                .options(joinedload(Post.user))\
                .join(Vote, Post.id == Vote.post_id, isouter=True)\
                .group_by(Post.id)\
                .filter(
                    Post.user_id == current_user.id,\
                    Post.title.contains(title_contains)
                )
# ... so on
```
Here we are loading `User` info `eagerly` upon the filtered and joined results of `Post` and `votes`.
This will throw an SQL error :
```console
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.GroupingError) column "users_1.id" must appear in the GROUP BY clause or be used in an aggregate function
```
This is because of : 
```python
.options(joinedload(Post.user))\
.join(Vote, Post.id == Vote.post_id, isouter=True)\
.group_by(Post.id)\
```
`joinedload(Post.user)` forces SQLAlchemy to include users table columns in the SELECT query.
But the query only has `GROUP BY posts.id`.
PostgreSQL requires:
    Every selected column must be in GROUP BY or aggregated
Since users columns are selected but not grouped, the query fails.
Solutions: 
    a. remove `joinedload(Post.user)` => remove **eager loading** -> fixes GROUP BY error.
    b. keep eager loading but explicitly fix the error by doing `.group_by(Post.id, Post.user_id)` => will include user columns in GROUP BY

7. Solution A => How does it know to fetch `User` info when I am only joining and retrieving `Post & Vote` info ?
**Lazy Loading of Related Tables in SQLAlchemy**
SQLAlchemy still automatically loads the related User table ONLY when accessed => on demand.
The Post.user relationship is defined via:
```python
user = relationship("User", back_populates="posts")
```
By default, SQLAlchemy uses lazy loading:
    - The initial query fetches only Post (and vote counts)
```python
db.query(Post, func.count(Vote.post_id).label("votes"))
```
When post.user is accessed (e.g., during Pydantic serialization),
```python
class PostResponse(BaseModel):
    user: _PostUserResponse
```
SQLAlchemy runs a separate query:
```sql
SELECT * FROM users WHERE id = post.user_id;
```
The `user_id` foreign key tells SQLAlchemy which User to load.
```python
user_id = Column(Integer, ForeignKey("users.id"))
```
**BUT** this introduces `N+1` problem
For example, the main query to fetch posts after filtering & joining returns 5 posts.
Now by lazy loading, which happens for every row, 5 queries are executed additionally to fetch user info.
So, instead of 1 Query (which we mention in the code), + N (in our case +5) queries would be executed behind the scenes. 

Solution for this can be using `selectinload` which avoids both `N+1` and `GROUP BY` issues. Instead of N + 1, only 2 queries will be executed. 
After the 1st query, a 2nd *Batch Query* will be executed to fetch all related users based on the `user_id`s in the results of the 1st query -- and map them back to corresponding `Post.user` objects.
Example:
```sql
SELECT * FROM users WHERE users.id IN (<user_id_1>, <user_id_2>, ..., <user_id_N>);
```
