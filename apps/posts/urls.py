from django.urls import path

from .views import CreatePostView

urlpatterns = [

    path(
        "",
        CreatePostView.as_view(),
        name="create-post",
    ),

]