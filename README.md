# Assignment-Submission-Portal

```markdown
# Assignment Submission Portal API

Welcome to the Assignment Submission Portal API! This document provides a comprehensive guide on how to interact with the API for user and admin functionalities.

## Table of Contents

- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
  - [User Endpoints](#user-endpoints)
  - [Admin Endpoints](#admin-endpoints)
- [Error Handling](#error-handling)
- [Running the Application](#running-the-application)

## Getting Started

### Prerequisites

- Python 3.x installed on your system.
- MongoDB installed and running.
- Required Python packages installed:

  ```bash
  pip install Flask Flask-PyMongo Flask-Bcrypt
  ```

### Setting Up the Application

Clone the Repository:

```bash
git clone <repository-url>
cd <repository-folder>
```

Set Environment Variables (Optional):

It's recommended to set up your environment variables, such as the secret key.

```bash
export SECRET_KEY='your_secret_key'
```

Run the Application:

Execute the following command to start the Flask application:

```bash
python app.py
```

Access the API:

The API will be accessible at `http://localhost:5000`.

## API Endpoints

### User Endpoints

#### User Registration

**Endpoint:** `POST /register`

**Request Body:**

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**

**Success:**

```json
{
  "message": "User registered successfully!"
}
```

**Error:**

```json
{
  "error": "Username and password are required!"
}
```

#### User Login

**Endpoint:** `POST /login`

**Request Body:**

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**

**Success:**

```json
{
  "message": "Login successful!"
}
```

**Error:**

```json
{
  "error": "Invalid credentials!"
}
```

#### Upload Assignment

**Endpoint:** `POST /upload`

**Request Body:**

```json
{
  "task": "your_task_description",
  "admin": "admin_username"
}
```

**Response:**

**Success:**

```json
{
  "message": "Assignment uploaded successfully!"
}
```

**Error:**

```json
{
  "error": "Task and admin fields are required!"
}
```

### Admin Endpoints

#### Admin Registration

**Endpoint:** `POST /admin/register`

**Request Body:**

```json
{
  "username": "admin_username",
  "password": "admin_password"
}
```

**Response:**

**Success:**

```json
{
  "message": "Admin registered successfully!"
}
```

**Error:**

```json
{
  "error": "Admin username already exists!"
}
```

#### Admin Login

**Endpoint:** `POST /admin/login`

**Request Body:**

```json
{
  "username": "admin_username",
  "password": "admin_password"
}
```

**Response:**

**Success:**

```json
{
  "message": "Admin login successful!"
}
```

**Error:**

```json
{
  "error": "Invalid credentials!"
}
```

#### View Assignments

**Endpoint:** `GET /admin/assignments`

**Response:**

**Success:**

```json
[
  {
    "_id": "assignment_id",
    "admin": "admin_username",
    "task": "assignment_task",
    "userId": "user_id"
  }
]
```

#### Accept Assignment

**Endpoint:** `POST /admin/assignments/<assignment_id>/accept`

**Response:**

**Success:**

```json
{
  "message": "Assignment accepted!"
}
```

**Error:**

```json
{
  "error": "Assignment not found or status already accepted!"
}
```

#### Reject Assignment

**Endpoint:** `POST /admin/assignments/<assignment_id>/reject`

**Response:**

**Success:**

```json
{
  "message": "Assignment rejected!"
}
```

**Error:**

```json
{
  "error": "Assignment not found or status already rejected!"
}
```

## Error Handling

All endpoints return appropriate error messages for various failure scenarios, including missing fields and invalid credentials. Ensure to check the response status codes and messages for debugging.

## Running the Application

1. Start your MongoDB server.
2. Ensure all necessary Python packages are installed.
3. Run the Flask application using:

```bash
python app.py
```

4. Use Postman or any API testing tool to interact with the endpoints as described above.
```

You can copy and paste this into your GitHub repository's README file. Let me know if you need any further adjustments!
