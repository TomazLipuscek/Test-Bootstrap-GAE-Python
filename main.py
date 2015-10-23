#!/usr/bin/env python
import os
import jinja2
import webapp2
import datetime
from models import Sporocilo

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)

date = datetime.datetime.now()
napisicas={"datum": date}

class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
 
        
        self.render_template("index.html", napisicas)
    
class OmeniHandler(BaseHandler):
    def get(self):


        self.render_template("omeni.html", napisicas)
    
class ProjektiHandler(BaseHandler):
    def get(self):
        
        
        self.render_template("projekti.html", napisicas)

class BlogHandler(BaseHandler):
    def get(self):
        

        self.render_template("blog.html", napisicas)
    
class KontaktHandler(BaseHandler):
    def get(self):
        
        self.render_template("kontakt.html", napisicas)

class GuestbookHandler(BaseHandler):
    def get(self):
        
        self.render_template("guestbook.html", napisicas)
        
        
class RezultatHandler(BaseHandler):
    def post(self):
        imeM = self.request.get("ime")
        priimekM = self.request.get("priimek")
        emailM = self.request.get("email")
        sporociloM = self.request.get("sporociloV")
        sporocilo = Sporocilo(ime=imeM, priimek=priimekM, email=emailM, sporocilo=sporociloM)
        sporocilo.put()
        self.write("Posiljanje uspesno")
        
class SeznamSporocilHandler(BaseHandler):
    def get(self):
            seznam = Sporocilo.query(Sporocilo.izbrisan == False).fetch()
            params = {"seznam": seznam}
            self.render_template("seznam_sporocil.html", params=params)

class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        self.render_template("posamezno_sporocilo.html", params=params)

class UrediSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
            sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
            params = {"sporocilo": sporocilo}
            self.render_template("uredi_sporocilo.html", params=params)
    def post(self, sporocilo_id):
        ime = self.request.get("ime")
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        sporocilo.ime = ime
        sporocilo.put()
        self.redirect_to("seznam-sporocil")

class IzbrisiSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
            sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
            params = {"sporocilo": sporocilo}
            self.render_template("izbrisi_sporocilo.html", params=params)
    def post(self, sporocilo_id):
            sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
            sporocilo.izbrisan = True
            sporocilo.put()
            self.redirect_to("seznam-sporocil")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/omeni', OmeniHandler),
    webapp2.Route('/projekti', ProjektiHandler),
    webapp2.Route('/blog', BlogHandler),
    webapp2.Route('/kontakt', KontaktHandler),
    webapp2.Route('/guestbook', GuestbookHandler),    
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/seznam-sporocil', SeznamSporocilHandler, name="seznam-sporocil"),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>', PosameznoSporociloHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>/izbrisi', IzbrisiSporociloHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>/uredi', UrediSporociloHandler),
], debug=True)
