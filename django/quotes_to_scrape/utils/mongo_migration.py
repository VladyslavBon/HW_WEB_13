import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes_to_scrape.settings")
django.setup()

from mongoengine import connect
from mongoengine import Document
from mongoengine.fields import StringField, ReferenceField, ListField

from quotes.models import Quote as QuoteDB
from quotes.models import Author as AuthorDB
from quotes.models import Tag
from quotes_to_scrape.settings import env


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()
    meta = {"collection": "qoutes"}


connect(
    db=env("MONGO_DB_NAME"),
    host=env("MONGO_DATABASE_URL"),
)


authors = Author.objects()

for author in authors:
    AuthorDB.objects.get_or_create(
        fullname=author["fullname"],
        born_date=author["born_date"],
        born_location=author["born_location"],
        description=author["description"],
    )

quotes = Quote.objects()

for quote in quotes:
    tags = list()
    for tag in quote["tags"]:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)
    exists_quote = bool(len(QuoteDB.objects.filter(quote=quote["quote"])))
    if not exists_quote:
        author = Author.objects(id=quote.author.id).first()
        a = AuthorDB.objects.get(fullname=author["fullname"])
        q = QuoteDB.objects.create(quote=quote["quote"], author=a)

        for tag in tags:
            q.tags.add(tag)
