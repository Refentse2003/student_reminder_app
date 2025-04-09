from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, TaskForm
from .models import Task
from datetime import date, timedelta
from django.utils.timezone import localdate

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'tasks/register.html', {'form': form})


@login_required
def home(request):
    today = localdate()
    tomorrow = today + timedelta(days=1)
    next_week = today + timedelta(days=7)

    upcoming_tasks = Task.objects.filter(
        user=request.user,
        completed=False,
        due_date__range=[today, next_week]
    ).order_by('due_date')

    upcoming_count = upcoming_tasks.count()

    return render(request, 'tasks/home.html', {
        'upcoming': upcoming_count,
        'upcoming_tasks': upcoming_tasks,
        'today': today,
        'tomorrow': tomorrow,
    })


@login_required
def task_list(request):
    # Show only the logged-in user's tasks
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('task_list')

@login_required
def about(request):
    return render(request, 'tasks/about.html')

