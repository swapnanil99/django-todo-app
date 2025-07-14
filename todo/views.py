from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from todo.models import TODOO, UserProfile


def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        icon = request.POST.get('profile_icon')

        # If username already exists
        if User.objects.filter(username=fnm).exists():
            messages.error(request, " Username already exists.")
            return redirect('signup')

        # Create new user
        user = User.objects.create_user(username=fnm, email=email, password=pwd)
        user.save()

        # Save selected profile icon
        if icon:
            UserProfile.objects.create(user=user, profile_icon=icon)

        messages.success(request, " Account created successfully! Please login.")
        return redirect('login')

    # Show icon list
    icons = [
        ("user0.png", "User 0"),
        ("user1.png", "User 1"),
        ("user2.png", "User 2"),
        ("user3.png", "User 3"),
        ("user4.png", "User 4"),
        ("user5.png", "User 5"),
        ("user6.png", "User 6"),
    ]
    return render(request, 'signup.html', {'icons': icons})


def login_view(request):
    if request.method == 'POST':
        fnmm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')

        user = authenticate(request, username=fnmm, password=pwd)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"👋 Welcome back, {user.username}!")
            return redirect('todo')
        else:
            messages.error(request, "❌ Invalid username or password")

    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)
    messages.info(request, "👋 You have been logged out.")
    return redirect('login')


@login_required(login_url='/login/')
def todo_view(request):
    tasks = TODOO.objects.filter(user=request.user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = total_tasks - completed_tasks

    # Get the profile icon from UserProfile
    try:
        profile = UserProfile.objects.get(user=request.user)
        icon = profile.profile_icon
    except UserProfile.DoesNotExist:
        icon = "user0.png"  # fallback icon

    return render(request, 'todo.html', {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'profile_icon': icon  # ✅ pass this to the template
    })



@login_required
@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('task')
        if TODOO.objects.filter(user=request.user, title=title).exists():
            messages.error(request, "❗ This task already exists!")
        else:
            TODOO.objects.create(user=request.user, title=title)
            messages.success(request, "✅ Task added successfully!")
    return redirect('todo')


@login_required
@csrf_exempt
def edit_task(request, task_id):
    task = get_object_or_404(TODOO, srno=task_id, user=request.user)
    if request.method == 'POST':
        new_title = request.POST.get('task')
        task.title = new_title
        task.save()
        messages.success(request, "✏️ Task updated successfully!")
        return redirect('todo')
    return render(request, 'edit_task.html', {'task': task})


@login_required
@csrf_exempt
def delete_task(request, task_id):
    task = get_object_or_404(TODOO, srno=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, "🗑️ Task deleted successfully!")
    return redirect('todo')


@login_required
@csrf_exempt
def toggle_complete(request, task_id):
    task = get_object_or_404(TODOO, srno=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    if task.completed:
        messages.success(request, "✅ Task marked as completed!")
    else:
        messages.success(request, "🔄 Task marked as incomplete!")
    return redirect('todo')

@login_required
def update_icon(request):
    if request.method == 'POST':
        new_icon = request.POST.get('profile_icon')
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.profile_icon = new_icon
        profile.save()
        messages.success(request, "✅ Profile icon updated successfully!")
    return redirect('/todo')