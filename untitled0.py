from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    # additional fields for client entity

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    # additional fields for project entity

# views.py
from django.shortcuts import render, redirect
from .models import Client, Project

def register_client(request):
    if request.method == 'POST':
        name = request.POST['name']
        contact_info = request.POST['contact_info']
        client = Client(name=name, contact_info=contact_info)
        client.save()
        return redirect('fetch_clients')
    return render(request, 'register_client.html')

def fetch_clients(request):
    clients = Client.objects.all()
    return render(request, 'fetch_clients.html', {'clients': clients})

def edit_client(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        client.name = request.POST['name']
        client.contact_info = request.POST['contact_info']
        client.save()
        return redirect('fetch_clients')
    return render(request, 'edit_client.html', {'client': client})

def delete_client(request, client_id):
    client = Client.objects.get(id=client_id)
    client.delete()
    return redirect('fetch_clients')

def add_project(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        project = Project(name=name, description=description, client=client)
        project.save()
        users = request.POST.getlist('users')
        for user_id in users:
            user = User.objects.get(id=user_id)
            project.users.add(user)
        project.save()
        return redirect('fetch_projects', client_id=client_id)
    users = User.objects.all()
    return render(request, 'add_project.html', {'client': client, 'users': users})

def fetch_projects(request, client_id):
    client = Client.objects.get(id=client_id)
    projects = Project.objects.filter(client=client)
    return render(request, 'fetch_projects.html', {'client': client, 'projects': projects})

def retrieve_assigned_projects(request):
    user = request.user
    projects = Project.objects.filter(users=user)
    return render(request, 'retrieve_assigned_projects.html', {'projects': projects})
