from django.contrib import admin
from .models import Book, BookInstance, Genre, Language, Author
# Register your models here.
admin.site.site_header = "Library Admin"
admin.site.site_title = "Welcome | library Admin"
admin.site.index_title = "Admin Library"

class BookInlines(admin.StackedInline):
  model = Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
  list_display = ['last_name', 'first_name', 'date_of_birth']
  fields=['last_name', 'first_name', ('date_of_birth', 'date_of_death'), 'nationality']
  inlines=[BookInlines]

# admin.site.register(Author, AuthorAdmin)

# @admin.register(Book)

class BookInstanceInlines(admin.TabularInline):
  model = BookInstance

# same block
class BookAdmin(admin.ModelAdmin):
  list_display = ['title', 'author', 'display_genre']
  list_filter=['genre', 'author']
  inlines = [BookInstanceInlines]

admin.site.register(Book, BookAdmin)
# Same block


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
  list_display = ['book', 'status', 'id', 'borrower' ]
  list_filter = ['status', 'due_back']
  # exclude= ['id']
  fieldsets = [
        (
            None,
            {
                "fields": ["book", "id"],
            },
        ),
        (
            "Available Status",
            {
              "fields": ['status', 'due_back', 'borrower']
            }
            
        ),
    ]


admin.site.register(Genre)
# admin.site.register(Book)
admin.site.register(Language)