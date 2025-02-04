from django.shortcuts import render 
from django.http import HttpResponse
from django.views import generic
from .models import Book, BookInstance, Author, Genre
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
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

class BookListView(LoginRequiredMixin, generic.ListView): #GET METHOD
  '''This will query our database and get all the records of the books that are available and it will render the records in our book_list template it will assume it is present in our templates/catalog(appname)/book_list.html(model_list)'''
  model= Book
  # Context default name--> book_list -> (modelName)_list
  template_name = 'book_list.html' #templates->catalog(appname)->book_list.html
  # def get_queryset(self):
  #   super().get_queryset()
  paginate_by= 1
  # Data 
  # context_object_name = 'book_list'

class BookDetailView(generic.DetailView):
  '''Detail view is the class based generic view: Single book ko detail information present garxa.. 
  1. ID Pathaunu parxa ? 
  2. model 
  3. template name over write
  4. context_object_name --> book_detail ()
  5. Custom query pani patahunu sakxam --> 
  --> REST FRAMEWORK 
  '''
  model = Book
  template_name ='book_detail.html'
  # context_object_name = 'book'
  
  #TODO: REquest Sessions -id match book return context 
  # HARRAY POTER, MACBETH, FIRE
  # MACBETH
  def get_context_data(self, **kwargs): #--> Dictionary, List, Memory variable member reference
    context= super().get_context_data(**kwargs)
    book = self.get_object()
    # recently_viewed_books = []
    if 'recently_viewed' in self.request.session: # check gareko already books haru addd garko xa ki xaina 
      # Recently_viewed array yo self.reqyest.session dictionary--> book.pk check garnae 
      if book.pk not in self.request.session['recently_viewed']:
        self.request.session['recently_viewed'].insert(0, book.pk)
      if len(self.request.session['recently_viewed']) > 3:
        self.request.session['recently_viewed'].pop()
    else: # first xoti add garnu khojeko 
      self.request.session['recently_viewed'] = [book.pk]
    self.request.session.modified = True
    recently_viewed_books_id = self.request.session['recently_viewed']
    context['recently_viewed'] =  Book.objects.filter(pk__in=recently_viewed_books_id)
    return context
