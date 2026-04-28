from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as admin_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from empApp.models import Department, Employee, Role, Leave
from .forms import EmployeeForm, DepartmentForm, RoleForm, LeaveForm


# ================= ROLE CHECK =================
def admin_only(user):
    if user.is_authenticated:
        if user.is_staff:
            return True
        if hasattr(user, 'employee'):
            return user.employee.role.name.lower() == "admin"
    return False


# ================= AUTH =================
def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            admin_login(request, user)

            # Admin → Home
            if admin_only(user):
                return redirect('home')

            # Employee → Dashboard
            return redirect('emp_dashboard')

        else:
            error_message = "Invalid credentials"

    return render(request, 'login.html', {'error': error_message})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


# ================= ADMIN DASHBOARD =================
@login_required(login_url='login')
def home(request):
    if not admin_only(request.user):
        return redirect('emp_dashboard')

    context = {
        'total_emp': Employee.objects.count(),
        'total_dept': Department.objects.count(),
        'total_role': Role.objects.count(),
    }
    return render(request, 'home.html', context)


# ================= EMPLOYEE MANAGEMENT =================
@login_required(login_url='login')
def empList(request):
    if not admin_only(request.user):
        return redirect('emp_dashboard')

    emps = Employee.objects.select_related('dept', 'role').all()
    return render(request, "empList.html", {'emps': emps})


@login_required(login_url='login')
def addEmp(request):
    if not admin_only(request.user):
        return redirect('emp_dashboard')

    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            emp = form.save()

            username = (emp.fname + emp.lname).lower()
            password = "emp123"

            user = User.objects.create_user(
                username=username,
                password=password
            )

            emp.user = user
            emp.save()

            messages.success(
                request,
                f"Employee Added! Username: {username} Password: {password}"
            )
            return redirect("empList")
    else:
        form = EmployeeForm()

    return render(request, "addEmp.html", {'form': form})


@login_required(login_url='login')
def delEmp(request, id):
    if not admin_only(request.user):
        return redirect('emp_dashboard')

    emp = get_object_or_404(Employee, id=id)
    emp.delete()
    messages.success(request, "Employee deleted successfully")
    return redirect("empList")


@login_required(login_url='login')
def updateEmp(request, id):
    if not admin_only(request.user):
        return redirect('emp_dashboard')

    emp = get_object_or_404(Employee, id=id)

    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee Updated Successfully")
            return redirect("empList")
    else:
        form = EmployeeForm(instance=emp)

    return render(request, "updateEmp.html", {'form': form})


# ================= ROLE MANAGEMENT =================
@login_required(login_url='login')
def roleList(request):
    if not admin_only(request.user):
        return redirect('emp_dashboard')

    roles = Role.objects.all()
    return render(request, "roleList.html", {'roles': roles})


@login_required(login_url='login')
def addRole(request):
    if not admin_only(request.user):
        return redirect('emp_dashboard')

    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Role Added")
            return redirect("roleList")
    else:
        form = RoleForm()

    return render(request, "addRole.html", {'form': form})


# ================= DEPARTMENT =================
@login_required(login_url='login')
def deptList(request):
    if not admin_only(request.user):
        return redirect('emp_dashboard')

    depts = Department.objects.all()
    return render(request, "deptList.html", {'depts': depts})


@login_required(login_url='login')
def addDept(request):
    if not admin_only(request.user):
        return redirect('emp_dashboard')

    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department Added")
            return redirect("deptList")
    else:
        form = DepartmentForm()

    return render(request, "addDept.html", {'form': form})


# ================= EMPLOYEE PANEL =================
@login_required(login_url='login')
def emp_dashboard(request):
    if admin_only(request.user):
        return redirect('home')

    emp = get_object_or_404(Employee, user=request.user)
    return render(request, 'employee/dashboard.html', {'emp': emp})


@login_required(login_url='login')
def emp_profile(request):
    emp = get_object_or_404(Employee, user=request.user)
    return render(request, 'employee/profile.html', {'emp': emp})


@login_required(login_url='login')
def emp_update(request):
    emp = get_object_or_404(Employee, user=request.user)

    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated")
            return redirect('emp_dashboard')
    else:
        form = EmployeeForm(instance=emp)

    return render(request, 'employee/update.html', {'form': form})


# # ================= LEAVE SYSTEM =================
# @login_required(login_url='login')
# def apply_leave(request):
#     emp = get_object_or_404(Employee, user=request.user)

#     if request.method == "POST":
#         form = LeaveForm(request.POST)
#         if form.is_valid():
#             leave = form.save(commit=False)
#             leave.employee = emp
#             leave.save()
#             messages.success(request, "Leave Applied Successfully")
#             return redirect('leave_list')
#     else:
#         form = LeaveForm()

#     return render(request, 'employee/apply_leave.html', {'form': form})


# @login_required(login_url='login')
# def leave_list(request):
#     emp = get_object_or_404(Employee, user=request.user)
#     leaves = Leave.objects.filter(employee=emp).order_by('-id')
#     return render(request, 'employee/leave_list.html', {'leaves': leaves})


# @login_required(login_url='login')
# def manage_leaves(request):
#     if not admin_only(request.user):
#         return redirect('emp_dashboard')

#     leaves = Leave.objects.all().order_by('-id')
#     return render(request, 'manage_leaves.html', {'leaves': leaves})


# @login_required(login_url='login')
# def approve_leave(request, id):
#     if not admin_only(request.user):
#         return redirect('emp_dashboard')

#     leave = get_object_or_404(Leave, id=id)
#     leave.status = 'Approved'
#     leave.save()
#     return redirect('manage_leaves')


# @login_required(login_url='login')
# def reject_leave(request, id):
#     if not admin_only(request.user):
#         return redirect('emp_dashboard')

#     leave = get_object_or_404(Leave, id=id)
#     leave.status = 'Rejected'
#     leave.save()
#     return redirect('manage_leaves')
