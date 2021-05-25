from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("logout", views.logout, name="logout"),
    path("institution", views.institution, name="institution"),
    path("branch", views.branch, name="branch"),
    path("course", views.course, name="course"),
    path("delete_branch", views.delete_branch, name="delete_branch"),
    path("delete_course", views.delete_course, name="delete_course"),
    path("delete_institute", views.delete_institute, name="delete_institute"),
    path("delete_planbanner", views.delete_planbanner, name="delete_planbanner"),
    path("delete_introbanner", views.delete_introbanner, name="delete_introbanner"),
    path("delete_institutebranch", views.delete_institutebranch, name="delete_institutebranch"),
    path("delete_institutebanner", views.delete_institutebanner, name="delete_institutebanner"),
    path("delete_insitute_course", views.delete_insitute_course, name="delete_insitute_course"),
    path("update_branch", views.update_branch, name="update_branch"),
    path("update_doc", views.update_doc, name="update_doc"),
    path("update_course", views.update_course, name="update_course"),
    path("update_institute", views.update_institute, name="update_institute"),
    path("update_planbanner", views.update_planbanner, name="update_planbanner"),
    path("update_introbanner", views.update_introbanner, name="update_introbanner"),
    path("update_institutebanner", views.update_institutebanner, name="update_institutebanner"),
    path("update_institutebranch", views.update_institutebranch, name="update_institutebranch"),
    path("update_institute_course", views.update_institute_course, name="update_institute_course"),
    path("supporting_documents", views.supporting_documents, name="supporting_documents"),
    path("delete_supporting_doc", views.delete_supporting_doc, name="delete_supporting_doc"),
    path("statecity", views.statecity, name="statecity"),
    path("list_branch", views.list_branch, name="list_branch"),
    path("list_course", views.list_course, name="list_course"),
    path("list_institute_branch_courses", views.list_institute_branch_courses, name="list_institute_branch_courses"),
    path("list_doc", views.list_doc, name="list_doc"),
    path("list_institute", views.list_institute, name="list_institute"),
    path("list_planbanner", views.list_planbanner, name="list_planbanner"),
    path("list_introbanner", views.list_introbanner, name="list_introbanner"),
    path("list_institutebanner", views.list_institutebanner, name="list_institutebanner"),
    path("list_staff", views.list_staff, name="list_staff"),
    path("list_institute_branch", views.list_institute_branch, name="list_institute_branch"),
    path("list_institute_course", views.list_institute_course, name="list_institute_course"),
    path("introbanner", views.introbanner, name="introbanner"),
    path("planbanner", views.planbanner, name="planbanner"),
    path("institutebanner", views.institutebanner, name="institutebanner"),
    path("profile", views.profile, name="profile"),
    path("college", views.college, name="college"),
    path("staff", views.staff, name="staff"),
    path("institute_branch", views.institute_branch, name="institute_branch"),
    path("institutecourse", views.institutecourse, name="institutecourse"),
    path("students", views.students, name="students"),
    path("list_course_duration", views.list_course_duration, name="list_course_duration"),
    path("list_student", views.list_student, name="list_student"),
    path("delete_student", views.delete_student, name="delete_student"),
    path("search_branch", views.search_branch, name="search_branch"),
    ]