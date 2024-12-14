# Adcash backend

Application was developed with Django Rest Framework version 3.15.2 and Python 3.10.11

---

## Prerequisites

Make sure you have the following installed on your system:

- Python (3.8 or later)
- PostgreSQL
- pip (Python package manager)
- Virtualenv (optional, but recommended)

---

### Clone the repository

```bash
git clone <https://github.com/yourusername/your-repository-name.git>
cd <repository-name>
```

## Creating a Virtual Environment

Before activating a virtual environment, you need to create one. Run the following command in your terminal or command prompt:

```bash
python -m venv <env_name>
```

Replace `<env_name>` with the name of your virtual environment. Usually `venv` is used.
<br/>

### Activation Instructions

#### Linux and macOS (Apple)

```python
source <env_name>/bin/activate
```

#### Windows

```python
# cmd
<env_name>\Scripts\activate

# powershell
<env_name>\Scripts\Activate.ps1
```

You should see the virtual environment name in your terminal prompt, indicating it is activated. Like this `(venv)`

### Deactivating the Virtual Environment

```bash
deactivate
```

---

For additional information, consult the Python documentation: [https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html)

## Database Setup

### 1. Create a PostgreSQL Database

Log in to your PostgreSQL server and run:

```sql
CREATE DATABASE mydb;
CREATE USER myuser WITH PASSWORD 'mypassword';
ALTER ROLE myuser SET client_encoding TO 'utf8';
ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
```

### 2. Configure Django to Use PostgreSQL

Create `.env` file in your base directory and configure these variables with your own database variables

For ease of use `SECRET_KEY` is not in `.env` file, but should be.

```python
# Database
DB_NAME=mydrfdb
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

# Settings
DJANGO_DEBUG=True
```

---

## Application setup

### Install dependencies

```bash
pip install -r requirements.txt
```

### Migrate database

```bash
python manage.py makemigrations
python manage.py migrate
```

## Run application

```bash
python manage.py runserver
```
