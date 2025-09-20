

from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=80)
    enrollment_date = models.DateField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.department})"


class Instructor(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=80)
    hire_date = models.DateField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.department})"


class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    credits = models.PositiveSmallIntegerField()
    instructor = models.ForeignKey(
        Instructor, on_delete=models.PROTECT, related_name="courses"
    )

    class Meta:
        ordering = ["course_code"]

    def __str__(self):
        return f"{self.course_code} — {self.title}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course  = models.ForeignKey(Course,  on_delete=models.CASCADE, related_name="enrollments")
    enrollment_date = models.DateField()
    grade = models.CharField(max_length=2, blank=True)

    class Meta:
        # Prevent duplicate student-course pair (same course twice)
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"], name="uniq_student_course"
            )
        ]
        ordering = ["-enrollment_date"]

    def __str__(self):
        return f"{self.student} → {self.course}"