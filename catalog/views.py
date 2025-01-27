from django.shortcuts import render 
from django.http import HttpResponse
from django.views import generic
from .models import Book, BookInstance, Author, Genre
# Create your views here.
def index(request):
  '''View Function for the home page of our library'''
  '''Book.object.all() --> returns a query_set; It is like list but not exactly'''
  total_books = Book.objects.all().count()
  total_books_copies = BookInstance.objects.all().count()
  total_authors = Author.objects.all().count()
  
  # Book instance avaialble count 
  book_instance_available_count = BookInstance.objects.filter(status__exact = 'a').count()
  

  '''TODO:Fetch the genre from the Genre model and display the count...'''
  '''TODO:Fetch if specific letter "S" is available in genre and return the count...'''
  '''TODO: FETCH if the specific word is present in book title'''

  # bookswithGenreFanstasy = Book.objects.filter(genre__exact="fantasy")
  payload = {
    'total_books':total_books,
    'total_books_copies': total_books_copies,
    'total_authors':total_authors,
    'book_instance_available_count':book_instance_available_count
  }

  return render(request, 'index.html', context=payload)

class BookListView(generic.ListView): #GET METHOD
  '''This will query our database and get all the records of the books that are available and it will render the records in our book_list template it will assume it is present in our templates/catalog(appname)/book_list.html(model_list)'''
  model= Book
  # Context default name--> book_list -> (modelName)_list
  template_name = 'book_list.html'

  # def get_queryset(self):
  #   super().get_queryset()
    
  # context_object_name = 'book_list'

