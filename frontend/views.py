from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Q
from .models import Profile
from .models import Profile_app
from .models import Slide
from .models import Teacher
from .models import Teacher, Course
from .models import PurchasedCourse
import google.generativeai as genai
from google import genai
from .models import Profile_app
import razorpay
from django.conf import settings


# 1. Landing Page
def landing_view(request):
    return render(request, "index.html")


# 2. Policy Page
def policy_view(request):
    return render(request, "policy.html")


# 3. Signup Page
def signup_view(request):

    if request.method == "POST":

        username = request.POST.get('username')
        age = request.POST.get('age')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already registered'})

        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        request.session['signup_data'] = {
            'username': username,
            'age': age,
            'mobile': mobile,
            'email': email,
            'password': password1
        }

        return redirect('payment')

    return render(request, 'signup.html')


# 4. Payment Page
def payment_view(request):

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    order = client.order.create({
        "amount": 9900,
        "currency": "INR",
        "payment_capture": 1
    })

    request.session['order_id'] = order['id']

    return render(request, "payment.html", {
        "payment": order,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })


# 5. Payment Success
def payment_success(request):

    data = request.session.get('signup_data')
    order_id = request.session.get('order_id')

    if not data or not order_id:
        return redirect('signup')

    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )

    Profile.objects.create(
        user=user,
        phone=data['mobile'],
        age=data['age']
    )

    request.session.pop('signup_data', None)
    request.session.pop('order_id', None)

    return redirect('login')


# 6. Login
def login_view(request):

    if request.method == "POST":

        username = request.POST.get('username3')
        password = request.POST.get('password3')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

# 7. Home 
def home_view(request):

    slides = Slide.objects.all()
    teacher = Teacher.objects.all()

    query = request.GET.get('q')

    courses = Course.objects.none()

    if query:

        courses = Course.objects.filter(
            Q(course_name__icontains=query) |
            Q(description__icontains=query)
        )

        if query.isdigit():

            courses = courses | Course.objects.filter(
                id=int(query)
            )

    return render(
        request,
        'home.html',
        {
            'slides': slides,
            'teacher': teacher,
            'courses': courses,
        }
    )

# 8. Teacher_Course

def teacher_courses(request, id):

    teacher = Teacher.objects.get(id=id)

    courses = Course.objects.filter(teacher=teacher)

    purchased_ids = []

    if request.user.is_authenticated:
        purchased_ids = PurchasedCourse.objects.filter(
            user=request.user
        ).values_list('course_id', flat=True)

    return render(
        request,
        'teacher.html',
        {
            'teacher': teacher,
            'courses': courses,
            'purchased_ids': purchased_ids
        }
    )

# 9. Payment 
def payment2_view(request, course_id):

    course = Course.objects.get(id=course_id)

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    order = client.order.create({
        "amount": course.price * 100,
        "currency": "INR",
        "payment_capture": 1
    })

    return render(
        request,
        "payment2.html",
        {
            "course": course,
            "payment": order,
            "razorpay_key":
            settings.RAZORPAY_KEY_ID
        }
    )

# 10. Course.payment
def course_payment_success(
    request,
    course_id
):

    course = Course.objects.get(
        id=course_id
    )

    already = PurchasedCourse.objects.filter(
        user=request.user,
        course=course
    ).exists()

    if not already:

        PurchasedCourse.objects.create(
            user=request.user,
            course=course
        )

    return redirect(
        'course_access',
        course_id=course.id
    )


# 11. Courses 
def course_access(
    request,
    course_id
):

    course = Course.objects.get(
        id=course_id
    )

    purchased = PurchasedCourse.objects.filter(
        user=request.user,
        course=course
    ).exists()

    if not purchased:

        return redirect(
            'payment2',
            course_id=course.id
        )
    
    print("Current User:", request.user)
    print("Is Authenticated:", request.user.is_authenticated)

    course = Course.objects.get(id=course_id)

    purchased = PurchasedCourse.objects.filter(
    user=request.user,
    course=course
    )

    print("Purchased:", purchased.exists())

    return render(
        request,
        'course.html',
        {
            'course': course
        }
    )

# 12. Doubt solver 

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

def doubt_solver(request):

    answer = ""

    if request.method == "POST":

        question = request.POST.get("question")

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=question
            )

            answer = response.text

        except Exception as e:

            answer = f"Error: {e}"

    return render(
        request,
        "doubt.html",
        {
            "answer": answer
        }
    )

from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):


    profile, created = Profile_app.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

     profile.phone = request.POST.get("phone")
     profile.age = request.POST.get("age")
     profile.gender = request.POST.get("gender")
     profile.bio = request.POST.get("bio")
     profile.hobbies = request.POST.get("hobbies")
     profile.city = request.POST.get("city")
     profile.instagram = request.POST.get("instagram")
     profile.github = request.POST.get("github")

    if request.FILES.get("profile_image"):
        profile.profile_image = request.FILES["profile_image"]

    profile.save()

    return render(
    request,
    "profile.html",
    {
        "profile": profile
    }
)

# All course 
def all_courses(request):

    courses = Course.objects.all()

    return render(
        request,
        'all_courses.html',
        {
            'courses': courses
        }
    )

from .models import PurchasedCourse

def activity(request):

    purchases = PurchasedCourse.objects.filter(
        user=request.user
    ).order_by('-purchased_at')

    total_courses = purchases.count()

    last_purchase = purchases.first()

    total_spent = sum(
        item.course.price
        for item in purchases
    )

    return render(
        request,
        'activity.html',
        {
            'purchases': purchases,
            'total_courses': total_courses,
            'last_purchase': last_purchase,
            'total_spent' :total_spent,
        }
    )

from django.shortcuts import render
from .models import SupportTicket

def contact_support(request):

    success = False

    if request.method == "POST":

        subject = request.POST.get(
            "subject"
        )

        message = request.POST.get(
            "message"
        )

        SupportTicket.objects.create(

            user=request.user,

            subject=subject,

            message=message

        )

        success = True

    tickets = SupportTicket.objects.filter(

        user=request.user

    ).order_by(

        "-created_at"
    )

    return render(

        request,

        "contact_support.html",

        {

            "success":success,

            "tickets":tickets

        }
    )

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import (
    Test,
    Question,
    Option,
    TestAttempt,
    StudentAnswer,
    Course
)


@login_required
def test_list(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    tests = Test.objects.filter(
        course=course
    )

    return render(
        request,
        "test_list.html",
        {
            "course": course,
            "tests": tests
        }
    )


@login_required
def start_test(request, test_id):

    test = get_object_or_404(
        Test,
        id=test_id
    )

    questions = Question.objects.filter(
        test=test
    )

    return render(
        request,
        "test_page.html",
        {
            "test": test,
            "questions": questions
        }
    )


@login_required
def result_page(request, attempt_id):

    attempt = get_object_or_404(
        TestAttempt,
        id=attempt_id,
        user=request.user
    )

    return render(
        request,
        "result.html",
        {
            "attempt": attempt
        }
    )


@login_required
def my_test_history(request):

    attempts = TestAttempt.objects.filter(
        user=request.user
    ).order_by("-submitted_at")

    return render(
        request,
        "attempt_history.html",
        {
            "attempts": attempts
        }
    )

@login_required
def submit_test(request, test_id):

    if request.method != "POST":
        return redirect(
            "start_test",
            test_id=test_id
        )

    test = get_object_or_404(
        Test,
        id=test_id
    )

    questions = Question.objects.filter(
        test=test
    )

    correct_count = 0
    wrong_count = 0
    skipped_count = 0
    total_score = 0

    time_taken = int(
        request.POST.get(
            "time_taken",
            0
        )
    )

    attempt = TestAttempt.objects.create(
        user=request.user,
        test=test
    )

    for question in questions:

        if question.question_type == "single":

            selected_option_id = request.POST.get(
                f"question_{question.id}"
            )

            if not selected_option_id:
                skipped_count += 1
                continue

            option = Option.objects.get(
                id=selected_option_id
            )

            is_correct = option.is_correct

            if is_correct:
                correct_count += 1
                total_score += question.marks
            else:
                wrong_count += 1

            StudentAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_option=option,
                is_correct=is_correct
            )

        elif question.question_type == "integer":

            answer = request.POST.get(
                f"question_{question.id}"
            )

            if answer == "":
                skipped_count += 1
                continue

            is_correct = (
                int(answer)
                ==
                question.correct_integer_answer
            )

            if is_correct:
                correct_count += 1
                total_score += question.marks
            else:
                wrong_count += 1

            StudentAnswer.objects.create(
                attempt=attempt,
                question=question,
                integer_answer=answer,
                is_correct=is_correct
            )

    total_questions = questions.count()

    percentage = 0

    if total_questions > 0:
        percentage = round(
            (correct_count / total_questions) * 100,
            2
        )

    attempt.score = total_score
    attempt.total_questions = total_questions
    attempt.correct_answers = correct_count
    attempt.wrong_answers = wrong_count
    attempt.skipped_answers = skipped_count
    attempt.percentage = percentage
    attempt.time_taken_seconds = time_taken

    attempt.save()

    return redirect(
        "result_page",
        attempt_id=attempt.id
    )