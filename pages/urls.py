from django.urls import path
from .views import (
    result_list,
    pu_create_view,
    PuDoneView,
    lga_result_list,
)

urlpatterns = [
    path("", result_list, name="pu_result"),
    path("add-pu", pu_create_view, name="pu_create"),
    path("add-pu-done", PuDoneView.as_view(), name="pu_create_done"),
    path("lga/<int:id>", lga_result_list, name="lga_result"),
]
