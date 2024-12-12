from django.urls import path
from .views import ClassroomViewSet, StudentViewSet,ClassroomStudentsView

classroom_list = ClassroomViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

classroom_detail = ClassroomViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

student_list = StudentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

student_detail = StudentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

urlpatterns = [
    path('classrooms/', classroom_list, name='classroom-list'),
    path('classrooms/<int:pk>/', classroom_detail, name='classroom-detail'),
    path('students/', student_list, name='student-list'),
    path('students/<int:pk>/', student_detail, name='student-detail'),
    path('classrooms/<int:classroom_id>/students/', ClassroomStudentsView.as_view(), name='classroom_students'),
]
