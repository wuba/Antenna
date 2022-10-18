"""antenna URL Configuration

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
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.static import serve
from django.contrib import admin
from django.urls import path, include, re_path

import modules.message.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("modules.account.urls")),
    path("api/v1/templates/", include("modules.template.urls")),
    path("api/v1/tasks/", include("modules.task.urls")),
    path("api/v1/messages/", include("modules.message.urls")),
    path("api/v1/openapi/", include("modules.api.urls")),
    path("api/v1/configs/", include("modules.config.urls")),
    re_path(
        r"^(js/.*|css/.*|img/.*|logo.png)$", serve, {"document_root": settings.BASE_DIR / "static"}
    ),
    re_path(".*", modules.message.views.index, name='index'),
]
