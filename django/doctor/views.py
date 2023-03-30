from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.core.mail import EmailMessage, message
from django.conf import settings
from django.contrib import messages
from .models import Appointment, report
from django.views.generic import ListView
import datetime
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.contrib.auth.models import User 
from django.contrib.auth  import authenticate, logout
from django.contrib.auth import login as loginned



class HomeTemplateView(TemplateView):
    template_name = "index.html"
    
    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        email = EmailMessage(
            subject= f"{name}, AlSamad's Patient",
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email]
        )
        email.send()
        return redirect("contact")

class AppointmentTemplateView(TemplateView):
    template_name = "appointment.html"

    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("fname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("request")

        appointment = Appointment.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=mobile,
            request=message,
        )

        appointment.save()

        messages.add_message(request, messages.SUCCESS, f"You've Successfully Requested For An Appointment. Our Team Will Shortly Get Back To You At {email}")
        return HttpResponseRedirect(request.path)

class ManageAppointmentTemplateView(ListView):
    template_name = "manage-appointments.html"
    model = Appointment
    context_object_name = "appointments"
    login_required = True
    paginate_by = 3


    def post(self, request):
        date = request.POST.get("date")
        appointment_id = request.POST.get("appointment-id")
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.accepted = True
        appointment.accepted_date = datetime.datetime.now()
        appointment.save()

        data = {
            "fname":appointment.first_name,
            "date":date,
        }

        message = get_template('email.html').render(data)
        email = EmailMessage(
            "About your appointment",
            message,
            settings.EMAIL_HOST_USER,
            [appointment.email],
        )
        email.content_subtype = "html"
        email.send()

        messages.add_message(request, messages.SUCCESS, f"You accepted the appointment of {appointment.first_name}")
        return HttpResponseRedirect(request.path)


    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = Appointment.objects.all()
        context.update({   
            "title":"Manage Appointments"
        })
        return context
    

# def onlineReporting(request):
#     query = request.GET.get('query')
#     if not query :
#         query = ""
#     # qq = report.objects.all()
#     allPosts = report.objects.filter(username__icontains=query)
#     params = {"allPosts": allPosts}
#     return render(request, "report.html",  params)
def onlineReporting(request):
    query = request.GET.get('query')
    if not query :
        query = ""
    # qq = report.objects.all()
    allPosts = report.objects.filter(username__icontains=query)
    params = {"allPosts": allPosts}
    return render(request, "report.html",  params)

def searchResults(request):
    query = request.GET.get('query')
    if not query :
        query = ""
    # qq = report.objects.all()
    allPosts = report.objects.filter(username__icontains=query)
    params = {"allPosts": allPosts, "query": query}
    return render(request, "search.html",  params)


def signUp(request):
    return render(request,"signup.html")

def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('signup')

        # check for errorneous input
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= username
        myuser.save()
        
        if myuser is not None:
            loginned(request, myuser)
            # messages.success(request, "Successfully Logged In")
            # messages.add_message(request, messages.SUCCESS, "Successfully Logged In")
            return redirect("home")

        else:
            return HttpResponse("404 - Not found")

def login(request):
    return render(request,"login.html")

def handleLogIn(request):
       if request.method=="POST":
        # Get the post parameters
        logUsername=request.POST['logUsername']
        logPass=request.POST['logPass']

        user=authenticate(username= logUsername, password= logPass)
        if user is not None:
            loginned(request, user)
            # messages.success(request, "Successfully Logged In")
            # messages.add_message(request, messages.SUCCESS, "Successfully Logged In")
            return redirect("home")
        else:
            # messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")
       
def handelLogout(request):
    logout(request)
    # messages.success(request, "Successfully logged out")
    return redirect('home')



def contact(request):
    return render(request,"contact.html")


def about(request):
    return render(request,"about.html")