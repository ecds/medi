"""medi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('date_test', views.date_test, name='date_test'),
    path('men_test', views.men_test, name='men_test'),
    path('women_test', views.women_test, name='women_test'),
    url(
        'woman-autocomplete/$',
        views.WomanAutocomplete.as_view(),
        name='woman-autocomplete',
    ),
    url(
        'familymember-autocomplete/$',
        views.FamilyMemberAutocomplete.as_view(),
        name='familymember-autocomplete',
    ),
    url(
        'relatedother-autocomplete/$',
        views.OtherAutocomplete.as_view(),
        name='relatedother-autocomplete',
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.autodiscover()
admin.site.enable_nav_sidebar = False
admin.site.site_header = 'Singlewomen in the medieval Mediterranean'
