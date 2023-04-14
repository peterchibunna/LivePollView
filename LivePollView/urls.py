"""LivePollView URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main.views import index, votes_view_modal, acme_challenge
from main.api import StateResource, VoteResource, PartyResource, ElectionResource
from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(StateResource())
v1_api.register(PartyResource())
v1_api.register(VoteResource())
v1_api.register(ElectionResource())

urlpatterns = [
    path('.well-known/acme-challenge/<str:codes>', acme_challenge),
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('api/', include(v1_api.urls)),
    path('get-votes', votes_view_modal, name='view-votes')
]
