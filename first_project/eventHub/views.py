from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Event, Attendee
from .forms import SignUpForm, SignInForm, UserUpdateForm, ProfileUpdateForm, ContactForm, RegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db.models import Q


# View for the homepage
def home(request):
    event = Event.objects.all()
    return render(request, 'eventHub/home.html', {'event': event})


# Class-based view for displaying a list of events for the homepage
class EventListView(ListView):
    model = Event
    template_name = 'eventHub/home.html'
    context_object_name = 'event'
    ordering = ['-date']
    paginate_by = 8


# View for the landing page
def landingpage(request):
    return render(request, 'eventHub/landingpage.html')


# View for the about page
def about(request):
    return render(request, 'eventHub/aboutpage.html')


# View for the contact page
def contact(request):
    if request.method =='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            #Process and send the email
            subject = 'Contact Form Submission'
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['email']
            recipient_list = ['nanagyamera3@gmail.com']
            send_mail(subject, message, from_email, recipient_list)
            return redirect('success-page')
    else:
        form = ContactForm()
    return render(request, 'eventHub/contact.html', {'form': form})


# View for the success page after a form submission
def successPage(request):
    return render(request, 'eventHub/sucess.html')


# View for user sign-in
def signIn(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('eventHub-home')
            else:
                messages.error(request, 'Incorrect Username or Password')
    else:
        form = SignInForm()
    return render(request, 'eventHub/signin.html', {'form': form})


# View for user registration
def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('eventHub-home')
            else:
                messages.error(request, 'Incorrect Username or Password')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = SignUpForm()
    return render(request, 'eventHub/signup.html', {'form': form})


# View for user sign-out
def signOut(request):
    logout(request)
    return redirect('eventHub-landingpage')


# Class-based view for displaying event details
class EventDetailView(DetailView):
    model = Event


# Class-based view for creating a new event
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'location', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('eventHub-home')  # Redirect to the homepage
    

# Class-based view for updating an event
class EventUpdateView(UserPassesTestMixin,LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['title', 'location', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    
    def get_success_url(self):
        return reverse_lazy('eventHub-home')  # Redirect to the homepage
    
    
    def test_func(self):
        event = self.get_object()
        if self.request.user == event.author:
            return True
        return False
    

# Class-based view for deleting an event   
class EventDeleteView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):
    model = Event
    success_url = reverse_lazy('eventHub-home')

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.author:
            return True
        return False
    

 # View for user profile           
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'eventHub/userprofile.html', context)


# View for searching events
def search_events(request):
    query = request.GET.get('q')
    results = Event.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'eventHub/search_results.html', {'results': results})


# View for registering for an event
def register_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    registration_successful = False

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Process the form and save the registration
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            # Create an Attendee record for the user
            attendee, created = Attendee.objects.get_or_create(user=request.user, event=event)
            attendee.name = name
            attendee.email = email
            # Set other fields for the Attendee model as needed
            attendee.save()

            registration_successful = True  # Set this to display the confirmation message

    else:
        form = RegistrationForm(initial={'event_id': event_id})

    return render(request, 'eventHub/eventregistration.html', {'form': form, 'event': event, 'registration_successful': registration_successful})


# View for displaying registered attendees for an event
def registered_attendees(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    attendees = Attendee.objects.filter(event=event)
    return render(request, 'eventHub/registered_attendees.html', {'event': event, 'attendees': attendees})