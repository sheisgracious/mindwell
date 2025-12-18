# MindWell 

This is a comprehensive web-based mental health platform that connects patients with therapists for virtual therapy sessions. MindWell helps by providing secure messaging, session scheduling, and therapy plan management for patients to discover and therapist to join.
**Website**: [https://cs-webapps.bu.edu/gpoa/mindwell/](https://cs-webapps.bu.edu/gpoa/mindwell/)

## Features

### For Patients
- **Browse Therapists**: Search and filter therapists by specialization, language, and experience
- **Therapy Plans**: Create customized therapy plans (Individual, Family, Kids therapy)
- **Session Booking**: Schedule sessions based on therapist availability
- **Secure Messaging**: Private communication with therapists
- **Dashboard**: Track upcoming sessions, view session history, and manage your profile

### For Therapists
- **Provider Dashboard**: Manage all patients and sessions in one place
- **Availability Management**: Set weekly availability schedules
- **Session Management**: Update session notes, payment status, and follow-up requirements
- **Patient Communication**: Respond to patient messages and maintain case notes
- **Plan Types**: Support multiple therapy plan types with custom pricing

**Sample Credentials**:

Provider Account:
- Username: `aisha.bello`
- Password: `MindWell123!`

Patient Account:
- Username: `fatima.khan`
- Password: `MindWell123!`

## 🛠️ Technologies Used

- **Backend**: Python3, Django 5.2.6
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Django Auth
- **Architecture**: Model-View-Template (MVT)

## 📋 Prerequisites

- Python 3.8 or higher
- pip 
- Git

## 💻 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/sheisgracious/mindwell.git
   cd mindwell
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django pillow
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and navigate to `http://localhost:8000/mindwell/`
   - Admin panel: `http://localhost:8000/admin/`

## 📁 Project Structure

```
mindwell/
├── mindwell/              # Main application
│   ├── models.py         # Database models
│   ├── views.py          # View logic
│   ├── forms.py          # Django forms
│   ├── urls.py           # URL routing
│   ├── templates/        # HTML templates
│   └── static/           # CSS, JavaScript, images
├── project/              # Project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # Root URL configuration
│   └── wsgi.py           # WSGI configuration
├── media/                # User-uploaded files
├── staticfiles/          # Collected static files
├── manage.py             # Django management script
└── db.sqlite3           # SQLite database
```

## 🗄️ Database Schema

Key models include:
- **HealthProvider**: Therapist profiles with specializations and availability
- **Patient**: Patient profiles with insurance and emergency contacts
- **TherapyPlan**: Links patients to providers with specific plan types
- **Session**: Individual therapy sessions with scheduling and status
- **Availability**: Provider weekly availability slots
- **Message**: Secure messaging between patients and providers
- **PlanType**: Different therapy plan offerings (Individual, Family, Kids)


## Future Enhancements

- [x] Message chat integration
- [ ] Video chat integration
- [ ] Payment processing
- [ ] Appointment reminders (email/SMS)
- [ ] Calendar integration
- [ ] Progress tracking and analytics
- [ ] Multi-language support
- [ ] Mobile app version with React Native


## License

This project was created as a coursework assignment for CS412 at Boston University.

## Acknowledgments

- Created for CS412
- Boston University, Fall 2025
- Special thanks to the course professor and TAs

---

**Please Note**: This is a student project created for educational purposes and not intended for production use with real patient data without proper HIPAA compliance and security audits.
