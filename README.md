# QnA Forum

QnA Forum is a Django-based web application that allows users to ask questions, provide answers, and interact with a community. It includes features like user authentication, voting, reporting, and administrative tools.

## Features

- **User Authentication**: Supports JWT-based authentication using `djoser` and `rest_framework_simplejwt`.
- **Questions and Answers**: Users can create questions, provide answers, and interact with others.
- **Voting System**: Users can upvote or downvote questions and answers.
- **Reports**: Users can report questions, and admins can approve or reject reports.
- **Admin Tools**: Admins can manage users, questions, answers, and reports through the Django admin panel.
- **REST API**: Fully functional REST API with nested routes for questions, answers, and votes.
- **Swagger and Redoc Documentation**: API documentation is available via Swagger UI and Redoc.
- **Excel Reports**: Admins can download detailed Excel reports for questions and their answers.

## Installation

### Prerequisites

- Python 3.8 or higher
- Django 5.1.5
- SQLite (default database)

### Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd qnaforum
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application:
   - Admin Panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
   - API Documentation (Swagger): [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)

## API Endpoints

### Authentication
- `POST /api/token/`: Obtain JWT access and refresh tokens.
- `POST /api/token/refresh/`: Refresh the access token.

### Questions
- `GET /questions/`: List all questions.
- `POST /questions/`: Create a new question.
- `GET /questions/{id}/`: Retrieve a specific question.
- `DELETE /questions/{id}/`: Delete a question (with permissions).

### Answers
- `GET /questions/{question_id}/answers/`: List answers for a question.
- `POST /questions/{question_id}/answers/`: Add an answer to a question.

### Votes
- `POST /questions/{question_id}/votes/`: Vote on a question.
- `POST /questions/{question_id}/answers/{answer_id}/votes/`: Vote on an answer.

### Reports
- `GET /reports/`: List all reports (admin only).
- `POST /reports/`: Create a report for a question.

## Project Structure

- **`forum/`**: Contains the main app for the QnA Forum.
  - **`models.py`**: Defines the database models for users, questions, answers, votes, and reports.
  - **`views.py`**: Contains the API views for handling requests.
  - **`serializers.py`**: Serializers for converting models to JSON and vice versa.
  - **`permissions.py`**: Custom permissions for access control.
  - **`signals.py`**: Signal handlers for creating user profiles and reports.
  - **`urls.py`**: Defines the API routes.
  - **`admin.py`**: Admin panel configurations.
- **`qa_forum/`**: Project-level settings and configurations.
- **`db.sqlite3`**: Default SQLite database (ignored in `.gitignore`).

## Development

### Running Tests
To run the tests, use:
```bash
python manage.py test
```

### Linting
Use `flake8` or `pylint` for linting:
```bash
pip install flake8
flake8 .
```

## Deployment

1. Set `DEBUG = False` in `settings.py`.
2. Configure a production database (e.g., PostgreSQL).
3. Use a production-ready WSGI server like Gunicorn.
4. Set up static file hosting using `collectstatic`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Contact

For any inquiries, please contact [surendrathapa986@gmail.com].