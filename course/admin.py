
from django.contrib import admin
from django.db.models import Count
from .models import Student, Instructor, Course, Enrollment

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display  = ("name", "email", "department", "enrollment_date")
    search_fields = ("name", "email")                # searchable by name
    list_filter   = ("department", "enrollment_date")# filter by department
    date_hierarchy = "enrollment_date"


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1
    autocomplete_fields = ("student",)
    fields = ("student", "enrollment_date", "grade")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_code", "title", "instructor", "enrolled_count")
    search_fields = ("course_code", "title", "instructor__name")
    list_select_related = ("instructor",)
    inlines = [EnrollmentInline]   # inline add multiple students

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_enrolled=Count("enrollments"))

    @admin.display(description="Enrolled Students", ordering="_enrolled")
    def enrolled_count(self, obj):
        return obj._enrolled


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "department", "hire_date", "courses_count")
    search_fields = ("name", "email")
    list_filter   = ("department", "hire_date")
    date_hierarchy = "hire_date"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_courses=Count("courses"))

    @admin.display(description="# Courses", ordering="_courses")
    def courses_count(self, obj):
        return obj._courses


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display  = ("student", "course", "enrollment_date", "grade")
    search_fields = ("student__name", "course__title", "course__course_code")
    list_filter   = ("enrollment_date", "grade")
    date_hierarchy = "enrollment_date"
    autocomplete_fields = ("student", "course")