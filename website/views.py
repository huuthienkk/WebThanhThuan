from venv import logger
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from .models import Tour
from .forms import TourForm
from django.contrib.auth import logout
from django.http import HttpResponseNotAllowed
from django.contrib import messages
from .models import TourRegistration
import logging 
from django.contrib.auth.models import Group


@login_required
def customer_home(request):
    if request.user.groups.filter(name='Customers').exists():
        return render(request, 'Customer/customer_home.html')
    return redirect('login')  # Nếu không đúng nhóm, điều hướng về trang đăng nhập

@login_required
def staff_home(request):
    if request.user.groups.filter(name='Staff').exists():
        return render(request, 'Staff/staff_home.html')
    return redirect('login')

@login_required
def manager_home(request):
    if request.user.groups.filter(name='Managers').exists():
        return render(request, 'Manager/manager_home.html')
    return redirect('login')

@login_required
def redirect_user(request):
    if request.user.groups.filter(name='Customers').exists():
        return redirect('customer_home')
    elif request.user.groups.filter(name='Staff').exists():
        return redirect('staff_home')
    elif request.user.groups.filter(name='Managers').exists():
        return redirect('manager_home')
    else:
        return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Thêm người dùng vào nhóm 'Customers' sau khi đăng ký
            customers_group = Group.objects.get(name='Customers')
            customers_group.user_set.add(user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'registration/profile.html')

@login_required
def tour_list_customer(request):
    tours = Tour.objects.all()
    query = request.GET.get('q')
    if query:
        tours = tours.filter(name__icontains=query)
    return render(request, 'Customer/tour_list_customer.html', {'tours': tours})


@login_required
def tour_list(request):
    tours = Tour.objects.all()
    query = request.GET.get('q')
    if query:
        tours = tours.filter(name__icontains=query)
    return render(request, 'Manager/tour_list.html', {'tours': tours})

@login_required
def tour_staff_list(request):
    tours = Tour.objects.all()
    query = request.GET.get('q')
    if query:
        tours = tours.filter(name__icontains=query)
    return render(request, 'Staff/tour_staff_list.html', {'tours': tours})


@login_required
def customer_list(request):
    if request.user.groups.filter(name='Staff').exists():
        customers = User.objects.filter(groups__name='Customers')
        return render(request, 'Staff/customer_list.html', {'customers': customers})
    else:
        return redirect('login')

# Kiểm tra nếu người dùng thuộc nhóm 'Managers'
def is_manager(user):
    return user.groups.filter(name='Managers').exists()

def is_staff(user):
    return user.groups.filter(name='Staff').exists()  # Đảm bảo "Staff" với chữ cái hoa


@user_passes_test(lambda user: is_manager(user) or is_staff(user))
@login_required
def add_tour(request):
    # Log thông tin về người dùng
    logger.debug(f"User: {request.user}, is_manager: {is_manager(request.user)}, is_staff: {is_staff(request.user)}")

    # Kiểm tra quyền truy cập
    if not (is_manager(request.user) or is_staff(request.user)):
        messages.error(request, 'Bạn không có quyền tạo tour.')
        return redirect('customer_home')  # Hoặc trang đích khác

    # Xử lý thêm tour khi người dùng có quyền
    if request.method == 'POST':
        form = TourForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tour đã được tạo thành công!')
            return redirect('tour_list')
    else:
        form = TourForm()

    return render(request, 'Staff/add_tour.html', {'form': form})

@user_passes_test(is_manager)
def edit_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = TourForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()
            return redirect('tour_list')
    else:
        form = TourForm(instance=tour)
    return render(request, 'Staff/edit_tour.html', {'form': form})

@user_passes_test(is_manager)
def delete_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    tour.delete()
    return redirect('tour_list')

@user_passes_test(is_manager)
def add_staff(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            staff_group = Group.objects.get(name='Staff')
            staff_group.user_set.add(user)
            return redirect('staff_list')
    else:
        form = UserCreationForm()
    return render(request, 'Manager/add_staff.html', {'form': form})

@user_passes_test(is_manager)
def staff_list(request):
    staff_members = User.objects.filter(groups__name='Staff')
    return render(request, 'Manager/staff_list.html', {'staff_members': staff_members})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')  # Điều hướng đến trang đăng nhập sau khi đăng xuất
    else:
        return HttpResponseNotAllowed(['POST'])  # Chỉ cho phép phương thức POST
    

@login_required
def register_tour(request):
    if request.method == 'POST':
        tour_id = request.POST.get('tour_id')
        tour = get_object_or_404(Tour, id=tour_id)
        # Tạo bản ghi đăng ký tour
        registration = TourRegistration(customer=request.user, tour=tour)
        registration.save()  # Lưu bản ghi vào database
        messages.success(request, 'Đăng ký tour thành công!')
        return redirect('tour_list_customer')

    # Nếu không phải POST, render form đăng ký
    tours = Tour.objects.all()  # Lấy danh sách tour để người dùng chọn
    return render(request, 'Customer/register_tour.html', {'tours': tours})


@login_required  # Đảm bảo chỉ nhân viên đã đăng nhập mới truy cập
def tour_registrations_by_staff(request):
    # Lấy danh sách tất cả đăng ký tour
    registrations = TourRegistration.objects.all().select_related('customer', 'tour')

    return render(request, 'Staff/tour_registrations.html', {'registrations': registrations})


def contact(request):
    return render(request, 'contact.html')



def profile(request):
    user = request.user
    group = None
    if user.groups.filter(name='Customers').exists():
        group = 'Customers'
    elif user.groups.filter(name='Staff').exists():
        group = 'Staff'
    elif user.groups.filter(name='Managers').exists():
        group = 'Managers'
    
    return render(request, 'registration/profile.html', {
        'user': user,
        'group': group,
    })