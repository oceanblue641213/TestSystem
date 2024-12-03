from django.urls import path
from Application.Controllers import DISCOVERED_APIS

# 動態生成urlpatterns
urlpatterns = [
    path(f'{key}/', DISCOVERED_APIS[key], name=key) 
    for key in DISCOVERED_APIS.keys()
]