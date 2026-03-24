"""
Management command to seed the database with sample data.
Usage:
  python manage.py seed
  python manage.py seed --clear   (wipe and re-seed)
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from notes_app.models import Unit, Student, Note, Group, Announcement


class Command(BaseCommand):
    help = 'Seed the database with initial IN16 class data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear', action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Announcement.objects.all().delete()
            Group.objects.all().delete()
            Note.objects.all().delete()
            Student.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            Unit.objects.all().delete()

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
        self.stdout.write(self.style.SUCCESS(f'✓ {len(units)} units'))

        # Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@in16.ac.ke', 'admin123')
            self.stdout.write(self.style.SUCCESS('✓ Superuser: admin / admin123'))

        # Students
        students_data = [
            ('IN16/00034/25', 'Kevin',   'Kiptoo',    'M'),
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
                student = Student.objects.create(
                    user=user, reg_number=reg, gender=gender
                )
                student_objects.append(student)
            else:
                try:
                    student_objects.append(Student.objects.get(reg_number=reg))
                except Student.DoesNotExist:
                    pass
        self.stdout.write(self.style.SUCCESS(
            f'✓ {len(student_objects)} students (password: pass1234)'
        ))

        # Notes
        notes_data = [
            (units[0], "Introduction to Operating Systems",
             "An OS manages hardware/software resources.\n\nFunctions:\n- Process management\n- Memory management\n- File system\n- I/O management\n- Security\n\nExamples: Linux, Windows, macOS"),
            (units[0], "Process Scheduling",
             "CPU scheduling algorithms:\n1. FCFS\n2. SJF\n3. Round Robin\n4. Priority Scheduling\n\nMetrics: throughput, turnaround time, waiting time, response time."),
            (units[1], "Number Systems",
             "Systems: Binary (2), Octal (8), Decimal (10), Hex (16).\n\nConversions and two's complement are key exam topics."),
            (units[2], "SDLC Phases",
             "1. Requirements\n2. Design\n3. Implementation\n4. Testing\n5. Deployment\n6. Maintenance\n\nModels: Waterfall, Agile, Spiral, V-Model"),
            (units[3], "Pointers in C",
             "int *ptr;\nptr = &variable;\n*ptr = 10;\n\nUses: dynamic memory, arrays, linked lists."),
            (units[4], "Limits & Continuity",
             "lim(x→a) f(x) = L\n\nContinuity requires:\n1. f(a) defined\n2. limit exists\n3. limit = f(a)"),
        ]
        for unit, topic, content in notes_data:
            Note.objects.get_or_create(
                unit=unit, topic=topic, defaults={'content': content}
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(notes_data)} notes'))

        # Groups
        if student_objects:
            g1, _ = Group.objects.get_or_create(name="Group A - OS", unit=units[0])
            g1.members.set(student_objects[:2])
            g2, _ = Group.objects.get_or_create(name="Group B - Architecture", unit=units[1])
            g2.members.set(student_objects)
            self.stdout.write(self.style.SUCCESS('✓ 2 groups'))

        # Announcements
        ann_data = [
            ("Welcome to IN16 Study Manager",
             "Welcome to the official IN16 class study management platform. Use this system to access notes, connect with your group, and stay updated. Best of luck this semester!"),
            ("CAT 1 Schedule Released",
             "CAT 1 schedules are out. Check your unit timetables. CATs begin Week 6."),
            ("Group Assignments Posted",
             "Study group assignments are live. Check the Groups section."),
        ]
        for title, content in ann_data:
            Announcement.objects.get_or_create(
                title=title, defaults={'content': content}
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(ann_data)} announcements'))

        self.stdout.write(self.style.SUCCESS(
            '\nDatabase seeded! Login credentials:\n'
            '  Admin    : admin / admin123\n'
            '  Student  : kevinkiptoo / pass1234\n'
            '  Student  : lynettechepkemoi / pass1234'
        ))
