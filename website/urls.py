from django.contrib import admin
from django.urls import path
from website import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('', views.customer_home, name='customer_home'),  # Trang chủ mặc định
    path('staff_home/', views.staff_home, name='staff_home'),  # Trang cho Nhân viên
    path('manager_home/', views.manager_home, name='manager_home'),  # Trang cho Quản lý
    path('redirect_user/', views.redirect_user, name='redirect_user'),  # Trang điều hướng người dùng
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Đăng xuất
    path('register/', views.register, name='register'),  # Trang đăng ký
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Đường dẫn cho trang đăng nhập

    path('profile/', views.profile, name='profile'),  # Trang thông tin cá nhân

    path('tours/staff/', views.tour_staff_list, name='tour_staff_list'),

    path('tours/', views.tour_list, name='tour_list'),  # Tìm kiếm tour du lịch
    path('tours/customer/', views.tour_list_customer, name='tour_list_customer'),  # Tìm kiếm tour cho khách hàng
    path('customers/', views.customer_list, name='customer_list'),  # Quản lý thông tin khách hàng
    path('tours/add/', views.add_tour, name='add_tour'),  # Thêm tour
    path('tours/edit/<int:tour_id>/', views.edit_tour, name='edit_tour'),  # Chỉnh sửa tour
    path('tours/delete/<int:tour_id>/', views.delete_tour, name='delete_tour'),  # Xóa tour
    path('staff/', views.staff_list, name='staff_list'),  # Danh sách nhân viên
    path('staff/add/', views.add_staff, name='add_staff'),  # Thêm nhân viên

    path('tours/register/', views.register_tour, name='register_tour'),  # Trang đăng ký tour

    path('tours/my_registrations/', views.tour_registrations_by_staff, name='my_registrations'),

    path('tours/registrations/', views.tour_registrations_by_staff, name='tour_registrations'),

    path('contact/', views.contact, name='contact'),
    

]
