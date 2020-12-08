from django.views.generic.base import TemplateView


class Home(TemplateView):
    login_url = 'login'
    template_name = 'home.html'

