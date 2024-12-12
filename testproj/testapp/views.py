from django.shortcuts import render,redirect
import requests
from django.conf import settings 
from django.contrib import messages

API_BASE_URL = getattr(settings, 'API_BASE_URL', 'http://127.0.0.1:8000/api/')

def classroom_table(request):
    try:
        response = requests.get(f'{API_BASE_URL}classrooms/')
        if response.status_code == 200:
            classrooms = response.json()
        else:
            classrooms = []  
    except Exception as e:
        print("inside except")
        classrooms = []  
        print(f"Error fetching classroom data: {e}")

    return render(request, 'classroom_table.html', {'classrooms': classrooms})

def add_classroom(request):
    original_form = True
    if request.method == "POST":
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        submit_button = request.POST.get('submit_button')
        classroom_id = request.POST.get('classroom_id')
        student_name = request.POST.get('student_name')
        student_age = request.POST.get('student_age')
        student_id = request.POST.get('student_id')
                
        data = {
            "name": name,
            "capacity": capacity,
        }
        if submit_button == "save":
            try:
                response = requests.post(f'{API_BASE_URL}classrooms/', json=data)
                if response.status_code == 201 or response.status_code == 200:
                    classroom_id = response.json().get('classroom_id')
                else:
                    print(f"Error: {response.json().get('detail', 'Failed to add classroom')}")
            except Exception as e:
                print(f"Error connecting to API: {e}")
            return redirect('classroom_edit', classroom_id=classroom_id)
        elif submit_button == "update":            
            try:
                response = requests.put(f'{API_BASE_URL}classrooms/{classroom_id}/', json=data)
                if response.status_code == 201 or response.status_code == 200:
                    classroom_id = response.json().get('classroom_id')
                    print("classroom_id",classroom_id)
                else:
                    print(f"Error: {response.json().get('detail', 'Failed to add classroom')}")
            except Exception as e:
                print(f"Error connecting to API: {e}")
            return redirect('classroom_edit', classroom_id=classroom_id)

        elif submit_button == "add_student":            
            data_student = {
                "name":student_name,
                "age":student_age,
                "classroom":classroom_id
            }
            try:
                response = requests.post(f'{API_BASE_URL}students/', json=data_student)
                if response.status_code == 201 or response.status_code == 200:
                    student_id = response.json().get('student_id')
                else:
                    print(f"Error: {response.json().get('detail', 'Failed to add classroom')}")
            except Exception as e:
                print(f"Error connecting to API: {e}")
            return redirect('classroom_edit', classroom_id=classroom_id)

        elif submit_button == "upd_student":
            data_student = {
                "name":student_name,
                "age":student_age,
                "classroom":classroom_id
            }
            try:
                response = requests.put(f'{API_BASE_URL}students/{str(student_id)}/', json=data_student)
                if response.status_code == 201 or response.status_code == 200:
                    print("student")
                else:
                    print(f"Error: {response.status_code}")
                    print("Response details:", response.json())
            except Exception as e:
                print(f"Error connecting to API: {e}")
            return redirect('classroom_edit', classroom_id=classroom_id)
    return render(request, 'add_classroom.html',{'original_form':original_form})


def edit_classroom(request, classroom_id):
    student_id = request.GET.get('student_id')
    original_form = False
    try:
        response = requests.get(f'{API_BASE_URL}classrooms/{classroom_id}/')
        if response.status_code == 200 or response.status_code == 201:
            classroom_data = response.json()
        else:
            print(f"Error: {response.json().get('detail', 'Failed to add classroom')}")
            return redirect('classroom-table')
    except Exception as e:
        print(f"Error connecting to API: {e}")
        return redirect('classroom-table')

    try:
        response = requests.get(f'{API_BASE_URL}classrooms/{classroom_id}/students/')
        if response.status_code == 200 or response.status_code == 201:
            students_data = response.json()  
        else:
            students_data = [] 
            print(f"Error fetching students for classroom {classroom_id}: {response.json()}")
    except Exception as e:
        students_data = []
        print(f"Error connecting to API: {e}")
    student_present = False
    student_data = []
    if student_id:
        student_present = True
        try:
            response = requests.get(f'{API_BASE_URL}students/{student_id}/')
            if response.status_code == 200 or response.status_code == 201:
                student_data = response.json()
            else:
                print(f"Error: {response.json().get('detail', 'Failed to add classroom')}")
                return redirect('classroom-table')
        except Exception as e:
            print(f"Error connecting to API: {e}")


    
    return render(request, 'add_classroom.html', {'student_id':student_id,'student_data':student_data,'student_present':student_present,'classroom_id':classroom_id,'classroom_data': classroom_data,'original_form':original_form,'students_data':students_data})



def delete_student(request,classroom_id,student_id):
    try:
        response = requests.delete(f'{API_BASE_URL}students/{student_id}/')
        if response.status_code == 204:  
            print("Student deleted successfully.")
        else:
            print(f"Error: Unable to delete student. {response.status_code} {response.text}")

    except Exception as e:
        print(f"Error connecting to API: {e}")

    return redirect('classroom_edit', classroom_id=classroom_id)


def delete_classroom(request,classroom_id):
    try:
        response = requests.delete(f'{API_BASE_URL}classrooms/{classroom_id}/')
        if response.status_code == 204:  
            print("classroom deleted successfully.")
        else:
            print(f"Error: Unable to delete classroom. {response.status_code} {response.text}")

    except Exception as e:
        print(f"Error connecting to API: {e}")

    return redirect('classroom_table')