# pos_project/urls.py

from django.contrib import admin
from django.urls import path, include
# Import view login & logout bawaan Django
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('kasir.urls')),

    # --- TAMBAHKAN DUA BARIS INI ---
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]