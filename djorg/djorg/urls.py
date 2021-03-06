"""djorg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.generic import TemplateView
# Instead of removing the csrf middleware:
from django.views.decorators.csrf import csrf_exempt

from rest_framework import routers
from notes.api import NoteViewSet

from graphene_django.views import GraphQLView
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register(r'notes', NoteViewSet)

urlpatterns = [
    path('', TemplateView.as_view(template_name='djorg_base.html')),

    path('admin/', admin.site.urls),
    path('bookmarks/', include('bookmark.urls')),
    path('notes/', include('notes.urls')),

    path('api/', include(router.urls)),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
    # Instead of removing the csrf middleware:
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),

    re_path(r'^api-token-auth/', views.obtain_auth_token)
]
