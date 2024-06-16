from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages, auth
from .models import SeekerProfile
from django.core.mail import send_mail
from django.conf import settings
from geopy.distance import great_circle





def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def registerHire(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'You are now registered and can log in')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'registerHire.html')
def registerSeeker(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        location = request.POST['location']
        about_me = request.POST['about_me']
        phone_number = request.POST['phone_number']
        skill_set = request.POST['skill_set']
        profile_photo = request.FILES.get('profile_photo')  # Get uploaded profile photo

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                seeker_profile = SeekerProfile(
                    user=user,
                    location=location,
                    about_me=about_me,
                    phone_number=phone_number,
                    skill_set=skill_set,
                    profile_photo=profile_photo  # Save profile photo to SeekerProfile model
                )
                seeker_profile.save()
                messages.success(request, 'You are now registered and can log in')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'registerSeeker.html')


def logout(request):
    auth.logout(request)
    return redirect('/')

def main(request):
    return render(request, 'desk.html')
def home(request):
    return render(request, 'home.html')

def search_results(request):
    if request.method == 'GET':
        skill_query = request.GET.get('query', '')
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')

        if skill_query:
            job_seekers = SeekerProfile.objects.filter(skill_set__icontains=skill_query)
        else:
            job_seekers = SeekerProfile.objects.none()

        if latitude is not None and longitude is not None:
            user_location = (float(latitude), float(longitude))
            # Calculate distance and sort job seekers by distance
            job_seekers_with_distance = []
            for seeker in job_seekers:
                if seeker.latitude is not None and seeker.longitude is not None:
                    seeker_location = (float(seeker.latitude), float(seeker.longitude))
                    distance = great_circle(user_location, seeker_location).miles
                    job_seekers_with_distance.append({
                        'seeker': seeker,
                        'distance': distance
                    })
            # Sort job seekers by distance
            job_seekers_with_distance = sorted(job_seekers_with_distance, key=lambda x: x.get('distance', float('inf')))

            return render(request, 'search.html', {'results': job_seekers_with_distance, 'latitude': latitude, 'longitude': longitude})
        
        return render(request, 'search.html', {'results': job_seekers})

    return render(request, 'search.html')

def seeker_detail(request, seeker_id):
    seeker = get_object_or_404(SeekerProfile, pk=seeker_id)
    return render(request, 'seeker_detail.html', {'seeker': seeker})

def edit_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    seeker_profile = get_object_or_404(SeekerProfile, user=user)

    if request.method == 'POST':
        # Retrieve data from POST request
        location = request.POST.get('location')
        skill_set = request.POST.get('skill_set')
        about_me = request.POST.get('about_me')
        phone_number = request.POST.get('phone_number')

        # Update SeekerProfile fields
        seeker_profile.location = location
        seeker_profile.skill_set = skill_set
        seeker_profile.about_me = about_me
        seeker_profile.phone_number = phone_number

        # Save updated profile
        User.save()
        seeker_profile.save()

        # Redirect to the seeker's detail page or any other desired page
        return redirect('home')

    # If not a POST request, render the edit profile form
    return render(request, 'edit_profile.html', {'user': user, 'seeker_profile': seeker_profile})


def booking(request, seeker_id):
    seeker = get_object_or_404(SeekerProfile, pk=seeker_id)
    if request.method == 'POST':
        # Extract additional fields from the form data
        date = request.POST.get('date')
        time = request.POST.get('time')
        note = request.POST.get('note')

        # Assuming you have the seeker's email stored in your Seeker model
        """if seeker.email:
            subject = 'Regarding your booking request'
            message = f'Dear {seeker.user.username},\n\nWe have received your booking request for {date} at {time}.\n\nAdditional Notes: {note}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [seeker.email]

            send_mail(subject, message, from_email, recipient_list)

            # Optionally, you can redirect the user to another page after sending the email
            return redirect('home')
        else:
            # Handle case where seeker email is not available
            return render(request, 'error.html', {'error_message': 'Seeker email not found'})
            """
        return redirect('home')

    return render(request, 'booking.html')

def about(request):
    return render(request, 'about.html')


