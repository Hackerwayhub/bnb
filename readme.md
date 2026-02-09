bnbke/
├── auth/                           # Authentication app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── forms.py                    # Create this
│   └── urls.py                     # Create this
├── bnb/                            # Project config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── listings/                       # Main listings app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── sitemaps.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── auth/                       # Auth templates (move here)
│   │   ├── forgotpassword.html
│   │   ├── login.html
│   │   ├── password_reset_email.html
│   │   ├── profile.html
│   │   └── register.html
│   ├── emails/                     # Email templates
│   │   └── booking_confirmation.html
│   ├── listings/                   # Listings templates
│   │   ├── bnb_house_party.html    # 
│   │   ├── book_via_whatsapp.html # 
│   │   ├── booking_confirmation.html
│   │   ├── booking_form.html      # 
│   │   ├── edit_listing.html
│   │   ├── list.html              # create listings page
│   │   ├── listings_detail.html
│   │   ├── my_listings.html
│   │   └── bnb.html     #displays listings to user
│   ├── base.html
│   └── robots.txt                 # Move from root
├── media/
│   ├── listings/                     
│   ├── extra/                 
│   └── main/                  
├── static/
│   ├── css/
│   ├── fonts/
│   ├── images/
│   └── js/
├── staticfiles/                    # For collectstatic output
├── venv/
├── .env
├── .gitignore
├── db.sqlite3
├── manage.py
└── requirements.txt