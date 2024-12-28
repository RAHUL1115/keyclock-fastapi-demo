# Docker Compose RBAC Demo

This repository demonstrates a simple role-based access control (RBAC) setup using Docker Compose. The application has two predefined users:

- **Admin**: `admin@test.com` (Password: `test`, Role: Admin)
- **User**: `user@test.com` (Password: `test`, Role: None)

In this demo, users will log in to the app, and depending on their roles, they will have different access privileges.

## Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

Follow these steps to get the application up and running with Docker Compose:

1. **Clone the repository**:
```bash
git clone <your-repository-url> cd <your-repository-directory>
```

2. **Start the application with Docker Compose**:
Run the following command to start all services defined in the `docker-compose.yml` file:
```bash
docker-compose up -d
```
This will create and start the containers in the background.

3. **Access the application**:
Open your browser and go to the application URL (`http://localhost:8000>`).

4. **Login as User**:

- Go to the login page.
- Use the following credentials to log in:
  - **Email**: `user@test.com`
  - **Password**: `test`
- Upon successful login, click on the check button to check the status.

4. **Login as User**:

- Go to the login page.
- Use the following credentials to log in:
  - **Email**: `admin@test.com`
  - **Password**: `test`
- Upon successful login, click on the check button to check the status.
