from django.contrib import admin
from .models import Author, Book, Student, Transaction

# Basic registration for now, can be customized later

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'author', 'stock', 'published_date')
    list_filter = ('author', 'published_date')
    search_fields = ('title', 'isbn', 'author__name')
    raw_id_fields = ('author',) # Better UI for selecting authors if many exist

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'department', 'enrollment_date')
    search_fields = ('user__username', 'student_id', 'department')
    raw_id_fields = ('user',) # Better UI for selecting users

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'borrow_date', 'due_date', 'return_date', 'status', 'is_overdue')
    list_filter = ('status', 'borrow_date', 'due_date', 'return_date')
    search_fields = ('student__user__username', 'book__title', 'book__isbn')
    raw_id_fields = ('student', 'book') # Better UI for selection
    readonly_fields = ('borrow_date',) # Usually set automatically

    def is_overdue(self, obj):
        return obj.is_overdue()
    is_overdue.boolean = True # Display as a checkmark icon
