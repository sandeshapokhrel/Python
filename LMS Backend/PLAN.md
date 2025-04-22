# LMS Backend Development Plan

**Project Goal:** Create a Django backend for a Library Management System (LMS) featuring CRUD operations for Authors, Books, Students, and Transactions. The system will use JWT for authentication and follow a Clean Architecture approach by implementing a distinct service layer for business logic.

**Technology Stack:**

*   **Backend Framework:** Django
*   **API Framework:** Django REST Framework (DRF)
*   **Authentication:** `djangorestframework-simplejwt`
*   **Database:** SQLite (Default, can be configured later)

**Proposed Project Structure:**

```
lms_backend/
├── manage.py                 # Django management script
├── lms_project/              # Django project configuration directory
│   ├── __init__.py
│   ├── settings.py           # Project settings
│   ├── urls.py               # Project-level URL routing
│   ├── wsgi.py               # WSGI config
│   └── asgi.py               # ASGI config
├── apps/                     # Main application directory containing modules
│   ├── __init__.py
│   ├── core/                 # Core domain logic and models
│   │   ├── __init__.py
│   │   ├── models/           # Database models
│   │   │   ├── __init__.py
│   │   │   ├── author.py     # Author model
│   │   │   ├── book.py       # Book model
│   │   │   ├── student.py    # Student profile model (linked to User)
│   │   │   └── transaction.py # Transaction model
│   │   ├── admin.py          # Django admin registrations
│   │   └── apps.py           # App configuration for 'core'
│   ├── services/             # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py   # Authentication related logic
│   │   ├── author_service.py # Author CRUD logic
│   │   ├── book_service.py   # Book CRUD logic
│   │   ├── student_service.py # Student CRUD logic
│   │   └── transaction_service.py # Transaction logic (borrow/return)
│   ├── api/                  # API layer (DRF Views/Serializers)
│   │   ├── __init__.py
│   │   ├── serializers/      # Data serialization/validation
│   │   │   ├── __init__.py
│   │   │   ├── auth_serializers.py
│   │   │   ├── author_serializers.py
│   │   │   ├── book_serializers.py
│   │   │   ├── student_serializers.py
│   │   │   └── transaction_serializers.py
│   │   ├── views/            # API endpoints (ViewSets/APIViews)
│   │   │   ├── __init__.py
│   │   │   ├── auth_views.py
│   │   │   ├── author_views.py
│   │   │   ├── book_views.py
│   │   │   ├── student_views.py
│   │   │   └── transaction_views.py
│   │   ├── urls.py           # API specific URL routing
│   │   └── apps.py           # App configuration for 'api'
│   ├── tests/                # Automated tests
│   │   └── ...
│   └── apps.py               # Main 'apps' app configuration (if needed, often combined)
└── requirements.txt          # Python package dependencies
```
*(Note: The standard Django `User` model will be used for authentication, residing within Django's `auth` app, but we'll interact with it via our `auth_service` and `auth_serializers`)*

**Development Plan (Sequential Steps):**

1.  **Environment & Project Setup:**
    *   Create and activate a Python virtual environment.
    *   Install Django: `pip install django`
    *   Start the Django project: `django-admin startproject lms_project .`
    *   Start the main app structure: `python manage.py startapp core apps/core`, `python manage.py startapp api apps/api` (We'll create the `services` directory manually).
    *   Configure `settings.py`: Add `apps.core`, `apps.api`, `rest_framework`, `rest_framework_simplejwt` to `INSTALLED_APPS`. Set up database (default SQLite is fine for now).
    *   Create `requirements.txt`: `pip freeze > requirements.txt`

2.  **Define Core Models (`apps/core/models/`):**
    *   `Author`: Fields like `name`, `birth_date`, `biography`.
    *   `Book`: Fields like `title`, `isbn` (unique), `published_date`, `author` (ForeignKey to `Author`), `stock` (IntegerField).
    *   `Student`: Fields like `user` (OneToOneField to `django.contrib.auth.models.User`), `student_id` (unique), `department`, `enrollment_date`.
    *   `Transaction`: Fields like `book` (ForeignKey to `Book`), `student` (ForeignKey to `Student`), `borrow_date` (auto_now_add=True), `due_date`, `return_date` (null=True, blank=True), `status` (CharField choices: 'Borrowed', 'Returned').
    *   Run migrations: `python manage.py makemigrations core` & `python manage.py migrate`.
    *   Register models in `apps/core/admin.py` for easy data management during development.

3.  **Setup JWT Authentication & Basic User Handling:**
    *   Install DRF & SimpleJWT: `pip install djangorestframework djangorestframework-simplejwt`
    *   Update `requirements.txt`.
    *   Configure `settings.py`: Add DRF default settings (e.g., default permission classes, authentication classes using JWT). Configure `SIMPLE_JWT` settings (e.g., token lifetimes).
    *   Configure project URLs (`lms_project/urls.py`): Include DRF's Simple JWT default URLs (`/api/token/`, `/api/token/refresh/`). Include URLs for our `api` app (`path('api/', include('apps.api.urls'))`).
    *   Create basic User registration:
        *   Serializer (`apps/api/serializers/auth_serializers.py`): Handles user creation data.
        *   Service (`apps/services/auth_service.py`): Contains `register_user` function (hashes password, creates User, creates linked Student).
        *   View (`apps/api/views/auth_views.py`): Endpoint (`/api/register/`) that uses the serializer and calls the service.
    *   Update API URLs (`apps/api/urls.py`) for the registration endpoint.

4.  **Implement Service Layer (`apps/services/`):**
    *   Create Python files for each main entity (`author_service.py`, `book_service.py`, etc.).
    *   Implement functions for CRUD operations (e.g., `create_author`, `get_author_by_id`, `list_authors`, `update_author`, `delete_author`). These functions encapsulate the business logic and interact directly with the Django ORM (models).
    *   Implement transaction logic in `transaction_service.py` (e.g., `borrow_book(user, book_id)`, `return_book(user, transaction_id)`), including checks like book availability (stock) and updating book stock count.

5.  **Implement API Layer (`apps/api/`):**
    *   Create Serializers (`apps/api/serializers/`) for each model (Author, Book, Student, Transaction) to handle data validation and representation (input/output).
    *   Create ViewSets or APIViews (`apps/api/views/`) for each entity.
        *   These views will handle incoming HTTP requests.
        *   They will use the corresponding Serializers for data validation.
        *   They will call the appropriate functions from the Service Layer to perform actions.
        *   They will manage permissions (e.g., `IsAuthenticated`, potentially custom permissions like `IsLibrarianOrReadOnly`).
    *   Define routes in `apps/api/urls.py` using DRF's routers or standard path definitions to link URLs to Views.

6.  **Testing:**
    *   Write unit tests for service layer functions (e.g., test borrowing logic).
    *   Write integration tests for API endpoints (e.g., test creating a book via the API).

7.  **Documentation (Optional):**
    *   Integrate a tool like `drf-spectacular` to auto-generate OpenAPI documentation for the API.

**Diagram: Layer Interaction Flow**

```mermaid
graph TD
    subgraph Client Interaction
        User[Client/API Consumer]
    end

    subgraph API Layer (apps.api)
        direction LR
        Views[DRF Views / ViewSets]
        Serializers[DRF Serializers]
        UrlsApi[api/urls.py]
    end

    subgraph Service Layer (apps.services)
        direction LR
        AuthService[auth_service.py]
        BookService[book_service.py]
        TransactionService[transaction_service.py]
        AuthorService[author_service.py]
        StudentService[student_service.py]
    end

    subgraph Core Layer (apps.core)
        direction LR
        Models[Django Models]
        Admin[admin.py]
        Migrations[Migrations]
    end

    subgraph Framework & Infrastructure
        DjangoORM[Django ORM]
        Database[(Database)]
        JWT[SimpleJWT]
        DRF[DRF Framework]
    end

    User -- HTTP Request --> UrlsApi;
    UrlsApi --> Views;
    Views -- Uses --> Serializers;
    Views -- Calls --> AuthService;
    Views -- Calls --> BookService;
    Views -- Calls --> TransactionService;
    Views -- Calls --> AuthorService;
    Views -- Calls --> StudentService;

    AuthService -- Interacts with --> Models;
    BookService -- Interacts with --> Models;
    TransactionService -- Interacts with --> Models;
    AuthorService -- Interacts with --> Models;
    StudentService -- Interacts with --> Models;

    AuthService -- Uses --> JWT;
    Models -- Managed by --> DjangoORM;
    DjangoORM -- Talks to --> Database;
    Admin -- Uses --> Models;
    Migrations -- Defines schema for --> Database;
    Views -- Built on --> DRF;
    Serializers -- Built on --> DRF;