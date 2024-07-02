
# Trees Everywhere

Trees Everywhere is a web application for managing trees planted arround the world, where users can register, view, and manage the trees they have planted. The application is built with Django and Django REST Framework, using MySQL as the database.

## Features

- User registration and authentication
- Register planted trees
- View trees planted by the user
- Edit and delete tree records
- Filter to view trees by account and user

## Requirements

- Python 3.12
- Docker
- Docker Compose

## Setup Instructions

### Step 1: Clone the Repository

Clone the repository to your local environment:

```bash
git clone https://github.com/marquesdavi/trees-everywhere.git
cd trees-everywhere
```

### Step 2: Configure the `.env` File

Create a `.env` file in the root directory of the project and add the following configurations:

```env
DEBUG=True
SECRET_KEY=yoursecurekey
DATABASE_NAME=trees_everywhere
DATABASE_USER=admin
DATABASE_PASSWORD=admin
DATABASE_HOST=localhost
DATABASE_PORT=3308
ALLOWED_HOSTS=127.0.0.1,.localhost
```

### Step 3: Build and Start the Containers

Run the following commands to build and start the Docker containers:

```bash
docker-compose build
docker-compose up
```

### Step 4: Apply Migrations and Create Superuser

In a new terminal, run the following commands to apply migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Step 5: Access the Application

The application will be available at `http://localhost:8000`. You can access the Django admin at `http://localhost:8000/admin` and log in with the superuser credentials you created.

## Running Tests

To run the tests, use the following command:

```bash
python manage.py test
```

## Technologies Used

- Django 5.0.6
- Django REST Framework 3.15.2
- MySQL 8.0
- Docker Compose
- Python Dotenv 1.0.1
- Django Crispy Forms 2.2
- Factory Boy 3.3.0

## Routes

### Global Routes

- **Home:** `GET /` - Home view
- **Admin:** `GET /admin/` - Django admin panel

### Users App

- **Signup:** `GET /users/signup/` - User registration view
- **Login:** `GET /users/login/` - User login view
- **Logout:** `GET /users/logout/` - User logout view
- **Profile Detail:** `GET /users/profile/` - User profile detail view
- **Profile Edit:** `GET /users/profile/edit/` - User profile edit view

### Trees App

- **Tree List:** `GET /trees/` - List of planted trees
- **Tree Detail:** `GET /trees/planted-tree/<int:pk>/` - Detail view of a specific planted tree
- **Create Tree:** `GET /trees/planted-tree/new/` - Create a new planted tree
- **Edit Tree:** `GET /trees/planted-tree/<int:pk>/edit/` - Edit a planted tree
- **Delete Tree:** `GET /trees/planted-tree/<int:pk>/delete/` - Delete a planted tree

### Trees API

- **Tree List API:** `GET /api/trees/planted-trees/` - API endpoint to list planted trees
- **Tree Detail API:** `GET /api/trees/planted-trees/<int:pk>/` - API endpoint to retrieve, update, or delete a specific planted tree

### Accounts App

- **Account List:** `GET /accounts/` - List of accounts

### Accounts API

- **Account List API:** `GET /api/accounts/` - API endpoint to list accounts
- **Account Detail API:** `GET /api/accounts/<int:pk>/` - API endpoint to retrieve, update, or delete a specific account

