from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='index'),
    path('books', views.BookListView.as_view(), name='book-list'), #Class Based Views 
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'), #Class Based Views 
    path("mybooks/", views.BorrowedBooksListView.as_view(), name="my-books"),
    path("markreturn/<uuid:id>", views.markReturned , name="mark-return"),
    path("allborrowedbooks/", views.AllBorrowedBooksListView.as_view(), name="all-borrowed-books")
]