from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from testapp.models import Classroom, Student
from .serializers import ClassroomSerializer, StudentSerializer

class ClassroomViewSet(viewsets.ViewSet):
    @swagger_auto_schema(operation_description="Get all classrooms")
    def list(self, request):
        classrooms = Classroom.objects.all()
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Get a classroom by its ID")
    def retrieve(self, request, pk=None):
        try:
            classroom = Classroom.objects.get(pk=pk)
        except Classroom.DoesNotExist:
            return Response({"error": "Classroom not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClassroomSerializer(classroom)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the classroom'),
                'capacity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Capacity of the classroom'),
            },
            required=['name', 'capacity'],
        )
    )
    def create(self, request):
        serializer = ClassroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update an existing classroom",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the classroom'),
                'capacity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Capacity of the classroom'),
            },
            required=['name', 'capacity'],  # Mark required fields
        ),
        responses={
            200: openapi.Response('Successfully updated the classroom', ClassroomSerializer),
            400: 'Bad Request',
            404: 'Not Found',
        }
    )
    def update(self, request, pk=None):
        try:
            classroom = Classroom.objects.get(pk=pk)
        except Classroom.DoesNotExist:
            return Response({"error": "Classroom not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClassroomSerializer(classroom, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Delete a classroom by its ID")
    def destroy(self, request, pk=None):
        try:
            classroom = Classroom.objects.get(pk=pk)
            classroom.delete()
            return Response({"message": "Classroom deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Classroom.DoesNotExist:
            return Response({"error": "Classroom not found"}, status=status.HTTP_404_NOT_FOUND)


class StudentViewSet(viewsets.ViewSet):
    @swagger_auto_schema(operation_description="Get all students")
    def list(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Get a student by their ID")
    def retrieve(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new student",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the student'),
                'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='Age of the student'),
                'classroom': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the classroom the student belongs to'),
            },
            required=['name', 'age', 'classroom'],  # Specify required fields
        ),
        responses={
            201: openapi.Response('Student created successfully', StudentSerializer),
            400: 'Bad Request',
        }
    )
    def create(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update an existing student",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Updated name of the student'),
                'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated age of the student'),
                'classroom': openapi.Schema(type=openapi.TYPE_INTEGER, description='Updated classroom ID for the student'),
            },
            required=['name', 'age', 'classroom'],  # Specify required fields
        ),
        responses={
            200: openapi.Response('Student updated successfully', StudentSerializer),
            400: 'Bad Request',
            404: 'Student not found',
        }
    )
    def update(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Delete a student by their ID")
    def destroy(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
            student.delete()
            return Response({"message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)


class ClassroomStudentsView(APIView):
    @swagger_auto_schema(operation_description="Get all students in a classroom by classroom ID")
    def get(self, request, classroom_id):
        try:
            classroom = Classroom.objects.get(classroom_id=classroom_id)
            students = classroom.students.all()
            serializer = StudentSerializer(students, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Classroom.DoesNotExist:
            return Response({"detail": "Classroom not found."}, status=status.HTTP_404_NOT_FOUND)
