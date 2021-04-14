from celery import shared_task

import requests

from .models import Author, Book, PublishingHouse, Genre


@shared_task
def sync_book():
    try:

        url = 'http://warehouse_employee:8002/genre/'
        response_genre = requests.get(url).json()
        while 1:
            for counter, data in enumerate(response_genre['results']):
                Genre.objects.get_or_create(
                    id=data['id'],
                    defaults={
                        'id': data['id'],
                        'name': data['name'],
                    }
                )

            if response_genre['next']:
                response_genre = requests.get(response_genre['next']).json()
            else:
                break

        url = 'http://warehouse_employee:8002/author/'
        response_author = requests.get(url).json()
        while 1:
            for counter, data in enumerate(response_author['results']):
                Author.objects.get_or_create(
                    id=data['id'],
                    defaults={
                        'id': data['id'],
                        'first_name': data['first_name'],
                        'last_name': data['last_name'],
                        'bio': data['bio'],
                        'date_of_birth': data['date_of_birth'],
                        'date_of_death': data['date_of_death'],
                    }
                )

            if response_author['next']:
                response_author = requests.get(response_author['next']).json()
            else:
                break

        url = 'http://warehouse_employee:8002/publishing-house/'
        response_publisher = requests.get(url).json()
        while 1:
            for counter, data in enumerate(response_publisher['results']):
                PublishingHouse.objects.get_or_create(
                    id=data['id'],
                    defaults={
                        'id': data['id'],
                        'name': data['name']
                    }
                )

            if response_publisher['next']:
                response_publisher = requests.get(response_publisher['next']).json()
            else:
                break

        url = 'http://warehouse_employee:8002/book'
        response = requests.get(url).json()
        while 1:
            for counter, data in enumerate(response['results']):
                book, created = Book.objects.get_or_create(
                    id=data['id'],
                    defaults={
                        'id': data['id'],
                        "title": data['title'],
                        "publication_year": data['publication_year'],
                        "image": data['image'],
                        "price": data['price'],
                        "description": data['description'],
                        'author': Author.objects.get(id=data['author']),
                        "publishing_house": PublishingHouse.objects.get(id=data['publishing_house']),
                        'quantity': data['quantity'],
                        'slug': data['slug'],
                    }
                )

                if not created:
                    book.title = data['title']
                    book.publication_year = data['publication_year']
                    book.image = data['image']
                    book.description = data['description']
                    book.price = data['price']
                    book.slug = data['slug']
                    book.author = Author.objects.get(id=data['author'])
                    book.publishing_house = PublishingHouse.objects.get(id=data['publishing_house']),
                    book.quantity = data['quantity']
                    book.save()

                for i in data['genre']:
                    genre = Genre.objects.get(id=i)
                    book.genre.add(genre)

            if response['next']:
                response = requests.get(response['next']).json()
            else:
                break
    except Exception as e:
        print('Synchronization of two databases failed. See exception:')  # noqa:T001
        print(e)  # noqa:T001


@shared_task
def send_order(first_name, last_name, phone_number, email, books):

    data = {
        "book": f"{books}",
        "email": f"{email}",
        "first_name": f"{first_name}",
        "last_name": f"{last_name}",
        "phone": f"{phone_number}",

    }
    requests.post(url='http://warehouse_employee:8002/order', data=data)
