from django.db import models
from django.contrib.auth.models import User




# 1. Model for profile page
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15)
    age = models.IntegerField()

    def __str__(self):
        return self.user.username


# 2. Model for Home page image slider
class Slide(models.Model):

    section_id = models.CharField(max_length=100)

    image_url = models.URLField()

    def __str__(self):
        return self.section_id
    
# 3. Model for Teacher-box
class Teacher(models.Model):
    image = models.URLField(max_length=500)
    contain = models.CharField(max_length=500)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 4. Model for Courses
class Course(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE
    )
    course_image = models.URLField(null=True, blank=True)
    course_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField(default=99)
    def __str__(self):
        return self.course_name
    

# 5. Model for course purchasing
class PurchasedCourse(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.course_name}"
    

class Profile_app(models.Model):


    user = models.OneToOneField(        
           User,
        on_delete=models.CASCADE
    )

    profile_image = models.ImageField(        
    upload_to="profiles/",
    blank=True,
    null=True
    )

    phone = models.CharField(        
    max_length=15,
    blank=True
    )

    age = models.IntegerField(        
    blank=True,
    null=True
    )

    gender = models.CharField(        
    max_length=20,
    blank=True
    )

    bio = models.TextField(        
    blank=True
    )

    hobbies = models.CharField(
        max_length=300,
        blank=True
    )

    city = models.CharField(
    max_length=100,
    blank=True
    )

    instagram = models.CharField(
    max_length=200,
    blank=True
    )

    github = models.CharField(
    max_length=200,
    blank=True
    )

    def __str__(self):
        return self.user.username


from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User


class SupportTicket(models.Model):

    CATEGORY_CHOICES = [

        ("Course", "Course Problem"),

        ("Payment", "Payment Problem"),

        ("Login", "Login Problem"),

        ("Technical", "Technical Issue"),

        ("AI", "AI Doubt Solver"),

        ("Other", "Other")

    ]

    STATUS_CHOICES = [

        ("Pending", "Pending"),

        ("In Review", "In Review"),

        ("Solved", "Solved"),

        ("Rejected", "Rejected")

    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="Other"
    )

    subject = models.CharField(
        max_length=200
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return (
            f"{self.user.username} - "
            f"{self.subject}"
        )
    
from django.db import models
from django.contrib.auth.models import User


# Agar Course model isi file me nahi hai
# to niche wali line ko apne app ke naam ke hisab se change karna
# from courses.models import Course


class Test(models.Model):

    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='tests'
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    duration_minutes = models.PositiveIntegerField(
        default=30
    )

    total_marks = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Question(models.Model):

    QUESTION_TYPES = [

        ('single', 'Single Correct'),

        ('multiple', 'Multiple Correct'),

        ('integer', 'Integer Type')

    ]

    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question_text = models.TextField()

    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES
    )

    marks = models.PositiveIntegerField(
        default=1
    )

    correct_integer_answer = models.IntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.question_text[:50]


class Option(models.Model):

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='options'
    )

    option_text = models.CharField(
        max_length=500
    )

    is_correct = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.option_text


class TestAttempt(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE
    )

    score = models.IntegerField(
        default=0
    )

    total_questions = models.IntegerField(
        default=0
    )

    correct_answers = models.IntegerField(
        default=0
    )

    wrong_answers = models.IntegerField(
        default=0
    )

    skipped_answers = models.IntegerField(
        default=0
    )

    percentage = models.FloatField(
        default=0
    )

    time_taken_seconds = models.IntegerField(
        default=0
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.user.username}"
            f" - "
            f"{self.test.title}"
        )


class StudentAnswer(models.Model):

    attempt = models.ForeignKey(
        TestAttempt,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    selected_option = models.ForeignKey(
        Option,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    integer_answer = models.IntegerField(
        null=True,
        blank=True
    )

    is_correct = models.BooleanField(
        default=False
    )

    def __str__(self):

        return (
            f"{self.attempt.user.username}"
            f" - Question "
            f"{self.question.id}"
        )