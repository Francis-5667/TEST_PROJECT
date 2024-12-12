from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.classroom_table, name='classroom_table'),
    path('classroom_new/', views.add_classroom, name='classroom_new'),
    path('classroom_edit/<int:classroom_id>',views.edit_classroom, name="classroom_edit"),
    path('delete_student/<int:classroom_id>/<int:student_id>',views.delete_student, name="delete_student"),
    path('delete_classroom/<int:classroom_id>',views.delete_classroom, name="delete_classroom"),
]