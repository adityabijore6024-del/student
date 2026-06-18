from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.landing_view, name='index'),

    path('policy/', views.policy_view, name='policy'),

    path('signup/', views.signup_view, name='signup'),

    path('payment/', views.payment_view, name='payment'),

    path('payment-success/', views.payment_success, name='payment_success'),

    path('login/', views.login_view, name='login'),

    path('home/', views.home_view, name='home'),

    path('teacher/<int:id>/',views.teacher_courses,name='teacher_courses'),

path(
    'payment2/<int:course_id>/',
    views.payment2_view,
    name='payment2'
),

path(
    'course-access/<int:course_id>/',
    views.course_access,
    name='course_access'
),


path(
    'course-payment-success/<int:course_id>/',
    views.course_payment_success,
    name='course_payment_success'
),

path(
    'doubt/',
    views.doubt_solver,
    name='doubt'
),
path(
"profile/",
views.profile_view,
name="profile"
),

path(
    'all-courses/',
    views.all_courses,
    name='all_courses'
),
path(
    'activity/',
    views.activity,
    name='activity'
),
path(
    "contact-support/",
    views.contact_support,
    name="contact_support"
),
# Course ke saare tests
    path(
        "course/<int:course_id>/tests/",
        views.test_list,
        name="test_list"
    ),

    # Test start page
    path(
        "test/<int:test_id>/",
        views.start_test,
        name="start_test"
    ),

    # Test submit
    path(
        "test/<int:test_id>/submit/",
        views.submit_test,
        name="submit_test"
    ),

    # Result page
    path(
        "result/<int:attempt_id>/",
        views.result_page,
        name="result_page"
    ),

    # User history
    path(
        "my-tests/",
        views.my_test_history,
        name="my_test_history"
    ),

]