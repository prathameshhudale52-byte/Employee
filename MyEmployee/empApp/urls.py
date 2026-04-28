from django.contrib import admin
from django.urls import path
from empApp import views

urlpatterns = [

    path('', views.login_view, name='login'),   # login at root

    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),

    path('empList/', views.empList, name='empList'),
    path('addEmp/', views.addEmp, name='addEmp'),
    path('delEmp/<int:id>/', views.delEmp, name='delEmp'),
    path('updateEmp/<int:id>/', views.updateEmp, name='updateEmp'),

    path('roleList/', views.roleList, name='roleList'),
    path('addRole/', views.addRole, name='addRole'),

    path('deptList/', views.deptList, name='deptList'),
    path('addDept/', views.addDept, name='addDept'),

    path('employee/dashboard/', views.emp_dashboard, name='emp_dashboard'),
    path('employee/profile/', views.emp_profile, name='emp_profile'),
    path('employee/update/', views.emp_update, name='emp_update'),

    # path('apply-leave/', views.apply_leave, name='apply_leave'),
    # path('my-leaves/', views.leave_list, name='leave_list'),

    # path('manage-leaves/', views.manage_leaves, name='manage_leaves'),
    # path('approve-leave/<int:id>/', views.approve_leave, name='approve_leave'),
    # path('reject-leave/<int:id>/', views.reject_leave, name='reject_leave'),

    path('admin/', admin.site.urls),
]
