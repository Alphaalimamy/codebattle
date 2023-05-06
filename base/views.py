from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from PIL import Image
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import User, Event, Submission
from .forms import SubmissionForm, CustomUserCreateForm, UserForm
# Create your views here.
from datetime import datetime, timedelta

def login_page(request):
    page = "login"
    
    if request.method == "POST":
        #email = request.POST['email']
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(email=email, password=password)
    
        if user is not None:
            login(request, user)
            messages.info(request, 'You have succesfully logged in.')
            return redirect('home')
        else:
            messages.error(request, "Email or password is incorrect")
            return redirect('login')
        
    context = {"page": page}
    return render(request, 'login_register.html', context)
 
def logout_user(request):
     logout(request)
     messages.info(request, "User logged out")
     return redirect("login")
     
def register_page(request):
    
    form = CustomUserCreateForm()
    
    if request.method == "POST":
        form = CustomUserCreateForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request, "User created successfully")
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")
    
    page = "register"
    context = {"page": page, "form": form}
    return render(request, 'login_register.html', context)   
    
def home_page(request):
    limit = request.GET.get('limit')
    if limit == None:
        limit = 20
    limit = int(limit)
    users = User.objects.filter(hackathon_participants=True)
    count = users.count()
    
    page = request.GET.get('page')
    paginator = Paginator(users, 20)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        users = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        users = paginator.page(page)


    pages = list(range(1, (paginator.num_pages + 1)))
 
    events = Event.objects.all()
    context = {'users':users, 'events':events, 'count':count, 'paginator':paginator, 'pages':pages}
    return render(request, "home.html", context)

def user_page(request, pk):
    user = User.objects.get(id=pk)
    context = {"user": user}
    return render(request, "profile.html", context)

@login_required(login_url="login")
def account_page(request):
    user =request.user
    
    
    context ={"user": user}
    return render(request, "account.html",context)

@login_required(login_url='/login')
def edit_account(request):

    form = UserForm(instance=request.user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES,  instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('account')

    context = {'form':form}
    return render(request, 'user_form.html', context)

@login_required(login_url='/login')
def change_password(request):
    
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 == password2:
            new_password = make_password(password1)
            request.user.password = new_password
            request.user.save()
            messages.success(request, 'You have succesfully reset your password')
            return redirect('account')

    return render(request, 'change_password.html')



def event_page(request, pk):
    event = Event.objects.get(id=pk)
    
    present = datetime.now()
    
    registered = False
    submitted = False
    
    if request.user.is_authenticated:
        registered = request.user.events.filter(id=event.id).exists()
        submitted = Submission.objects.filter(participant=request.user, event=event).exists()
    context = {'event':event, 'registered':registered, 'submitted':submitted}
    return render(request, 'event.html', context)


@login_required(login_url="/login")
def register_confirmation(request, pk):
    event = Event.objects.get(id=pk)
    
    if request.method == "POST":
        event.participants.add(request.user)
        return redirect("event", pk=event.id)
    
    context ={"event": event}
    return render(request, "event_confirmation.html", context)


@login_required(login_url="/login")
def project_submission(request, pk):
    event = Event.objects.get(id=pk)
    
    form = SubmissionForm()
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        submission = form.save(commit=False)
        
        if form.is_valid():
            submission.participant = request.user
            submission.event = event
            submission.save()
            return redirect("account")
            
            
    context ={"event": event, "form": form}
    return render(request, "submit_form.html", context)


# Add owner authentication
# @login_required(login_url='/login')
# def update_submission(request, pk):
#     submission = Submission.objects.get(id=pk)
#     event = submission.event
#     form = SubmissionForm(instance=submission)
    
#     if request.user != submission.user:
#         return HttpResponse("You are not allowed to be here.")
        
#     if request.method == 'POST':
#         form = SubmissionForm(request.POST,instance=submission)
#         if form.is_valid():
#             form.save()
#             return redirect('account')
        
#     context = {'form': form, 'event': event}
#     return render(request, 'submit_form.html', context)

@login_required(login_url='/login')
def update_submission(request, pk):
    submission = Submission.objects.get(id=pk)

    if request.user != submission.participant:
        return HttpResponse('You cant be here!!!!')

    event = submission.event
    form = SubmissionForm(instance=submission)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form, 'event':event}
    return render(request, 'submit_form.html', context)
