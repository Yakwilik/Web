from django.contrib import admin
from django.urls import path, include
from askme import views

urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.new_question, name="greet"),
    path('one_question/<int:i>', views.one_question, name="one_question"),
    path('registration/', views.registration, name="registration"),
    path('hot_question/', views.hot_question, name="hot"),
    path('auth/', views.authentication, name="authentication")

    # path('ask/', views.ask, name="ask"),
    # path('login/', views.login, name="login"),
    # path('registration/', views.registration, name="registration"),
    # path('settings/', views.settings, name="settings"),
    # path('hot/', views.hot, name="hot_question"),
    # path('tag/<str:tag>', views.tag_listing, name="tag"),
    # path('<int:i>/', views.question, name="question"),

]