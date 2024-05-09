# Perfect Memory Training

This project is part of the perfect memory developer training.

This project parsers the data from a csv file, transform it into a rdfs graph and send to the exchange manager api to insert in the knowledge base. It uses an existing process called insertGraph to make this operation.


## Setup

To set up the project, follow these steps:

#### Step 1

First of all, clone this project in your local machine.


```
$ git clone https://github.com/JuninhoCarlos/perfect-memory-training.git
$ cd perfect-memory-training
```

#### Step 2

Create a virtual environment and activate it, and install the dependencies.

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

To install developer dependencies like pylint, black formatter and ipdb debugger uses de `requirements-dev.txt` file

#### Step 3

Create a `.env` file in `/lib` folder. There is a `env.sample` file in the `/lib` folder that you can fill with your own parameters and credentials.

```
$ cat lib/env.sample > lib/.env
```

The variable are the following:

- `EM_BASE_URL` : base url from the exchange manager api
- `EM_API_KEY` : api key from the exchange manager api
- `EM_CLIENT_NAME` : name of the exchange manager client


## Running the application

To run the application execute:


```
$ python3 lib/main.py -p <path_to_your_csv>
```

You can use the csv that is in the repo and run  `python3 lib/main.py -p pizzas.csv`

## Running the tests and check coverage


To run the unit test execute the following command:

```
$ pytest
```

To run test and check coverage analisys you can run the following commands:

```
$ coverage run -m pytest
$ coverage report
```

