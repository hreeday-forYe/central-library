from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import Book, BookInstance, Author, Genre
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
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
  paginate_by= 3
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


class BorrowedBooksListView(LoginRequiredMixin,generic.ListView):
  model = BookInstance
  template_name = 'my_books.html'
  def get_queryset(self):
    return (
      BookInstance.objects.filter(borrower = self.request.user).filter(status__exact="l").order_by('due_back')
    )
  

class AllBorrowedBooksListView(LoginRequiredMixin,  PermissionRequiredMixin, generic.ListView):
  model = BookInstance
  template_name='all_borrowed_books.html'
  permission_required="catalog.can_mark_returned"

  def get_queryset(self):
    return (BookInstance.objects.filter(status='l').select_related('borrower'))
  

#TODO: IMPLEMENT THIS ONLY FOR LIBRIANS
def markReturned(request):
  pass

'''
Image handling --> 2 class
blog --> 
rest framework --> 2 class
6 class 
social media --> 
deployment --> 
'''
from .forms import RenewBookModelForm
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
@login_required
@permission_required("catalog.can_mark_returned")
def renew_book(request, pk):
  book_instance = get_object_or_404(BookInstance, pk=pk)
  if request.method == "POST":
    form = RenewBookModelForm(request.POST)

    if form.is_valid():
      book_instance.due_back = form.cleaned_data['renewal_date']
      book_instance.save()
      return HttpResponseRedirect(reverse('all-borrowed-books'))
  else:
    new_renewal_date = datetime.date.today() + datetime.timedelta(weeks=2)
    # DEfault value for the new dae
    form = RenewBookModelForm(initial={'renewal_date': new_renewal_date})
  context = {
    'form': form,
    'book_instance': book_instance,
  }
  return render(request, "book_renew_form.html",context)

class BookCreate(PermissionRequiredMixin, generic.CreateView):
  model = Book
  permission_required ="catalog.add_book"
  fields = ['title', 'author', 'description','genre','language','isbn' ]
  template_name = "book_form.html"
  initial = {'language':"english"}
  
  def get_success_url(self):
      return reverse('book-list')
  
class BookUpdate(PermissionRequiredMixin, generic.UpdateView):
  model = Book
  permission_required = 'catalog.change_book'
  fields = ['title', 'author', 'description','genre','language','isbn' ]
  template_name = 'book_form.html'


class BookDelete(PermissionRequiredMixin, generic.DeleteView):
  model = Book
  permission_required= "catalog.delete_book"
  template_name = "book_deleted.html"
  success_url = reverse_lazy("book-list")
  def form_valid(self, form):
      try:
        self.object.delete()
        return HttpResponseRedirect(self.success_url)
      except Exception as e:
        return HttpResponseRedirect(
          reverse('book-delete', kwargs={"pk": self.object.pk} )
        )

  



