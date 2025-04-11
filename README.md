# QnA Forum

## Overview
QnA Forum is a Django-based web application that allows users to ask questions, provide answers, vote on questions and answers, and generate reports. It includes features such as user authentication, role-based permissions, and an admin panel for managing content.

## Features
- User registration and authentication
- Role-based access control (Admin/User)
- Create, read, update, and delete questions and answers
- Voting system for questions and answers
- Reporting system for questions
- Admin panel for managing users, questions, and reports
- API documentation using Swagger and Redoc

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd qnaforum
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables:
   Create a `.env` file in the root directory and add the following:
   ```env
   SECRET_KEY=<your-secret-key>
   DEBUG=True
   DATABASE_NAME=<your-database-name>
   DATABASE_USER=<your-database-user>
   DATABASE_PASSWORD=<your-database-password>
   DATABASE_HOST=<your-database-host>
   DATABASE_PORT=<your-database-port>
   ```

5. Apply migrations:
   ```bash
   python manage.py migrate
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000/`.

## Custom Management Command: Populate Database

This project includes a custom management command to populate the database with dummy data for testing purposes.

### How to Use the Command

1. Navigate to the project directory:
   ```bash
   cd qnaforum
   ```

2. Run the custom command:
   ```bash
   python manage.py populate_forum --users <number_of_users> --questions <number_of_questions> --answers <number_of_answers> [--clear]
   ```

   - `--users`: Number of users to create (default: 10)
   - `--questions`: Number of questions to create (default: 30)
   - `--answers`: Number of answers to create (default: 100)
   - `--clear`: Clears existing data before populating

### Example
To create 20 users, 50 questions, and 200 answers, and clear existing data:
```bash
python manage.py populate_forum --users 20 --questions 50 --answers 200 --clear
```

## API Documentation

API documentation is available at:
- Swagger UI: `/api/schema/swagger-ui/`
- Redoc: `/api/schema/redoc/`

## Testing

Run the test suite using:
```bash
python manage.py test
```

## License
This project is licensed under the MIT License.