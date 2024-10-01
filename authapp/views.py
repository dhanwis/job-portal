import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import*
from django.contrib import messages
from  jobapp.models import*
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model

from django.db import IntegrityError


def register_company(request):
    if request.method == 'POST':
        try:
            # Extract data from POST request
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            mailing_address = request.POST.get('mailing_address')
            pin_code = request.POST.get('pin_code')
            industry = request.POST.get('industry')
            location = request.POST.get('location')  # Extract location data
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            website = request.POST.get('website', '')  # Optional field
            description = request.POST.get('description', '')  # Optional field

            # Validate data
            if not all([name, email, phone_number, mailing_address , pin_code,  industry, location, password, confirm_password]):
                messages.error(request, 'All fields are required.')
                return render(request, 'register_company.html')

            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'register_company.html')

            # Check if username already exists
            User = get_user_model()
            if User.objects.filter(username=name).exists():
                messages.error(request, 'Username already exists. Please choose a different username.')
                return render(request, 'register_company.html')

            # Create a new User instance
            user = User.objects.create_user(
                username=name,
                email=email,
                password=password,
                name=name,
                phone_number=phone_number,
                is_company=True
            )

            # Create a new Company instance linked to the User
            company = Company.objects.create(
                user=user,
                mailing_address=mailing_address,
                pin_code=pin_code,
                industry=industry,
                location=location,  # Include location in the company creation
                website=website,
                description=description,
                name=name  # Ensure this field is included
            )

            # Success message and redirect
            messages.success(request, 'Company registered successfully.')
            return redirect('mainlogin')  # Replace with your URL name for the success page

        except KeyError as e:
            # Handle missing POST data
            messages.error(request, f'Missing field: {e.args[0]}')
            return render(request, 'register_company.html')
        except IntegrityError as e:
            # Handle integrity errors (e.g., unique constraints)
            messages.error(request, str(e))
            return render(request, 'register_company.html')
        except Exception as e:
            # Handle other exceptions
            messages.error(request, str(e))
            return render(request, 'register_company.html')

    # Render a registration form (GET request)
    return render(request, 'register_company.html')




def user_register(request):
    if request.method == 'POST':
        # Extract data from POST request
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        gender = request.POST['gender']
        password = request.POST['password']
        education_qualifications = request.POST['education_qualifications']
        university = request.POST['university']
        pass_out_year = request.POST['pass_out_year']
        date_of_birth = request.POST['date_of_birth']
        company_name = request.POST['company_name']
        years_of_experience = request.POST['years_of_experience']
        designation = request.POST['designation']
        user_type = request.POST['user_type']
        cv = request.FILES.get('cv', None)

        try:
            User = get_user_model()
            user = User.objects.create_user(username=name, email=email, password=password, phone_number=phone_number, is_employee=True)

            # Determine user type and set corresponding attributes
            if user_type == 'fresher':
                college_name = request.POST['college_name']
                university = request.POST['university']
                pass_out_year = request.POST['pass_out_year']

                # Create a new Employee instance for fresher
                new_user = Employee.objects.create(
                    user=user,
                    gender=gender,
                    college_name=college_name,
                    university=university,
                    pass_out_year=pass_out_year,
                    date_of_birth=date_of_birth,
                    education_qualifications=education_qualifications,
                    cv=cv,
                    is_Fresher=True
                )

            elif user_type == 'experienced':
                company_name = request.POST['company_name']
                years_of_experience = request.POST['years_of_experience']
                designation = request.POST['designation']

                # Create a new Employee instance for experienced user
                new_user = Employee.objects.create(
                    user=user,
                    gender=gender,
                    company_name=company_name,
                    years_of_experience=years_of_experience,
                    designation=designation,
                    date_of_birth=date_of_birth,
                    education_qualifications=education_qualifications,
                    cv=cv,
                    is_Experienced=True
                )

            # Save the new user
            new_user.save()

            # Authenticate and login the user
            user = authenticate(request, username=name, password=password)
            if user is not None:
                login(request, user)
                return redirect('mainlogin')  # Redirect to index page after successful registration and login
            else:
                messages.error(request, 'Authentication failed. Please try logging in manually.')

        except Exception as e:
            # Handle the error gracefully, maybe render the registration form again with error messages
            messages.error(request, f'Error: {str(e)}')
            return render(request, 'user_register.html')

    # Render a registration form (GET request)
    return render(request, 'user_register.html')



def mainlogin(request):
    return render(request, 'mainlogin.html' ) 



   

def user_dashboard(request):
    jobs = Job.objects.all() 
    
    
    return render(request, 'user_dashboard.html',{'jobs': jobs} ) 






def dashboard_admin(request):
    companies = Company.objects.all()
    employees = Employee.objects.all()  # Query all employees

    context = {
        'companies': companies,
        'employees': employees,
    }
    return render(request, 'dashboard_admin.html', context)



def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        employee.user.username = request.POST.get('username', employee.user.username)
        employee.is_Fresher = 'is_Fresher' in request.POST
        employee.is_Experienced = 'is_Experienced' in request.POST
        employee.save()
        messages.success(request, 'User updated successfully.')
        return redirect('dashboard_admin')
    return render(request, 'edit_user.html', {'employee': employee})

def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('dashboard_admin')
    return render(request, 'confirm_delete_user.html', {'employee': employee})




def view_company(request, id):
    company = get_object_or_404(Company, id=id)
    template_path = os.path.join(settings.BASE_DIR, 'jobapp/templates/view_company.html')
    print(f"Template path: {template_path}")  # Check this path in your console
    return render(request, 'view_company.html', {'company': company})


def edit_company(request, id):
    company = get_object_or_404(Company, id=id)
    
    if request.method == 'POST':
        company.mailing_address = request.POST.get('mailing_address')
        company.pin_code = request.POST.get('pin_code')
        company.industry = request.POST.get('industry')
        company.location = request.POST.get('location')  # Update location
        company.website = request.POST.get('website')
        company.description = request.POST.get('description')
        company.save()
        messages.success(request, 'Company details updated successfully.')
        return redirect('view_company', id=company.id)

    return render(request, 'edit_company.html', {'company': company})


def delete_company(request, id):
    company = get_object_or_404(Company, id=id)
    if request.method == 'POST':
        company.delete()
        messages.success(request, 'Company successfully deleted.')
        return redirect('dashboard_admin')




def logout_user(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        logout(request)
    return redirect('mainlogin')



def logout_superuser(request):
    logout(request)
    return redirect('mainlogin') 





def login_company(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            messages.error(request, 'Username does not exist.')
            return render(request, 'login_company.html')

        if user.check_password(password):
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, 'Login Successful')
                return redirect('index')
            else:
                messages.error(request, 'Invalid login credentials.')
        else:
            messages.error(request, 'Incorrect password.')

        return render(request, 'login_company.html')

    return render(request, 'login_company.html')





def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            messages.error(request, 'Username does not exist.')
            return render(request, 'user_login.html')

        if user.check_password(password):
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, 'Login Successful')
                return redirect('index')
            else:
                messages.error(request, 'Invalid login credentials.')
        else:
            messages.error(request, 'Incorrect password.')

        return render(request, 'user_login.html')

    return render(request, 'user_login.html')





