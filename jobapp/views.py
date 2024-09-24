
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, JobApplication
from django.contrib import messages
from authapp.models import *
from jobapp.models import*
from django.http import HttpResponseBadRequest
from django.core.paginator import Paginator

# Existing views...

@login_required
def apply_job(request, job_id):
    # Retrieve the job object using the job_id
    job = get_object_or_404(Job, id=job_id)

    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Get the cover letter from the submitted form data
        cover_letter = request.POST.get('cover_letter', '')

        # Get the uploaded CV file
        cv = request.FILES.get('cv')

        # Create a new JobApplication object with the submitted data
        JobApplication.objects.create(
            job=job,
            employee=request.user,
            cover_letter=cover_letter,
            cv=cv
        )

        # Display a success message to the user
        messages.success(request, 'Your application has been submitted successfully.')

        # Redirect the user to the dashboard or a success page
        return redirect('user_dashboard')

    # Render the 'apply_job.html' template, passing the job object
    return render(request, 'apply_job.html', {'job': job})





def index(request):
   
    return render(request, 'index.html' )



def companies(request):
    # Get filter criteria from GET parameters
    location_filter = request.GET.get('location')
    industry_filter = request.GET.get('industry')
    company_type_filter = request.GET.get('company_type')
    
    # Build the query with filters
    companies = Company.objects.all()
    
    if location_filter:
        companies = companies.filter(location=location_filter)
    
    if industry_filter:
        companies = companies.filter(industry=industry_filter)
    
    if company_type_filter:
        companies = companies.filter(company_type=company_type_filter)
    
    # Paginate the filtered query
    paginator = Paginator(companies, 8)
    page_number = request.GET.get('page')
    companiesData = paginator.get_page(page_number)
    
    return render(request, 'companies.html', {
        'companies': companiesData,
        'location_filter': location_filter,
        'industry_filter': industry_filter,
        'company_type_filter': company_type_filter
    })


def services(request):
   
    return render(request, 'services.html' )



def dashboard(request):
    if request.user.is_authenticated and request.user.is_company:
        try:
            current_company = Company.objects.get(user=request.user)
            jobs = Job.objects.filter(company_name=current_company)
        except Company.DoesNotExist:
            jobs = []
    else:
        jobs = []

    return render(request, 'dashboard.html', {'jobs': jobs})



def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'job_detail.html', {'job': job})



def job_delete(request, id):
    job = get_object_or_404(Job, id=id)  # Get the job to delete

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('dashboard')

    return render(request, 'confirm_delete.html', {'job': job})


def view_job(request, id):
    job = get_object_or_404(Job, id=id)
    return render(request, 'view_job.html', {'job': job})

def user_view_job(request, id):
    job = get_object_or_404(Job, id=id)
    return render(request, 'user_view_job.html', {'job': job})



def job_edit(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        job.title = request.POST.get('title', job.title)
        job.company_name = request.POST.get('company_name', job.company_name)
        job.posted_date = request.POST.get('posted_date', job.posted_date)
        job.job_type = request.POST.get('job_type', job.job_type)
        job.description = request.POST.get('description', job.description)
        job.location = request.POST.get('location', job.location)
        job.workplace_type = request.POST.get('workplace_type', job.workplace_type)
        job.salary = request.POST.get('salary', job.salary)
        job.job_category = request.POST.get('job_category', job.job_category)  # Add this line

        try:
            job.save()
        except Exception as e:
            # Handle exceptions, e.g., log the error
            return HttpResponseBadRequest("An error occurred while saving the job.")
        
        return redirect('dashboard')  # Adjust this to your actual job list page URL name

    return render(request, 'edit_job.html', {'job': job})

@login_required
def upload_cv(request):
    if request.method == 'POST':
        if 'cv' in request.FILES:
            cv_file = request.FILES['cv']
            try:
                employee = Employee.objects.get(user=request.user)
                employee.cv.save(cv_file.name, cv_file)
                employee.save()
                messages.success(request, 'Your CV has been uploaded successfully!')
            except Employee.DoesNotExist:
                messages.error(request, 'Employee profile does not exist.')
        else:
            messages.error(request, 'No file was uploaded.')
        return redirect('dashboard')
    
    return render(request, 'upload_cv.html')


def view_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    return render(request, 'view_employee.html', {'employee': employee})

def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully.')
        return redirect('admin_dashboard')
    return render(request, 'delete_employee.html', {'employee': employee})




@login_required
def view_applications(request):
    # Fetch applications for the current user
    applications = JobApplication.objects.all()

    # Render the page with the fetched applications
    return render(request, 'view_applications.html', {'applications': applications})



def view_application_detail(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    return render(request, 'application_detail.html', {'application': application})


def add_job(request):
    if request.method == 'POST':
        # Get the company associated with the logged-in user
        try:
            company = Company.objects.get(user=request.user)
        except Company.DoesNotExist:
            messages.error(request, 'No company profile found. Please create one first.')
            return redirect('register_company')

        # Proceed with creating the job
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        workplace_type = request.POST.get('workplace_type')
        salary = request.POST.get('salary')
        posted_date = request.POST.get('posted_date')
        job_type = request.POST.get('job_type')
        job_category = request.POST.get('job_category')  # Get the job category from the form

        job = Job.objects.create(
            title=title,
            description=description,
            location=location,
            workplace_type=workplace_type,
            salary=salary,
            company_name=company.name,
            posted_date=posted_date,
            job_type=job_type,
            job_category=job_category  # Save the job category
        )
        job.save()

        return redirect('dashboard')

    return render(request, 'add_job.html')




def job_search(request):
    query = request.GET.get('q')
    location = request.GET.get('location')

    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(title__icontains=query)
    
    if location:
        jobs = jobs.filter(location__icontains=location)

    return render(request, 'your_template.html', {'jobs': jobs})




def jobs_by_category(request, category):
    # Replace spaces with hyphens to match database entries
    category = category.replace(' ', '-')
    jobs = Job.objects.filter(job_category=category)
    return render(request, 'jobs_by_category.html', {'jobs': jobs, 'category': category})




def viewjob(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'viewjob.html', {'job': job})



def jobs(request):
    jobs = Job.objects.all()

    # Filter by job type
    job_type = request.GET.getlist('job_type')
    if job_type:
        jobs = jobs.filter(job_type__in=job_type)

    # Filter by job category
    job_category = request.GET.getlist('job_category')
    if job_category:
        jobs = jobs.filter(job_category__in=job_category)

    # Filter by career level
    career_level = request.GET.getlist('career_level')
    if career_level:
        if 'Fresher' in career_level:
            jobs = jobs.filter(fresher=True)
        if 'Experienced' in career_level:
            jobs = jobs.filter(experienced=True)

    # Filter by education level
    education_level = request.GET.getlist('education_level')
    if education_level:
        jobs = jobs.filter(education_level__in=education_level)

    # Filter by years of experience
    experience_years = request.GET.getlist('experience_years')
    if experience_years:
        jobs = jobs.filter(years_of_experience__in=experience_years)

    paginator = Paginator(jobs, 4)
    page_number = request.GET.get('page')
    jobsData = paginator.get_page(page_number)
    
    return render(request, 'jobs.html', {'jobs': jobsData})