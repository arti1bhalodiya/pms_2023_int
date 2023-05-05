from django.shortcuts import render,redirect
from django.views.generic import CreateView
from .forms import *
from django.views.generic import ListView,DetailView,FormView
from django.views.generic import DeleteView,UpdateView
from .models import *
from django.http import HttpResponseRedirect
# Create your views here.



class ProjectCreationView(CreateView):
    form_class =ProjectCreationForm
    model = Project
    template_name = 'project/project_create.html'
    success_url = '/project/list_project/'


class ProjectListView(ListView):
    model = Project
    template_name = 'project/project_list.html'
    context_object_name = 'project_list'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort_by', 'title')
        sort_by = self.request.GET.get('sort_by', 'tech')
        direction = self.request.GET.get('direction', 'asc')
        if direction == 'asc':
            queryset = queryset.order_by(sort_by)
        elif direction == 'desc':
            queryset = queryset.order_by(f'-{sort_by}')
        return queryset
    
    # def get(self, request):
    #     projects = Project.objects.all()
    #     context = {'projects': projects}
    #     return render(request, self.template_name, context) 
    

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectCreationForm
    template_name = 'project/project_create.html'
    success_url = '/project/list_project/'
    
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/project_detail.html'
    context_object_name = 'project_detail'
    
    labels=[]
    data =[]
    project = ProjectModule.objects.all().values_list('name',flat=True)
    time = ProjectModule.objects.all().values_list('estimatedHrs',flat=True)
    for i in project:
        labels.append(i)
    for i in time:
        data.append(i)
    
    
    def get(self, request, *args, **kwargs):
        team = ProjectTeam.objects.filter(project=self.kwargs['pk'])
        module = ProjectModule.objects.filter(project=self.kwargs['pk'])
        return render(request, self.template_name, {'project_detail': self.get_object(),'team':team,'module':module,'labels':self.labels,'data':self.data})
    
    # def get(self, request, *args, **kwargs):
    #     module = ProjectModule.objects.filter(project=self.kwargs['pk'])
    #     return render(request, self.template_name, {'project_detail': self.get_object(),'team':module})
    
class ProjectDeleteView(DeleteView):
    model = Project
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    success_url = '/project/list_project/'   
    
class ProjectTeamCreationView(CreateView):
    model = ProjectTeam
    form_class =ProjectTeamCreationForm
    template_name = 'project/project_team_create.html'
    success_url = '/project/list_project/'
    
    def form_valid(self, form):
        return super().form_valid(form) 
    
class Create_Project_team(CreateView):
    form_class =ProjectTeamCreationForm
    template_name = 'project/project_team_create.html'
    success_url = '/project/list_project/'

class ProjectTeamListView(ListView):
    model = ProjectTeam
    template_name = 'project/project_team_list.html'
    context_object_name = 'project_team_list'
    
class ProjectTeamByProject(ListView):
    model = ProjectTeam
    template_name = 'project/project_team_list.html'
    context_object_name = 'project_team_list'
    
    def get_queryset(self):
        # return super().get_queryset().filter(Project_id=self.kwargs['pk']) 
        return ProjectTeam.objects.filter(project=self.kwargs['pk'])
    
class CreateProjectModule(CreateView):
    model = ProjectModule
    form_class = CreateProjectModuleForm
    template_name = 'project/project_module_create.html'
    success_url = '/project/list_project_module/'
    
        

class ProjectModuleListByProject(ListView):
    model = ProjectModule
    template_name = 'project/project_module_list.html'
    context_object_name = 'project_module_list'
    
    
    # def get_queryset(self):
    #     return super().get_queryset().filter(project=self.kwargs['pk']) 
    
class ProjectTeamDeleteView(DeleteView):
    model = ProjectTeam
    template_name = 'project/project_detail.html'
    success_url = '/project/detail_project/'
    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    # def delete(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     success_url = request.GET.get('next',self.success_url)
    #     self.object.delete()
    #     return HttpResponseRedirect(success_url)
    
    # def get_success_url(self):
    #     return self.request.GET.get('next',self.success_url)
    
    
class ModuleUpdateView(UpdateView):
    model = ProjectModule
    form_class = CreateProjectModuleForm
    template_name = 'project/project_module_create.html'
    success_url = '/project/list_project_module/' 
    
class ModuleDeleteView(DeleteView):
    model = ProjectModule
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    success_url = '/project/detail_project/'  
    
class ModuleDetailView(DetailView):
    model = ProjectModule
    template_name = 'project/module_detail.html'
    context_object_name = 'module_detail'
    
   
    def get(self, request, *args, **kwargs):
       
        task = Task.objects.filter(module_id=self.kwargs['pk']).values()
        # print("task.....",task)
        return render(request, self.template_name, {'project_detail': self.get_object(),'task': task})
    
    
# class TeamDeleteView(DeleteView):
#     model = ProjectTeam
    
#     def get(self, request, *args, **kwargs):
#         return self.delete(request, *args, **kwargs)
    
#     success_url = '/project/detail_project/'
        
        
class CreateProjectTask(CreateView):
    model = Task
    form_class = CreateProjectTaskForm
    template_name = 'project/project_task_create.html'
    success_url = '/project/list_project_task/'
    
class ProjectTaskListByProject(ListView):
    model = Task
    template_name = 'project/project_task_list.html'
    context_object_name = 'project_task_list'
    
    
class TaskUpdateView(UpdateView):
    model = Task
    form_class = CreateProjectTaskForm
    template_name = 'project/project_task_create.html'
    success_url = '/project/list_project_task/' 
    
class TaskDeleteView(DeleteView):
    model = Task
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    success_url = '/project/list_project_task/' 
    
class UserTaskDeleteView(DeleteView):
    model = UserTask
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    success_url = '/project/assign_project_task/'
    
class AssignProjectTask(CreateView):
    form_class = AssignProjectTaskForm
    template_name = 'project/project_task_assign.html'
    success_url = '/project/assign_project_task/'

class ProjectTaskListView(ListView):
    model = UserTask
    template_name = 'project/project_task_list_assign.html'
    context_object_name = 'project_task_list_assign'
    