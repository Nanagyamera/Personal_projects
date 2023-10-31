![Screenshot 2023-10-31 213240](https://github.com/Nanagyamera/Personal_projects/assets/111068130/89705b02-d516-45cc-894d-0ff2efb3011a)
MyWebsite - EventHub

OVERVIEW

MyWebsite is a web application called "EventHub" built with Django. EventHub allows users to create, manage, and share events. Users can also update their profiles, including adding a profile picture and a short bio.

FEATURES

User registration and authentication

Create, update and delete events

Update user profiles with a profile picture and bio

Event listings with event details

User-friendly interface

User event registration

Event Search

INSTALLATION

Clone the repository to your local machine

Navigate to the project directory:

Create a virtual environment:

python -m venv venv

Activate the virtual environment:

ON WINDOWS:

venv\Scripts\activate

On macOS and Linux:

source venv/bin/activate

Install project dependencies:

pip install -r requirements.txt

Start the development server:

python manage.py runserver

Access the application in your web browser at http://localhost:8000.

USAGE

User Registration:

New users can register for an account.

Visit the registration page and fill in the required details.

Upon successful registration, users can log in with their credentials.

Creating Events:

Logged-in users can create new events.

Navigate to the "Create Event" page.

Fill in the event details, including title, location, and description.

After submission, the event will be added to the event listings.

Managing Events:

Event authors can manage their events.

On the "Manage Events" page, authors can update event details or delete events they've created.

Event Listings:

Users can explore event listings.

Events are displayed with key details such as title, location, date, and description.

User Profiles:

Users have the option to personalize their profiles.

Upload a profile picture and provide a bio.

Event Registration:

Users can register for events created by others.

Event authors can view a list of users who have registered for their events.

Event Search:

Search for specific events by entering keywords, such as the event title or description, in the search bar.

User-Friendly Interface:

The application provides an intuitive and responsive user interface for an enhanced user experience.

LICENSE

This project is licensed under the MIT License.
