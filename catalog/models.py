from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
# Create your models here.

class Genre(models.Model):
  name = models.CharField(max_length=100, help_text="Genre of your book", unique=True)

  def __str__(self):
    return self.name

  class Meta:
    constraints = [
      UniqueConstraint(Lower("name"), name="unique_genre_name",
      violation_error_message = "Genre is already present"),
    ]



class Book(models.Model):
  title = models.CharField('Title', max_length=100, help_text='Insert title of your book')
  author = models.ForeignKey('Author', on_delete=models.PROTECT)
  description = models.TextField(max_length=1000, help_text='Insert description of your book')
  genre = models.ManyToManyField(Genre, help_text="Enter the genres of the book")
  language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, blank=True)
  isbn = models.CharField('ISBN', max_length=100, help_text='Insert the isbn the book <a href="https://google.com" alt="isbn link"> </a>')

  def __str__(self):
    return self.title

  def display_genre(self):
    return list(self.genre.all()[:3])
  
  # display_genre.description = "genre"
import uuid
class BookInstance(models.Model):
  id = models.UUIDField( default=uuid.uuid4, primary_key=True, help_text='Unique id for the each book')
  book = models.ForeignKey(Book, on_delete=models.CASCADE)
  BOOK_STATUS_CHOICES = [
    ('m', 'Maintainance'),
    ('a', 'Available'),
    ('l', 'loan'),
    ('r', 'reserved')
  ]
  status = models.CharField(max_length=1, choices=BOOK_STATUS_CHOICES, help_text="Staus of the each book", default='m')
  due_back = models.DateField()
  #TODO: burrower = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)

class Author(models.Model):
  first_name = models.CharField(max_length=100, unique=True)
  last_name = models.CharField(max_length=100, unique=True)
  date_of_birth= models.DateField()
  date_of_death = models.DateField(null=True, blank=True)
  nationality = models.CharField(max_length=50)

  def __str__(self):
    return f"{self.last_name}  {self.first_name} "

  class Meta:
    unique_together = [['first_name','last_name']]
    ordering = ['last_name', 'first_name']



class Language(models.Model):
  language = models.CharField(max_length=100, help_text='Enter the language', null=True)

  def __str__(self):
    return self.language