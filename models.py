import datetime
import os

import peewee
from playhouse.db_url import connect
import markdown2

DB = connect(
    os.environ.get(
    'DATABASE_URL',
    'postgres://localhost:5432/blog'
    )
)

class BaseModel (peewee.Model):
    class Meta:
        database = DB

class Author (BaseModel):
    name = peewee.CharField(max_length=60)
    twitter = peewee.CharField(max_length=60)
    def __str__ (self):
      return self.name

class BlogPost (BaseModel):
  author = peewee.ForeignKeyField(Author, null=True)
  title = peewee.CharField(max_length=60)
  slug = peewee.CharField(max_length=50, unique=True)
  body = peewee.TextField()
  created = peewee.DateTimeField(
    default=datetime.datetime.utcnow)
  def html (self):
      return markdown2.markdown(self.body)
  def __str__ (self):
    return self.title

class Comment(BaseModel):
  BlogPost = peewee.ForeignKeyField(BlogPost, null=False)
  comment = peewee.CharField(max_length=500)

# post = BlogPost.create(
#     author='Logan2'
#     title='TEST',
#     slug='TEST',
#     body='THIS IS A TEST!'
# )

#
# me = Author.create(name='Logan', twitter='LDAWG5000')
# post.save()
# post = BlogPost.select().where(BlogPost.title == 'How Robots Are Taking Over')
