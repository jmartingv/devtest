# Dev Test

## Installing dependencies

To install the necessary dependencies/packages, navigate into the project repository and run the following command:

`pip install -r requirements.txt`

## Running the project

After installing the required packages, and while still in the project repository, run the following command to start the server

`uvicorn elevator.main:app --reload`

For the tests, run:

`pytest -v elevator/tests/tests.py`

Once the app is running, the Swagger documentation for the endpoints can be accessed at `http://127.0.0.1:8000/docs` or at `http://127.0.0.1:8000/redoc`
