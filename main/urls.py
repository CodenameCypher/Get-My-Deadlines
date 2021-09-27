from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='home'),
    path('deadlines/', get_deadlines, name='deadlines'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('faq/', faq, name='faq'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
