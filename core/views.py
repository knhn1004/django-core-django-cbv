from django.views.generic import View
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect


def about_usredirect_view(req):
    return HttpResponseRedirect('/about/')


def about_us_view(req):
    return render(req, 'about.html', {})


# class AboutUsView(View):
#    def get(self, req, *args, **kwargs):
#        return render(req, 'about.html', {})

class AboutUsView(TemplateView):
    template_name = 'about.html'
