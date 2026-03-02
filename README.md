# learn_fastapi
## Day 1
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