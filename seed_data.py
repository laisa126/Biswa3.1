"""
Run this after migrations to seed sample data:
  python manage.py shell < seed_data.py
  OR
  python seed_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IN16_Study_Manager.settings')
django.setup()

from django.contrib.auth.models import User
from notes_app.models import Unit, Student, Note, Group, Announcement

print("Seeding data...")

# Units
units_data = [
    "Operating Systems (COMP113)",
    "Computer Architecture (COMP100)",
    "System Analysis and Design (SOEN112)",
    "Structure Programming in C (SOEN102)",
    "Calculus 1 (MATH111)",
    "Introductory Electronics (PHY213)",
]
units = []
for u in units_data:
    unit, _ = Unit.objects.get_or_create(name=u)
    units.append(unit)
print(f"  ✓ {len(units)} units")

# Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@in16.ac.ke', 'admin123')
    print("  ✓ Superuser: admin / admin123")

# Sample students
students_data = [
    ('IN16/00034/25', 'Kevin', 'Kiptoo', 'M'),
    ('IN16/00031/25', 'Lynette', 'Chepkemoi', 'F'),
]
student_objects = []
for reg, first, last, gender in students_data:
    username = first.lower() + last.lower()
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username, f'{first.lower()}@in16.ac.ke', 'pass1234',
            first_name=first, last_name=last
        )
        student = Student.objects.create(user=user, reg_number=reg, gender=gender)
        student_objects.append(student)
    else:
        try:
            student_objects.append(Student.objects.get(reg_number=reg))
        except Student.DoesNotExist:
            pass
print(f"  ✓ {len(student_objects)} students (password: pass1234)")

# Notes
notes_data = [
    (units[0], "Introduction to Operating Systems",
     "An operating system (OS) is system software that manages computer hardware and software resources.\n\nKey functions:\n- Process management\n- Memory management\n- File system management\n- I/O management\n- Security and access control\n\nExamples: Linux, Windows, macOS, Android"),
    (units[0], "Process Scheduling Algorithms",
     "CPU scheduling determines which process runs next.\n\nAlgorithms:\n1. FCFS (First Come First Served)\n2. SJF (Shortest Job First)\n3. Round Robin (with time quantum)\n4. Priority Scheduling\n5. Multilevel Queue\n\nKey metrics: throughput, turnaround time, waiting time, response time."),
    (units[1], "Number Systems & Data Representation",
     "Computers use binary (base 2) internally.\n\nNumber systems:\n- Binary (base 2): 0, 1\n- Octal (base 8): 0-7\n- Decimal (base 10): 0-9\n- Hexadecimal (base 16): 0-9, A-F\n\nConversions and two's complement for signed integers are core exam topics."),
    (units[2], "SDLC Phases",
     "Software Development Life Cycle phases:\n1. Requirements gathering\n2. System design\n3. Implementation (coding)\n4. Testing\n5. Deployment\n6. Maintenance\n\nModels: Waterfall, Agile, Spiral, V-Model"),
    (units[3], "Pointers in C",
     "A pointer stores the memory address of another variable.\n\nDeclaration: int *ptr;\nAssignment: ptr = &variable;\nDereference: *ptr = 10;\n\nCommon uses:\n- Dynamic memory allocation (malloc/free)\n- Passing arrays to functions\n- Building linked lists and trees"),
    (units[4], "Limits and Continuity",
     "A limit describes the value a function approaches as input approaches a point.\n\nlim(x→a) f(x) = L\n\nContinuity: f is continuous at a if:\n1. f(a) is defined\n2. lim(x→a) f(x) exists\n3. lim(x→a) f(x) = f(a)\n\nDifferentiability implies continuity (but not vice versa)."),
]
for unit, topic, content in notes_data:
    Note.objects.get_or_create(unit=unit, topic=topic, defaults={'content': content})
print(f"  ✓ {len(notes_data)} notes")

# Groups
if student_objects:
    g1, _ = Group.objects.get_or_create(name="Group A - OS", unit=units[0])
    g1.members.set(student_objects[:2])
    g2, _ = Group.objects.get_or_create(name="Group B - Architecture", unit=units[1])
    g2.members.set(student_objects)
    print("  ✓ 2 groups")

# Announcements
ann_data = [
    ("Welcome to IN16 Study Manager",
     "Welcome to the official IN16 class study management platform. Use this system to access notes, connect with your group, and stay updated with class announcements. Best of luck this semester!"),
    ("CAT 1 Schedule Released",
     "The Continuous Assessment Test 1 schedule has been released. Please check your unit timetables and prepare accordingly. CATs will begin in Week 6."),
    ("Group Assignments Posted",
     "Study group assignments for all units have been posted. Please check the Groups section to see your assigned group members."),
]
for title, content in ann_data:
    Announcement.objects.get_or_create(title=title, defaults={'content': content})
print(f"  ✓ {len(ann_data)} announcements")

print("\nDone! Credentials:")
print("  Admin panel : /admin/   →  admin / admin123")
print("  Student     : kevinkiptoo / pass1234")
print("  Student     : lynettechepkemoi / pass1234")
