from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView,FormView
from django.views.generic import ListView,DetailView
from .models import User
from project.models import *
from .forms import ManagerRegisterForm,DeveloperRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView,LogoutView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django import forms

# Create your views here.
class ManagerRegisterView(CreateView):
    #model = User
    form_class = ManagerRegisterForm
    template_name = 'user/manager_register.html'
    success_url = '/user/manager/dashboard'
    
    
    # def get_context_data(self, **kwargs):
    #     kwargs['user_type'] = 'manager'
    #     return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        #response = super().form_valid(form)
        user = form.save()
        if user is not None: 
            subject = "Welcome"
            message = "welcome User!"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            login(self.request,user)
        return super(ManagerRegisterView,self).form_valid(form)
        #return response
    
    # def form_valid(self,form):
    #     #email = form.cleaned_data.get('email')
        
    #     user = form.save()
    #     login(self.request,user)
    #     return super().form_valid(form)
        

class DeveloperRegisterView(CreateView):
    #model = User
    form_class = DeveloperRegistrationForm
    template_name = 'user/developer_register.html'
    success_url = '/user/dashboard' 
    
    # def get_context_data(self, **kwargs):
    #     kwargs['user_type'] = 'developer'
    #     return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        #response = super().form_valid(form)
        user = form.save()
        if user is not None: 
            subject = "Welcome"
            message = "welcome User!"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            login(self.request,user)
        return super(DeveloperRegisterView,self).form_valid(form)
    



class UserLoginView(LoginView):
    template_name = 'user/login.html'
    #success_url = "/"
    
    def get_redirect_url(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_manager1:
                return '/user/manager/dashboard/'
            else:
                return '/user/developer/dashboard/'
        
    # def form_valid(self, form):
    #     response = super().form_valid(form)
        
    #     subject = "You have logged in"
    #     message = "Thank you for login"
    #     from_email = settings.EMAIL_HOST_USER
    #     recipient_list = [self.request.user.email]
    #     send_mail(subject, message, from_email, recipient_list)
        
    #     return response
        
        
        
class UserLogoutView(LogoutView):
    template_name = "user/logout.html"
    
    
class SignUpForm(forms.Form):
    CHOICES = (
        ('manager', 'Manager'),
        ('developer', 'Developer'),
    )
    account_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    

class SignUpView(FormView):
    template_name = 'user/signup.html'
    form_class = SignUpForm
    

    def form_valid(self, form):
        account_type = form.cleaned_data['account_type']
        if account_type == 'manager':
            # Redirect to manager registration form
            return redirect('managerregister')
        elif account_type == 'developer':
            # Redirect to developer registration form
        
            return redirect('developerregister')
        else:
            return redirect('signup')
    

class ManagerDashboardView(ListView):            

    def get(self, request, *args, **kwargs):
        project = Project.objects.all().values()
        project_count = Project.objects.count()
        module_count = ProjectModule.objects.count()
        task_count = Task.objects.count()
        
        return render(request, 'user/manager_dashboard.html',{
            'projects':project,
            'labels':self.labels,
            'data':self.data,
            # 'labels1':self.labels1,
            # 'data1':self.data1,
            'project_count': project_count,
            'module_count': module_count,
            'task_count': task_count,
        })

    template_name = 'user/manager_dashboard.html'

    labels=[]
    data =[]
    # labels1=[]
    # data1=[]
    project = Project.objects.all().values_list('title',flat=True)
    time = Project.objects.all().values_list('estimatedHrs',flat=True)
    # project1=Project.objects.all().values_list('technology',flat=True)
    # startdate = Project.objects.all().values_list('estimatedHours',flat=True)
    
    for i in project:
        labels.append(i)
    for i in time:
        data.append(i)
    # for i in project1:
    #     labels1.append(i)
    # for i in startdate:
    #     data1.append(i)

# @login_required   
class DeveloperDashBoardView(ListView):
    model = User
    def get(self, request, *args, **kwargs):
        user = request.user
        user_tasks = user.usertask_set.all()
        
        completed_task = Task.objects.filter(status="Completed").count()
        progress_task = Task.objects.filter(status="inProgress").count()
        pending_task = Task.objects.filter(status="Pending").count()
        task_count = Task.objects.count()
        
        high_priority = Task.objects.filter(priority='high').count()
        low_priority = Task.objects.filter(priority='low').count()
        normal_priority = Task.objects.filter(priority='medium').count()
        
        return render(request,'user/developer_dashboard.html',{
            'completed_task':completed_task,
            'progress_task':progress_task,
            'pending_task':pending_task,
            'task_count':task_count,
            'high_priority':high_priority,
            'low_priority':low_priority,
            'normal_priority':normal_priority,
            'user_tasks':user_tasks})
    
template_name = 'user/developer_dashboard.html'
    
class TaskDetailView(DetailView):
    model = Task
    template_name = 'user/task_detail.html'
    context_object_name = 'task_detail'  
    
    def get(self, request, *args, **kwargs):
        task = Task.objects.filter(project_id=self.kwargs['pk'])
        user = request.user
        print(self.kwargs['pk'])
        task1 = UserTask.objects.filter(user = request.user,taskid_id=self.kwargs['pk']).values('id','taskid_id__status','taskid_id__project__title','taskid_id__project__startdate','taskid_id__project__completitiondate','taskid_id__priority','taskid_id__title','taskid_id__desc')
        print(task1)
        task_detail = user.usertask_set.all()
        return render(request, self.template_name,{
            'task_detail': self.get_object(),
            'task': task,
            'detail': task1
        })
        
class TaskBoardView(ListView):
    model = User
    template_name = 'users/task_board.html'
    context_object_name = 'task_board'
    
    def get(self, request, *args, **kwargs):
        user = request.user
        user_tasks = user.usertask_set.all()
        return render(request,'user/task_board.html',{
            'user_tasks':user_tasks})
#--------------------------------------------------------------------------------------------------------------
@login_required
def dashboard(request):
    return render(request,'user/dashboard.html')

def password(request):
    return render(request,'user/password.html')

def navbar(request):
    return render(request,'user/navbar.html')



