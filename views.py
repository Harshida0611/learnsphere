#razorpay method
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

from django.urls import reverse

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def payment(request):
    currency = 'INR'
    amount = 20000  # Rs. 200
    
    quiz_id = request.GET.get('quiz_id')  # Get quiz ID from URL
    
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    
    callback_url = reverse('paymenthandler') + f"?quiz_id={quiz_id}"

    # we need to pass these details to frontend.
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount / 100,  # Convert paise to INR for display
        'currency': currency,
        'callback_url': callback_url,
        'quiz_id': quiz_id
    }

    return render(request, 'payment.html', context=context)

# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            quiz_id = request.GET.get('quiz_id')  # Get quiz ID from URL

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    
                    # Redirect to the quiz after successful payment
                    return redirect(f'/quiz/{quiz_id}/')
                except:
                    return render(request, 'paymentfail.html')
            else:
                return render(request, 'paymentfail.html')
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()



from django.contrib import messages
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login as auth_login
# views.py

# views.py
# views.py

from django.shortcuts import render, redirect
from django.urls import reverse
from Register.forms import UserProfileForm
from Register.models import UserProfile
from django.contrib.auth.hashers import check_password
import assignment
from assignment.forms import AssignmentForm
from assignment.models import Assignment
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from assignment.models import Assignment


def student_assignment_list(request):
    assignments = Assignment.objects.all()

        
    return render(request, 'D:/django-project/LearnSphere/assignment/templates/stud_assignment.html', {"assignments": assignments})



def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)  # Handling file uploads
        if form.is_valid():
            form.save()  # Save the form to the database
            return redirect('assignment_list')  # Redirect after successful submission
    else:
        form = AssignmentForm()

   

    return render(request, 'D:/django-project/LearnSphere/assignment/templates/create_assignmnet.html', {'form': form})

# View for listing all assignments

def assignment_list(request):
    assignments = Assignment.objects.all()  # Fetch all assignments

    if request.method == "POST":  
        form = AssignmentForm(request.POST, request.FILES)  # Handle file uploads too
        if form.is_valid():
            form.save()  # Save the new assignment
            return redirect("assignment_list")  # Redirect to refresh the page

    else:
        form = AssignmentForm()  # Empty form for GET request

    return render(request, "D:/django-project/LearnSphere/assignment/templates/assignment_list.html", {"assignments": assignments, "form": form})

def edit_assignment(request, id):
    assignment = get_object_or_404(Assignment, id=id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignment_list')  # Redirect after save
    else:
        form = AssignmentForm(instance=assignment)

    return render(request, 'D:/django-project/LearnSphere/assignment/templates/edit_assignment.html', {'form': form, 'assignment': assignment})

def delete_assignment(request, id):
    # Fetch the assignment or return 404 if not found
    assignment = get_object_or_404(Assignment, id=id)

    if request.method == 'POST':
        # Delete the assignment from the database
        assignment.delete()
        return redirect('assignment_list')  # Redirect to the assignment list page after deletion

    return render(request, 'D:/django-project/LearnSphere/assignment/templates/delete_assignment.html', {'assignment': assignment})
from annoucement.models import Announcement
from annoucement.forms import AnnouncementForm

def create_announcement(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('announcement_list')  # Redirect after saving
    else:
        form = AnnouncementForm()

  
    
    return render(request, 'D:/django-project/LearnSphere/annoucement/templates/create_annuncement.html', {'form': form})

def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'D:/django-project/LearnSphere/annoucement/templates/annoucement_list.html', {'announcements': announcements})

def stud_announcement(request):
    announcements = Announcement.objects.all().order_by('-date')  # Fetch announcements, newest first
    return render(request, "D:/django-project/LearnSphere/annoucement/templates/stud_announcement.html", {'announcements': announcements})

def edit_announcement(request, id):
    announcement = get_object_or_404(Announcement, id=id)

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcement_list')  # Redirect to the list after editing
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, 'D:/django-project/LearnSphere/annoucement/templates/edit_announcement.html', {'form': form, 'announcement': announcement})

def delete_announcement(request, id):
    # Get the announcement or raise 404 if not found
    announcement = get_object_or_404(Announcement, id=id)

    if request.method == 'POST':
        # Delete the announcement
        announcement.delete()
        return redirect('announcement_list')  # Adjust 'announcement_list' with the correct URL name for the list page

   
    return render(request, 'D:/django-project/LearnSphere/annoucement/templates/delete_announcement.html', {'announcement': announcement})



def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = UserProfile.objects.get(email=email, password=password)
            request.session['user_email'] = user.email  # Store email in session
            messages.success(request, "Login successful!")
            return redirect('studentdash')  # Redirect to dashboard after login
        except UserProfile.DoesNotExist:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, 'login.html')
def enroll_login(request):
    return render(request, "enroll_login.html")
def ds1(request):
    return render(request, "ds1.html")
def ds2(request):
    return render(request, "ds2.html")
def ds3(request):
    return render(request, "ds3.html")
def ds4(request):
    return render(request, "ds4.html")
def ai1(request):
    return render(request, "ai1.html")
def ai2(request):
    return render(request, "ai2.html")
def ai3(request):
    return render(request, "ai3.html")
def c1(request):
    return render(request, "c1.html")
def c2(request):
    return render(request, "c2.html")
def c3(request):
    return render(request, "c3.html")
def cc1(request):
    return render(request, "cc1.html")
def cc2(request):
    return render(request, "cc2.html")
def cc3(request):
    return render(request, "cc3.html")
def cc4(request):
    return render(request, "cc4.html")
def b1(request):
    return render(request, "b1.html")
def b2(request):
    return render(request, "b2.html")
def b3(request):
    return render(request, "b3.html")
def b4(request):
    return render(request, "b4.html")
def w1(request):
    return render(request, "w1.html")
def w2(request):
    return render(request, "w2.html")
def w3(request):
    return render(request, "w3.html")
def w4(request):
    return render(request, "w4.html")
def de1(request):
    return render(request, "de1.html")
def de2(request):
    return render(request, "de2.html")
def de3(request):
    return render(request, "de3.html")
def de4(request):
    return render(request, "de4.html")
def do1(request):
    return render(request, "do1.html")
def do2(request):
    return render(request, "do2.html")
def do3(request):
    return render(request, "do3.html")
def do4(request):
    return render(request, "do4.html")
def app1(request):
    return render(request, "app1.html")
def app2(request):
    return render(request, "app2.html")
def app3(request):
    return render(request, "app3.html")
def app4(request):
    return render(request, "app4.html")

def register(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('login')  # Redirect to a success page or another page
        else:
            return render(request, 'Registration.html', {'form': form})
    else:
        form = UserProfileForm()
        return render(request, 'Registration.html', {'form': form})



def studentdash(request):
    student = request.user  

    quiz_count = Quiz.objects.count()
    announcement_count = Announcement.objects.count()
    assignment_count = Assignment.objects.count()

    context = {
        'student': student,
        'quiz_count': quiz_count,
        'announcement_count': announcement_count,
        'assignment_count': assignment_count,
    }

    return render(request, 'studentdash.html', context)

    

def login(request):

    return render(request, "login.html")
def home(request):
    return render(request,"index.html")
def aboutUs(request):
    return render(request,"aboutus.html")
def courses(request):
    return render(request,"courses.html")

def display_course(request):
    return render(request,"display_course.html")
def datascience(request):
    return render(request,"ds.html")
def machine(request):
    return render(request,"ai_ml.html")
def cyber(request):
    return render(request,"cybersecurity.html")
def cloud(request):
    return render(request,"cloud.html")
def devops(request):
    return render(request,"devops.html")
def blockchain(request):
    return render(request,"blockchain.html")
def mobileapp(request):
    return render(request,"mobileapp.html")
def dataeng(request):
    return render(request,"dataeng.html")
def web(request):
    return render(request,"web.html")

from django.shortcuts import render




def dashboard(request):
    quiz_count = Quiz.objects.count()  # Count total quizzes
    assignment_count = Assignment.objects.count()  # Count total assignments
    announcement_count = Announcement.objects.count()  # Count total announcements
    student_count = UserProfile.objects.count()  # Count total users using the 'id' field

    context = {
        "quiz_count": quiz_count,
        "assignment_count": assignment_count,
        "announcement_count": announcement_count,
        "student_count": student_count,  # Total number of users in the database
    }

    return render(request, "dashboard.html", context)


def profile_settings(request):
    # Logic for loading the Profile Settings page
    return render(request, 'profile.html')

def account_settings(request):
    # Logic for loading the Account Settings page
    return render(request, 'account.html')
def navigation(request):
    return render(request,"nav.html")
def navheader(request):
    return render(request,"nh.html")

def stud_nav(request):
    return render(request,"stud_nav.html")
# In views.py


from quiz.models import Quiz, Question

from django.http import JsonResponse
from quiz.models import Quiz, Question
import json

def add_quiz(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")

        if title and description and due_date:
            quiz = Quiz.objects.create(title=title, description=description, due_date=due_date)
            return redirect(reverse("add_questions", kwargs={"quiz_id": quiz.id}))  # ✅ Fixed redirect

    return render(request, "D:/django-project/LearnSphere/quiz/templates/add_quiz.html")

from django.shortcuts import render, get_object_or_404, redirect
from quiz.models import Quiz, Question

def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == "POST":
        total_questions = 11  # Ensure it is exactly 10 questions

        for i in range(1, total_questions + 1):  # Runs from 1 to 10 (inclusive)
            question_text = request.POST.get(f"question-{i}")
            option1 = request.POST.get(f"option1-{i}")
            option2 = request.POST.get(f"option2-{i}")
            option3 = request.POST.get(f"option3-{i}")
            option4 = request.POST.get(f"option4-{i}")
            correct_option = request.POST.get(f"correct-option-{i}")

            if question_text and option1 and option2 and option3 and option4 and correct_option:
                Question.objects.create(
                    quiz=quiz,
                    text=question_text,
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    correct_option=int(correct_option),
                )

        return redirect("admin_quiz_list")  # Redirect after saving

    return render(
        request, 
        "D:/django-project/LearnSphere/quiz/templates/quiz_question.html", 
        {"quiz": quiz, "quiz_id": quiz.id}
    )
def student_list(request):
    students = UserProfile.objects.all()  # Fetch all student data
    
    return render(request, 'D:/django-project/LearnSphere/templates/stud_list.html', {'students': students})


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from Register.models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Register.models import UserProfile

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Register.models import UserProfile

@login_required(login_url='/login/')  # Redirect to login page if user is not logged in
def edit_student_profile(request):
    if request.user.is_anonymous:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')  # Redirect to login if user is not authenticated

    # Fetch the user profile based on the email
    student = get_object_or_404(UserProfile, email=request.user.email)

    if request.method == "POST":
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.phone = request.POST.get('phone')
        student.address = request.POST.get('address')
        student.email = request.POST.get('email')
        student.technology = request.POST.get('technology')

        # Handle profile picture update
        if 'photo' in request.FILES:
            student.photo = request.FILES['photo']

        student.save()  # Save changes
        messages.success(request, "Profile updated successfully!")
        return redirect('studentdash')  # Redirect after saving

    return render(request, 'edit_student_profile.html', {'student': student})


from django.shortcuts import render, get_object_or_404
from quiz.models import Quiz, Question
from django.urls import reverse
from django.contrib import messages


import random


# View to display all quizzes
def quiz_list(request):
    quizzes = Quiz.objects.all()  # Fetch all quizzes
    quiz = quizzes.first()  # Get a sample quiz (or use logic to determine which one)

    # Check if quiz exists before passing
    context = {
        'quizzes': quizzes,
        'quiz': quiz if quiz else None,
    }
    return render(request, 'D:/django-project/LearnSphere/quiz/templates/quiz_list.html', context)

    

# View to display shuffled questions for a specific quiz
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Fetch all questions and select 10 random ones
    all_questions = list(quiz.questions.all())  
    questions = random.sample(all_questions, min(10, len(all_questions)))

    # Store selected question IDs in session to ensure the same ones are evaluated
    request.session["displayed_question_ids"] = [q.id for q in questions]

    return render(request, "quiz_detail.html", {
        "quiz": quiz,
        "questions": questions  # Only these 10 questions will be displayed
    })

# View for handling quiz submission

import random
from django.shortcuts import render, get_object_or_404, redirect
from quizres.models import CertificateRequest
from quiz.models import Quiz, Question
import random
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def submit_quiz(request, quiz_id):
    if request.method == "POST":
        quiz = get_object_or_404(Quiz, id=quiz_id)

        # Retrieve the 10 displayed questions from session
        question_ids = request.session.get("displayed_question_ids", [])
        questions = list(quiz.questions.filter(id__in=question_ids))  # Fetch only those 10 questions

        score = 0
        total = len(questions)  # Always 10 (or fewer if not enough questions)

        submitted_answers = {}  # To store what the user selected

        for question in questions:
            selected_option = request.POST.get(f"question_{question.id}")

            # Store the user's selected answer
            submitted_answers[question.id] = selected_option

            # Ensure both values are compared as strings for accuracy
            correct_answer = str(question.correct_option).strip()
            user_answer = str(selected_option).strip() if selected_option else ""

            if user_answer == correct_answer:
                score += 1  # Increment score if correct

        # Calculate percentage
        percentage = (score / total) * 100 if total > 0 else 0

        # Store results in session
        request.session["quiz_score"] = score  # Store correct answer count
        request.session["quiz_total"] = total  # Always out of 10
        request.session["quiz_percentage"] = round(percentage, 2)  # Round percentage to 2 decimal places
        request.session["submitted_answers"] = submitted_answers  # Store user answers

        return redirect("quiz_list")  # Redirect to quiz list after submission

    return redirect("quiz_detail", quiz_id=quiz_id)  # Redirect if not a POST request


 # Redirect if not a POST request
from django.http import JsonResponse

def save_certificate_request(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        course = request.POST.get("course")

        # Get the quiz results from the session
        quiz_score = request.session.get("quiz_score", 0)
        quiz_total = request.session.get("quiz_total", 10)
        quiz_percentage = request.session.get("quiz_percentage", 0)

        # Save to database
        CertificateRequest.objects.create(
            full_name=full_name,
            email=email,
            course=course,
            quiz_score=quiz_score,
            quiz_total=quiz_total,
            quiz_percentage=quiz_percentage
        )

        return JsonResponse({"message": "Certificate request saved successfully!"})

    return JsonResponse({"error": "Invalid request"}, status=400)


def clear_quiz_session(request):
    """Clears quiz score session data after displaying it once."""
    request.session.pop("quiz_score", None)
    request.session.pop("quiz_total", None)
    request.session.pop("quiz_percentage", None)
    return JsonResponse({"status": "success"})

def admin_quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, "D:/django-project/LearnSphere/quiz/templates/admin_quiz_list.html", {"quizzes": quizzes})

def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == "POST":
        quiz.title = request.POST.get("title")
        quiz.description = request.POST.get("description")
        quiz.due_date = request.POST.get("due_date")
        quiz.save()
        return redirect("admin_quiz_list")  # Redirect to quiz list after editing

    return render(request, "edit_quiz.html", {"quiz": quiz})

def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()
    messages.success(request, "Quiz deleted successfully.")
    return redirect("admin_quiz_list")  # Redirect after deletion

from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from Register.models import UserProfile  # Assuming UserProfile stores registered users

def get_registered_users(request):
    users = UserProfile.objects.values('email', 'password')
    return JsonResponse(list(users), safe=False)


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import render

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import render
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import render
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

import io
from django.http import FileResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
from quizres.models import CertificateRequest

from io import BytesIO
from django.http import FileResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from quizres.models import CertificateRequest

from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from io import BytesIO
from quizres.models import CertificateRequest
from quiz.models import Quiz

from django.shortcuts import get_object_or_404
from django.http import FileResponse, HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from quiz.models import Quiz
from quizres.models import CertificateRequest

def generate_certificate(request, quiz_id=None):
    if request.method == "POST":
        # Fetch the quiz
        quiz = get_object_or_404(Quiz, id=quiz_id)

        # Get user details
        full_name = request.POST.get("full_name", "Student").strip().title()
        email = request.POST.get("email", "").strip()

        # Save certificate request in the database
        CertificateRequest.objects.create(
            full_name=full_name,
            email=email,
            quiz=quiz
        )

        # Example score (You can replace this with your actual quiz result calculation)
        score_percentage = 90.0  # This should ideally come from quiz results

        # Generate PDF Certificate
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Add border
        p.setStrokeColor(colors.black)
        p.setLineWidth(5)
        p.rect(30, 30, width - 60, height - 60)

        # Add logo
        try:
            logo_path = "static/images/logo.png"
            logo = ImageReader(logo_path)
            logo_width, logo_height = 80, 80
            logo_x = width / 2 - (logo_width / 2)
            logo_y = height - 120
            p.drawImage(logo, logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')
        except:
            pass

        # LearnSphere text
        p.setFont("Helvetica-Bold", 22)
        p.drawCentredString(width / 2, height - 150, "LearnSphere")

        # Certificate Title
        p.setFont("Helvetica-Bold", 28)
        p.drawCentredString(width / 2, height - 190, "🎓 Certificate of Achievement 🎓")

        # Subtitle
        p.setFont("Helvetica", 18)
        p.drawCentredString(width / 2, height - 230, "This certificate is proudly presented to")

        # Student Name
        p.setFont("Helvetica-Bold", 24)
        p.setFillColor(colors.blue)
        p.drawCentredString(width / 2, height - 270, full_name)
        p.setFillColor(colors.black)

        # Course Name
        p.setFont("Helvetica", 18)
        p.drawCentredString(width / 2, height - 310, "for successfully completing the course")
        p.setFont("Helvetica-Bold", 22)
        p.setFillColor(colors.green)
        p.drawCentredString(width / 2, height - 340, quiz.title)
        p.setFillColor(colors.black)

        # ➕ Add score content
        p.setFont("Helvetica", 16)
        p.drawCentredString(width / 2, height - 370, f"You scored {score_percentage:.1f}% in the quiz")

        # Footer Text
        p.setFont("Helvetica", 14)
        p.drawCentredString(width / 2, height - 400, "We recognize your hard work and dedication. Keep learning!")

        # Signature Line
        p.setStrokeColor(colors.black)
        p.line(100, 100, 300, 100)
        p.setFont("Helvetica", 12)
        p.drawString(100, 85, "Authorized Signature")

        # Signature Text
        p.setFont("Helvetica-Oblique", 22)
        p.setFillColor(colors.gray)
        p.drawCentredString(200, 120, "LearnSphere")

        p.showPage()
        p.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f"{full_name}_certificate.pdf")

    return HttpResponse("Invalid request", status=400)

def certificate_page(request):
    return render(request, "certificate.html", {"full_name": "John Doe", "course": "Python Programming"})



from quizres.models import CertificateRequest

def certificate_list(request):
    certificates = CertificateRequest.objects.all()  # Fetch all certificate requests
    return render(request, 'certificates.html', {'certificates': certificates})

import random
import smtplib
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from Register.models import UserProfile

# Dictionary to store verification codes temporarily
verification_codes = {}

@csrf_exempt
def forgot_password(request):
    if request.method == "POST":
        data = json.loads(request.body)
        step = data.get("step")

        # Step 1: Send Verification Code
        if step == "email":
            email = data.get("email")
            try:
                user = UserProfile.objects.get(email=email)  # Check if user exists
                verification_code = str(random.randint(100000, 999999))
                verification_codes[email] = verification_code  # Store code temporarily
                
                # Send Email (Update with your SMTP settings)
                sender_email = "dhobi.harshida06@gmaail.com"
                sender_password = "H@rsh!da0611"
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, "H@rsh!da0611")
                message = f"Subject: LearnSphere Password Reset\n\nYour verification code is: {verification_code}"
                server.sendmail(sender_email, email, message)
                server.quit()

                return JsonResponse({"success": True, "message": "Verification code sent to your email."})
            except UserProfile.DoesNotExist:
                return JsonResponse({"success": False, "error": "Email not registered."})

        # Step 2: Verify Code
        elif step == "code":
            email = data.get("email")
            code = data.get("code")

            if email in verification_codes and verification_codes[email] == code:
                return JsonResponse({"success": True, "message": "Code verified successfully."})
            else:
                return JsonResponse({"success": False, "error": "Invalid verification code."})

        # Step 3: Reset Password
        elif step == "password":
            email = data.get("email")
            new_password = data.get("password")

            try:
                user = UserProfile.objects.get(email=email)
                user.password = new_password  # Store password in plain text
                user.save()
                del verification_codes[email]  # Remove verification code
                return JsonResponse({"success": True, "message": "Password reset successfully."})
            except UserProfile.DoesNotExist:
                return JsonResponse({"success": False, "error": "User not found."})

    return render(request, "forget.html")



from django.shortcuts import render, redirect
from stud_ass.models import AssignmentSubmission
from django.contrib import messages

def submit_assignment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        pdf_file = request.FILES.get('pdf_file')

        if pdf_file and pdf_file.name.endswith('.pdf'):
            AssignmentSubmission.objects.create(name=name, email=email, pdf_file=pdf_file)
            messages.success(request, "Assignment submitted successfully!")
            return redirect('student_assignment_list')  # Change this to a real success page URL
        else:
            messages.error(request, "Please upload a valid PDF file.")

    return render(request, 'D:/django-project/LearnSphere/stud_ass/templates/submit_assignment.html')

from django.shortcuts import render
from stud_ass.models import AssignmentSubmission

def assignment_list_students(request):
    submissions = AssignmentSubmission.objects.all()
    return render(request, 'D:/django-project/LearnSphere/stud_ass/templates/assignment_list.html', {'submissions': submissions})
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from Register.models import UserProfile

def send_otp(request):
    """Send OTP to the email"""
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        email = data.get("email")

        try:
            user = UserProfile.objects.get(email=email)  # Check if user exists

            # Generate a 6-digit OTP
            otp = str(random.randint(100000, 999999))
            request.session["otp"] = otp  # Store OTP in session
            request.session["email"] = email  # Store email in session

            # Send OTP via email
            send_mail(
                "Password Reset OTP",
                f"Your OTP for password reset is: {otp}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return JsonResponse({"message": "OTP sent successfully!"})

        except UserProfile.DoesNotExist:
            return JsonResponse({"message": "User with this email does not exist!"}, status=400)

def verify_otp(request):
    """Verify entered OTP and redirect to reset password if valid"""
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        generated_otp = request.session.get("otp")  # Get stored OTP
        email = request.session.get("email")

        if not email:
            messages.error(request, "Session expired. Please try again.")
            return redirect("verify_otp")

        if entered_otp == generated_otp:
            request.session["otp_verified"] = True  # Mark OTP as verified
            messages.success(request, "OTP verified! Now reset your password.")
            return redirect("reset_password")  # Redirect to reset password page

        messages.error(request, "Invalid OTP. Please try again.")
        return redirect("verify_otp")

    return render(request, "verify_otp.html")

def reset_password(request):
    """Reset the password if OTP verification is successful"""
    if not request.session.get("otp_verified"):
        messages.error(request, "OTP verification failed. Please try again.")
        return redirect("verify_otp")

    if request.method == "POST":
        email = request.session.get("email")  # Get stored email
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("reset_password")

        try:
            user = UserProfile.objects.get(email=email)
            user.password = new_password  # Save plain-text password (No hashing)
            user.save()

            request.session.flush()  # Clear session
            messages.success(request, "Password reset successful! Please log in.")
            return redirect("login")  # Redirect to login page

        except UserProfile.DoesNotExist:
            messages.error(request, "Something went wrong. Try again.")

    return render(request, "reset_password.html")
