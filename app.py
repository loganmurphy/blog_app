import os
import tornado.ioloop
import tornado.web
import tornado.log

from jinja2 import \
  Environment, PackageLoader, select_autoescape
from models import BlogPost, Author, Comment

ENV = Environment(
  loader=PackageLoader('blog', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)

class TemplateHandler(tornado.web.RequestHandler):
  def render_template (self, tpl, context):
      template = ENV.get_template(tpl)
      self.write(template.render(**context))

class MainHandler(TemplateHandler):
  def get(self):
    posts = BlogPost.select().order_by(
      BlogPost.created.desc())
    self.render_template('home.html', {'posts': posts})

class PostHandler(TemplateHandler):
  def get(self, slug):
      post = BlogPost.select().\
        where(BlogPost.slug == slug).get()
      self.render_template('post.html', {'post': post})

class CommentHandler(TemplateHandler):
  def post (self, slug):
    comment = self.get_body_argument('comment')
    post = BlogPost.select().where(BlogPost.slug == slug).get()
    Comment.create(BlogPost=post.id, comment=self.get_body_argument('comment'))
    self.redirect('/post/' + slug)

class AuthorArticleHandler(TemplateHandler):
  def get (self, id):

    author = Author.select().where(Author.id == id)
    posts =  BlogPost.select().where(BlogPost.author_id == author)
    self.render_template('author_articles.html', {'posts': posts})

class AuthorHandler(TemplateHandler):
  def get (self, authors):
    authors = Author.select()
    self.render_template('authors.html', {'authors': authors})

def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/post/(.*)/comment", CommentHandler),
    (r"/post/(.*)", PostHandler),
    (r"/authors/(.*)", AuthorHandler),
    (r"/author/(.*)", AuthorArticleHandler),
    (r"/static/(.*)",
      tornado.web.StaticFileHandler, {'path': 'static'}),
  ], autoreload=True)

if __name__ == '__main__':
  tornado.log.enable_pretty_logging()
  app = make_app()
  app.listen(int(os.environ.get('PORT', '8080')))
  print("All systems are go!")
  tornado.ioloop.IOLoop.current().start()
