from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.auth_views import UserRegistrationView
from .views.author_views import AuthorViewSet
from .views.book_views import BookViewSet
from .views.student_views import StudentViewSet
from .views.transaction_views import TransactionViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'books', BookViewSet, basename='book')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'transactions', TransactionViewSet, basename='transaction')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # Authentication URLs
    path('register/', UserRegistrationView.as_view(), name='user_register'),

    # Include router URLs
    path('', include(router.urls)),

    # Transaction custom actions are automatically routed by the ViewSet router
    # e.g., /api/transactions/borrow/ (POST)
    # e.g., /api/transactions/{pk}/return/ (POST)
]