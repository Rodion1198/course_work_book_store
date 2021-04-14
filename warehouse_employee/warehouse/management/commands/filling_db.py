import random

from django.core.management.base import BaseCommand
from faker import Faker
from warehouse.models import Author, Genre, PublishingHouse, Book, BookInstance


fake = Faker()


class Command(BaseCommand):
    '''Management coomand for filling db random values using Faker and random libs'''
    help = 'Generating random values for db filling'  # noqa: A003

    def handle(self, *args, **options):

        genre_list = []  # we will use only 15 genres here in db and store those genres in list
        for _ in range(1):
            genre = Genre(name=fake.word())  # creating Genre object
            genre.save()
            genre_list += [genre]

        for _ in range(100):

            author = Author(  # creating Author object
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                bio=fake.text(max_nb_chars=400),
                date_of_birth=fake.date(),
                date_of_death=fake.date()
            )
            author.save()

            publishing_house = PublishingHouse(  # creating PublishingHouse object
                name=fake.text(max_nb_chars=20),
            )
            publishing_house.save()

            for _ in range(13):
                a = random.randint(0, 9)

            for _ in range(random.randint(4, 10)):
                book = Book(  # creating Book object
                    title=fake.text(max_nb_chars=20),
                    publication_year=random.randint(1950, 2020),
                    publishing_house=publishing_house,
                    author=author,
                    price=round(random.uniform(50, 300), 2),
                    description=fake.text(max_nb_chars=400),
                    quantity=random.randint(1, 150),
                    slug=a
                )

                book.save()

                for iterr in random.sample(range(0, 14), k=3):
                    book.genre.add(genre_list[iterr])  # Adding genres to Book

                for _ in range(random.randint(1, 10)):
                    book_instance = BookInstance(book=book)    # creating BookInstance object
                    book_instance.save()
