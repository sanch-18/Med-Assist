# Med-Assist
Medassist is a multi-functionality platform designed to help people in healthcare and related emergencies.

## Table of Contents

- [Installation](#installation)
- [Creating a Virtual Environment](#creating-a-virtual-environment)
- [Running the Server](#running-the-server)
- [Project Structure](#project-structure)
- [Features](#features)

## Installation

To get started with this project, clone the repository to your local machine:

```bash
git clone https://github.com/sanch-18/Med-Assist.git
```

Navigate into the project directory:

```bash
cd Med-Assist
```

## Creating a Virtual Environment

It is recommended to use a virtual environment to manage dependencies. To create a virtual environment, follow these steps:

1. Make sure you have Python installed. You can download it from [python.org](https://www.python.org/).

2. Create a virtual environment using the following command:

    ```bash
    python -m venv env
    ```

3. Activate the virtual environment:

    - On Windows:

        ```bash
        .\env\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source env/bin/activate
        ```

4. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Server

Once you have installed the dependencies, you can run the Django development server:
1. Go to directory containing manage.py

    ```bash
    cd KJSIT
    ```    
    
2. Apply the migrations:

    ```bash
    python manage.py migrate
    ```

3. Create a superuser to access the Django admin (optional but recommended):

    ```bash
    python manage.py createsuperuser
    ```

4. Start the development server:

    ```bash
    python manage.py runserver
    ```

5. Open your web browser and navigate to `http://127.0.0.1:8000/` to see the application running.

## Project Structure

Briefly describe the structure of your project, for example:

```
KJSIT/
│
├── KJSIT/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
│
├── main/
│   ├── migrations/
|   ├── templates/
|   ├── Models/
|   ├── static/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── ...
│
├── manage.py
└── db.sqlite
```

## Features

- List the main features of your project
- Feature 1 - MedPred - It is an application used for predicting the possibility of a particular disease based on symptoms and additional data.
- Feature 2 - MedScan - It is an application used for finding a particular disease from the list of possible diseases based on selecting symptoms.
- Feature 3 - History - Trcaks the usage of the application by the user along with date, time and results.
