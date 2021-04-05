# import requests
# from celery import shared_task
#
# from .models import Book


# @shared_task
# def sync_book():
#     url = 'http://127.0.0.1:8002/book.json/'
#     response = requests.get(url=url)
#
#     for count, book in enumerate(response):
#         if Book.objects.filter(id=book['id']).exists():
#             continue
#         else:
#             Book.objects.create(
#                 id=book['id'],
#                 title=book['title'],
#                 author=book['author'],
#                 publishing_house=book['publishing_house'],
#                 description=book['description'],
#                 slug=book['slug'],
#                 genre=book['genre'],
#                 price=book['price'],
#             )
#     print('Sync was successfully!')
