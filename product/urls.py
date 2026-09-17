from django.urls import path
from .routes import router
urlpatterns = [
    
]+router.urls