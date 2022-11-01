# Getting Started

- System requirements
    - Python v3.9
- Set up a virtual environment. Please refer to this
  [document](https://flask.palletsprojects.com/en/1.1.x/installation/#virtual-environments) for how to use virtual
  environments.
- Install dependencies
  ```
  pip install -r requirements.txt
  ```
- Seed database
  ```
  python seed.py
  ```
- Run dev server
  ```
  flask run --port=8080
  ```

# Getting Started (Docker)

Instead of following the steps above, you can also use Docker to set up your environment.

- System requirements
    - [Docker Compose](https://docs.docker.com/compose/install/)
- Run `docker-compose up` to spin up the dev server.
- Enter `Ctrl-C` in the same same terminal or `docker-compose down` in a separate terminal to shut down the server.

# Verify That Everything Is Set Up Correctly

You can use cURL or a tool like [Postman](https://www.postman.com/) to test the API.

#### Example Curl Commands

You can log in as one of the seeded users with the following curl command:

```bash
curl --location --request POST 'localhost:8080/api/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "thomas",
    "password": "123456"
}'
```

Then you can use the token that comes back from the /login request to make an authenticated request to create a new blog
post

```bash
curl --location --request POST 'localhost:8080/api/posts' \
--header 'x-access-token: your-token-here' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text": "This is some text for the blog post...",
    "tags": ["travel", "hotel"]
}'
```

# Helpful Commands

- `black .` : Runs auto-formatter.
- `flask test` : This repository contains a non-comprehensive set of unit tests used to determine if your code meets the
  basic requirements of the assignment. **Please do not modify these tests.**
- `python seed.py` : Wipes existing data and populates the database with sample data.
