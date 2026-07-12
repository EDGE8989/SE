from app import create_app
from extensions import db
from models.user import User
from models.club import Club
from models.event import Event
from models.notice import Notice
from models.scholarship import Scholarship
from models.workshop import Workshop
from models.opportunity import Opportunity
from models.calendar_event import CalendarEvent
from models.activity_log import ActivityLog
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, date, time

def seed_db():
    app = create_app('development')
    with app.app_context():
        # Clear existing data to ensure fresh, clean seeding
        print("[IEMS] Cleaning database...")
        db.drop_all()
        db.create_all()
        
        # 1. Create Users
        print("[IEMS] Seeding users...")
        super_admin = User(
            name='Super Admin',
            email='admin@iems.edu',
            password_hash=generate_password_hash('Admin@123'),
            role='super_admin',
            status='active'
        )
        college_admin = User(
            name='College Admin',
            email='college_admin@iems.edu',
            password_hash=generate_password_hash('Admin@123'),
            role='college_admin',
            status='active'
        )
        
        db.session.add_all([super_admin, college_admin])
        db.session.commit()
        
        # 2. Create Clubs
        print("[IEMS] Seeding clubs...")
        clubs_data = [
            {
                "name": "Coding Club",
                "description": "The coding community focused on algorithms, web development, open source contributions, and competitive programming.",
                "faculty": "Dr. Ramesh Sharma",
                "president": "Aman Verma",
                "email": "codingclub@cem.edu",
                "phone": "+91 98765 00001",
                "category": "technical",
                "is_active": True
            },
            {
                "name": "Robotics Society",
                "description": "Fostering interest in robotics, embedded systems, microcontrollers, IoT, and hardware building projects.",
                "faculty": "Prof. S. K. Gupta",
                "president": "Neha Patel",
                "email": "robotics@cem.edu",
                "phone": "+91 98765 00002",
                "category": "technical",
                "is_active": True
            },
            {
                "name": "Music and Dance Club",
                "description": "Uniting music and dance enthusiasts. Organizes jamming sessions, cultural fests, and intra-college competitions.",
                "faculty": "Mrs. Anjali Sen",
                "president": "Rohan Das",
                "email": "musicanddance@cem.edu",
                "phone": "+91 98765 00003",
                "category": "cultural",
                "is_active": True
            },
            {
                "name": "Literary & Debate Society",
                "description": "Nurturing creative writing, public speaking, poetry, and debate skills among engineering students.",
                "faculty": "Dr. Preeti Mishra",
                "president": "Siddharth Joshi",
                "email": "literary@cem.edu",
                "phone": "+91 98765 00004",
                "category": "general",
                "is_active": True
            },
            {
                "name": "Sports Association",
                "description": "Promoting physical fitness and team spirit through basketball, football, cricket, and athletics tournaments.",
                "faculty": "Mr. Vikram Singh",
                "president": "Tanmay Goel",
                "email": "sports@cem.edu",
                "phone": "+91 98765 00005",
                "category": "sports",
                "is_active": True
            }
        ]
        
        seeded_clubs = []
        for c in clubs_data:
            club = Club(**c)
            db.session.add(club)
            seeded_clubs.append(club)
        db.session.commit()
        
        # 3. Create Club President Users
        print("[IEMS] Seeding club presidents...")
        coding_president = User(
            name='Aman Verma',
            email='coding@iems.edu',
            password_hash=generate_password_hash('Admin@123'),
            role='club_president',
            club_id=seeded_clubs[0].id,
            status='active'
        )
        robotics_president = User(
            name='Neha Patel',
            email='robotics@iems.edu',
            password_hash=generate_password_hash('Admin@123'),
            role='club_president',
            club_id=seeded_clubs[1].id,
            status='active'
        )
        music_president = User(
            name='Rohan Das',
            email='music@iems.edu',
            password_hash=generate_password_hash('Admin@123'),
            role='club_president',
            club_id=seeded_clubs[2].id,
            status='active'
        )
        
        db.session.add_all([coding_president, robotics_president, music_president])
        db.session.commit()
        
        # 4. Create Events
        print("[IEMS] Seeding events...")
        events_data = [
            {
                "title": "Annual Hackathon (CEMHack 2026)",
                "description": "CEMHack is our flagship 36-hour coding marathon. Teams of up to 4 will build solutions for real-world problems in Healthcare, FinTech, and Smart Cities. Prizes worth Rs. 1,00,000 up for grabs!",
                "venue": "Main Seminar Hall",
                "date": date.today() + timedelta(days=15),
                "time": time(9, 0),
                "registration_link": "https://cemhack2026.example.com",
                "club_id": seeded_clubs[0].id,
                "status": "approved",
                "created_by": coding_president.id,
                "approved_by": college_admin.id
            },
            {
                "title": "RoboWars Exhibition",
                "description": "Watch customized combat robots clash in the custom-built arena! Live commentary, exciting crashes, and mechanical battles at their finest.",
                "venue": "Campus Open Amphitheatre",
                "date": date.today() + timedelta(days=22),
                "time": time(14, 0),
                "registration_link": "https://robowars.example.com",
                "club_id": seeded_clubs[1].id,
                "status": "approved",
                "created_by": robotics_president.id,
                "approved_by": college_admin.id
            },
            {
                "title": "Symphony: Cultural Jam Session",
                "description": "An open stage for acoustic, rock, classical and folk performances. Both solo and band entries are welcome. Come and support your local college musicians!",
                "venue": "College Auditorium",
                "date": date.today() + timedelta(days=8),
                "time": time(17, 30),
                "registration_link": "https://symphony.example.com",
                "club_id": seeded_clubs[2].id,
                "status": "approved",
                "created_by": music_president.id,
                "approved_by": college_admin.id
            },
            {
                "title": "Intra-College Coding Duel",
                "description": "A 2-hour competitive programming challenge on HackerRank. Speed and accuracy are everything. Refreshments will be provided.",
                "venue": "CS Lab 3 & 4",
                "date": date.today() + timedelta(days=4),
                "time": time(15, 0),
                "registration_link": "https://codingduel.example.com",
                "club_id": seeded_clubs[0].id,
                "status": "approved",
                "created_by": coding_president.id,
                "approved_by": college_admin.id
            },
            {
                "title": "Web Development Basics with React",
                "description": "A beginner-friendly project-building session. Learn components, state management, and basic API integrations.",
                "venue": "Online - Zoom Link to be emailed",
                "date": date.today() + timedelta(days=12),
                "time": time(10, 0),
                "registration_link": "https://reactweb.example.com",
                "club_id": seeded_clubs[0].id,
                "status": "pending",
                "created_by": coding_president.id
            },
            {
                "title": "Basketball Championship 2026",
                "description": "Inter-departmental basketball league matches. Cheer for your department and help them lift the trophy!",
                "venue": "Sports Arena Court A",
                "date": date.today() + timedelta(days=3),
                "time": time(16, 0),
                "registration_link": "https://sportsbasketball.example.com",
                "club_id": seeded_clubs[4].id,
                "status": "approved",
                "created_by": college_admin.id,
                "approved_by": super_admin.id
            }
        ]
        
        for e in events_data:
            event = Event(**e)
            db.session.add(event)
        db.session.commit()
        
        # 5. Create Notices
        print("[IEMS] Seeding notices...")
        notices_data = [
            {
                "title": "Registration Deadline for Odd Semester 2026",
                "description": "All students must submit their course registrations and pay academic fees for the upcoming semester. A late fee of Rs. 1000 will be applicable after the deadline.",
                "category": "academic",
                "club_id": None,
                "status": "approved",
                "created_by": college_admin.id
            },
            {
                "title": "Independence Day Celebration Program",
                "description": "Flag hoisting ceremony will begin at 8:30 AM in the Main Ground, followed by patriotic songs and a short speech by our honorable Director. Clean campus drive starts at 10:00 AM. Attendance is highly encouraged.",
                "category": "general",
                "club_id": None,
                "status": "approved",
                "created_by": college_admin.id
            },
            {
                "title": "Coding Club Core Committee Recruitment 2026",
                "description": "Coding Club is looking for passionate developers, designers, and managers for the core team. Interested 2nd and 3rd year students can apply via the portal. Interviews will be scheduled next week.",
                "category": "recruitment",
                "club_id": seeded_clubs[0].id,
                "status": "approved",
                "created_by": coding_president.id
            },
            {
                "title": "Mid-Semester Examination Schedule Out",
                "description": "The Mid-Semester Examination schedule for all branches has been uploaded to the website. Examinations will commence from July 20th. Admit cards can be collected from the department coordinator.",
                "category": "academic",
                "club_id": None,
                "status": "pending",
                "created_by": college_admin.id
            }
        ]
        
        for n in notices_data:
            notice = Notice(**n)
            db.session.add(notice)
        db.session.commit()
        
        # 6. Create Workshops
        print("[IEMS] Seeding workshops...")
        workshops_data = [
            {
                "title": "Python Flask Web Development",
                "description": "A hands-on workshop covering Flask app setup, routing, templates, SQLAlchemy database integration, and deploying to PythonAnywhere.",
                "speaker": "Mr. Rajdeep Sen (Senior Dev)",
                "venue": "Central Computing Center",
                "date": date.today() + timedelta(days=6),
                "time": time(14, 0),
                "registration_link": "https://flaskwork.example.com",
                "status": "approved",
                "created_by": college_admin.id,
                "approved_by": super_admin.id
            },
            {
                "title": "Introduction to Arduino and Microcontrollers",
                "description": "Get started with hardware coding. We will cover digital input/output, analog sensors, motors, and serial communication. Kits will be provided for teams of two.",
                "speaker": "Dr. Amit Roy (ECE Dept)",
                "venue": "ECE Hardware Lab",
                "date": date.today() + timedelta(days=14),
                "time": time(10, 0),
                "registration_link": "https://arduinowork.example.com",
                "status": "approved",
                "created_by": college_admin.id,
                "approved_by": super_admin.id
            },
            {
                "title": "UI/UX Design Masterclass using Figma",
                "description": "Learn typography, grids, layout structures, components, and creating clickable wireframes/high-fidelity prototypes in Figma.",
                "speaker": "Ms. Shruti Shah (Lead Designer)",
                "venue": "Design Studio Rm 102",
                "date": date.today() + timedelta(days=25),
                "time": time(11, 0),
                "registration_link": "https://figmawork.example.com",
                "status": "pending",
                "created_by": college_admin.id
            }
        ]
        
        for w in workshops_data:
            workshop = Workshop(**w)
            db.session.add(workshop)
        db.session.commit()
        
        # 7. Create Scholarships
        print("[IEMS] Seeding scholarships...")
        scholarships_data = [
            {
                "title": "CEM Merit-cum-Means Scholarship 2026",
                "description": "A financial aid program designed to support students with exceptional academic records who belong to economically weaker sections. Covers up to 75% of tuition fees.",
                "eligibility": "Minimum 8.5 CGPA in previous semesters and annual family income below Rs. 4.5 Lakhs.",
                "deadline": date.today() + timedelta(days=30),
                "application_link": "https://scholarship.cem.edu/mcm2026",
                "amount": "Up to Rs. 60,000 per year"
            },
            {
                "title": "Women in Tech Engineering Scholarship",
                "description": "An initiative to support and empower female students pursuing Bachelor of Technology (B.Tech) courses. Sponsored by leading tech corporations.",
                "eligibility": "Open to all female students in CS/IT/ECE branches with CGPA >= 7.5.",
                "deadline": date.today() + timedelta(days=18),
                "application_link": "https://scholarship.cem.edu/wit2026",
                "amount": "Rs. 50,000 per year and mentor access"
            },
            {
                "title": "Summer Research Grant 2025 (Expired)",
                "description": "Funding for students doing summer research internships at premier institutes (IITs, IISc, or international universities).",
                "eligibility": "Approved research proposal and invitation letter from host institution.",
                "deadline": date.today() - timedelta(days=90),
                "application_link": "https://scholarship.cem.edu/srg2025",
                "amount": "Rs. 25,000 one-time"
            }
        ]
        
        for s in scholarships_data:
            scholarship = Scholarship(**s)
            db.session.add(scholarship)
        db.session.commit()
        
        # 8. Create Opportunities
        print("[IEMS] Seeding opportunities...")
        opportunities_data = [
            {
                "title": "Software Engineer Intern",
                "company": "Google India",
                "type": "internship",
                "description": "Join Google's engineering team for a 10-12 week summer internship. Work on core services, search, cloud, or system tools. Gain hands-on exposure to massive-scale computing.",
                "deadline": date.today() + timedelta(days=20),
                "application_link": "https://careers.google.com/internships",
                "stipend": "Rs. 80,000/month",
                "location": "Bangalore / Hyderabad"
            },
            {
                "title": "Graduate Engineer Trainee",
                "company": "TechCorp Solutions",
                "type": "job",
                "description": "Full-time position for graduating students. Responsibilities include building scalable web backends, writing unit tests, and designing database models using Python and PostgreSQL.",
                "deadline": date.today() + timedelta(days=45),
                "application_link": "https://techcorp.example.com/careers/get2026",
                "stipend": "Rs. 8,50,000/annum",
                "location": "Noida / Remote"
            },
            {
                "title": "Smart Cities Innovation Fellowship",
                "company": "Ministry of Urban Development",
                "type": "fellowship",
                "description": "A 1-year prestigious fellowship program working with civic planners, data analysts, and software engineers to deploy smart traffic management solutions.",
                "deadline": date.today() + timedelta(days=15),
                "application_link": "https://smartcities.gov.in/fellowship",
                "stipend": "Rs. 40,000/month",
                "location": "New Delhi"
            },
            {
                "title": "National Algorithmic Coding Challenge",
                "company": "CodeArena",
                "type": "competition",
                "description": "An individual coding contest spanning 3 rounds. Top performers will get direct interview invites to top product companies.",
                "deadline": date.today() + timedelta(days=10),
                "application_link": "https://codearena.example.com/nacc2026",
                "stipend": "Prizes worth Rs. 5 Lakhs",
                "location": "Online"
            }
        ]
        
        for o in opportunities_data:
            opportunity = Opportunity(**o)
            db.session.add(opportunity)
        db.session.commit()
        
        # 9. Create CalendarEvents
        print("[IEMS] Seeding calendar events...")
        calendar_events_data = [
            {
                "title": "Odd Semester Commencement",
                "event_date": date.today() - timedelta(days=10),
                "category": "semester",
                "description": "Start of regular classes for academic year 2026-27."
            },
            {
                "title": "Independence Day Holiday",
                "event_date": date(2026, 8, 15),
                "category": "holiday",
                "description": "Independence Day of India. Flag hoisting ceremony in campus."
            },
            {
                "title": "Mid-Semester Examinations",
                "event_date": date.today() + timedelta(days=8),
                "end_date": date.today() + timedelta(days=14),
                "category": "exam",
                "description": "Mid-semester theory exams for all semesters."
            },
            {
                "title": "Annual Cultural Fest (Aura 2026)",
                "event_date": date.today() + timedelta(days=28),
                "end_date": date.today() + timedelta(days=30),
                "category": "event",
                "description": "Inter-college annual cultural festival with music, dance, fashion, and theater contests."
            }
        ]
        
        for ce in calendar_events_data:
            cal_event = CalendarEvent(**ce)
            db.session.add(cal_event)
        db.session.commit()
        
        # 10. Log some Activity
        print("[IEMS] Seeding activity logs...")
        activity_logs = [
            {
                "user_id": college_admin.id,
                "action": "LOGIN",
                "module": "Auth",
                "details": "College Admin logged in successfully.",
                "ip_address": "127.0.0.1",
                "timestamp": datetime.utcnow() - timedelta(hours=2)
            },
            {
                "user_id": college_admin.id,
                "action": "APPROVE_EVENT",
                "module": "Events",
                "details": "Approved event: Annual Hackathon (CEMHack 2026)",
                "ip_address": "127.0.0.1",
                "timestamp": datetime.utcnow() - timedelta(hours=1.5)
            },
            {
                "user_id": super_admin.id,
                "action": "CREATE_USER",
                "module": "Users",
                "details": "Created user account: college_admin@iems.edu",
                "ip_address": "127.0.0.1",
                "timestamp": datetime.utcnow() - timedelta(days=1)
            }
        ]
        
        for al in activity_logs:
            log = ActivityLog(**al)
            db.session.add(log)
        db.session.commit()
        
        print("[IEMS] Database seeded successfully!")
        print(f"[IEMS] Super Admin: admin@iems.edu / Admin@123")
        print(f"[IEMS] College Admin: college_admin@iems.edu / Admin@123")
        print(f"[IEMS] Coding President: coding@iems.edu / Admin@123")

if __name__ == '__main__':
    seed_db()
