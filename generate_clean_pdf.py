import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from PIL import Image as PILImage

class PlainNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 10)
        self.setFillColor(colors.black)

        # Draw page number at top-left like reference PDF
        self.drawString(54, 842 - 36, str(self._pageNumber))

        # On Page 1, draw the neat outer border rectangle
        if self._pageNumber == 1:
            self.setStrokeColor(colors.black)
            self.setLineWidth(1)
            self.rect(38, 38, 595.27 - 76, 841.89 - 76)

        self.restoreState()

def build_pdf():
    pdf_filename = "Restaurant_Table_Reservation_System_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Plain styles matching reference report
    title_bold = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        alignment=1,
        textColor=colors.black
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True,
        textColor=colors.black
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
        textColor=colors.black
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        spaceAfter=5,
        textColor=colors.black
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.black
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        alignment=1,
        spaceBefore=4,
        spaceAfter=10,
        textColor=colors.black
    )

    cell_style = ParagraphStyle(
        'Cell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.black
    )

    cell_bold = ParagraphStyle(
        'CellBold',
        parent=cell_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE & COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>SRI SIVASUBRAMANIYA NADAR COLLEGE OF ENGINEERING</b>", title_bold))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Department of Information Technology</b>", ParagraphStyle('Sub', parent=title_bold, fontSize=12, leading=16)))
    story.append(Spacer(1, 25))

    course_table_data = [
        [Paragraph("<b>Course Code</b>", cell_bold), Paragraph("UIT3361", cell_style)],
        [Paragraph("<b>Course Name</b>", cell_bold), Paragraph("OBJECT-ORIENTED PROGRAMMING USING JAVA", cell_style)],
        [Paragraph("<b>Regulation</b>", cell_bold), Paragraph("2024", cell_style)],
        [Paragraph("<b>Academic Year</b>", cell_bold), Paragraph("2026-2027", cell_style)],
        [Paragraph("<b>Degree and Branch</b>", cell_bold), Paragraph("B.Tech Information Technology", cell_style)],
        [Paragraph("<b>Semester</b>", cell_bold), Paragraph("III", cell_style)]
    ]
    t_course = Table(course_table_data, colWidths=[150, 310])
    t_course.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_course)

    story.append(Spacer(1, 55))
    story.append(Paragraph("<b>ASSIGNMENT</b>", ParagraphStyle('Assign', parent=title_bold, fontSize=14, leading=18)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>RESTAURANT TABLE RESERVATION SYSTEM</b>", ParagraphStyle('ProjTitle', parent=title_bold, fontSize=16, leading=22)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<i>A Java Swing desktop application connected to a MySQL database using JDBC</i>", ParagraphStyle('SubItalic', parent=title_bold, fontName='Helvetica-Oblique', fontSize=10, leading=14)))

    story.append(Spacer(1, 65))
    story.append(Paragraph("<b>Submitted by</b>", ParagraphStyle('SubBy', parent=title_bold, fontSize=11, leading=15)))
    story.append(Spacer(1, 10))

    students_data = [
        [Paragraph("<b>S.No</b>", cell_bold), Paragraph("<b>Student Name</b>", cell_bold), Paragraph("<b>Register Number</b>", cell_bold)],
        [Paragraph("1", cell_style), Paragraph("GOKUL HARI RAJAN R", cell_style), Paragraph("3122255002037", cell_style)],
        [Paragraph("2", cell_style), Paragraph("DHARSHAN SATHISH KUMAR", cell_style), Paragraph("3122255002029", cell_style)],
        [Paragraph("3", cell_style), Paragraph("DHARSHINI PK", cell_style), Paragraph("3122255002030", cell_style)],
        [Paragraph("4", cell_style), Paragraph("DHESH SARVAJITH R", cell_style), Paragraph("3122255002031", cell_style)]
    ]
    t_students = Table(students_data, colWidths=[40, 260, 160])
    t_students.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_students)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: 1. SYSTEM REQUIREMENTS & 2. SYSTEM DESIGN
    # =========================================================================
    story.append(Paragraph("1. System Requirements", h1_style))
    story.append(Paragraph("Our project is a desktop application. It runs on a normal laptop or desktop computer. The same computer also runs the MySQL database. The tables below show the hardware and software we used.", body_style))
    
    story.append(Paragraph("1.1 Hardware Requirements", h2_style))
    hw_data = [
        [Paragraph("Component", cell_bold), Paragraph("Minimum", cell_bold), Paragraph("Recommended", cell_bold)],
        [Paragraph("Processor", cell_style), Paragraph("Dual-core, 2.0 GHz (64-bit)", cell_style), Paragraph("Quad-core, 2.5 GHz or faster", cell_style)],
        [Paragraph("RAM", cell_style), Paragraph("4 GB", cell_style), Paragraph("8 GB or more (MySQL and the code editor run together)", cell_style)],
        [Paragraph("Hard disk", cell_style), Paragraph("10 GB free space", cell_style), Paragraph("20 GB free space on an SSD", cell_style)],
        [Paragraph("Screen", cell_style), Paragraph("1280 × 720", cell_style), Paragraph("1366 × 768 or higher", cell_style)],
        [Paragraph("Input devices", cell_style), Paragraph("Keyboard and mouse", cell_style), Paragraph("Keyboard and mouse", cell_style)],
        [Paragraph("Printer", cell_style), Paragraph("Not needed", cell_style), Paragraph("Any printer, to print reservation slips", cell_style)],
    ]
    t_hw = Table(hw_data, colWidths=[100, 160, 200])
    t_hw.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_hw)
    story.append(Spacer(1, 4))

    story.append(Paragraph("1.2 Software Requirements", h2_style))
    sw_data = [
        [Paragraph("Software", cell_bold), Paragraph("Version used", cell_bold), Paragraph("Why we need it", cell_bold)],
        [Paragraph("Operating system", cell_style), Paragraph("Windows 10 / 11 (64-bit)", cell_style), Paragraph("To run the application (it also works on Linux and macOS)", cell_style)],
        [Paragraph("Java Development Kit", cell_style), Paragraph("JDK 21", cell_style), Paragraph("To compile and run the Java code", cell_style)],
        [Paragraph("GUI toolkit", cell_style), Paragraph("Java Swing (comes with the JDK)", cell_style), Paragraph("To build the windows, forms, buttons and tables", cell_style)],
        [Paragraph("Database", cell_style), Paragraph("MySQL Server 8.0 / 8.4", cell_style), Paragraph("To store tables, customers, reservations and users", cell_style)],
        [Paragraph("JDBC driver", cell_style), Paragraph("MySQL Connector/J (mysql-connector-j-9.7.0.jar)", cell_style), Paragraph("To connect the Java program to MySQL", cell_style)],
        [Paragraph("Database tool", cell_style), Paragraph("MySQL Workbench / CLI", cell_style), Paragraph("To run the database setup script and verify tables", cell_style)],
        [Paragraph("Code editor", cell_style), Paragraph("Eclipse IDE / VS Code", cell_style), Paragraph("To write, build and run the code", cell_style)],
        [Paragraph("Version control", cell_style), Paragraph("Git and GitHub", cell_style), Paragraph("To share the code within our team", cell_style)],
    ]
    t_sw = Table(sw_data, colWidths=[100, 150, 210])
    t_sw.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_sw)
    story.append(Spacer(1, 4))

    story.append(Paragraph("1.3 Setup in Short", h2_style))
    story.append(Paragraph("• The database connection URL, username and password are kept inside <code>util/DBConnection.java</code> connecting to <code>restaurant_db</code>.", bullet_style))
    story.append(Paragraph("• The JDBC library file (<code>mysql-connector-j-9.7.0.jar</code>) is included in the project classpath.", bullet_style))
    story.append(Paragraph("• The program starts from the class <code>Main.java</code>, which checks MySQL connectivity and launches the authentication window.", bullet_style))

    story.append(Paragraph("2. System Design", h1_style))
    story.append(Paragraph("2.1 Overall Architecture", h2_style))
    story.append(Paragraph("We built the project in layers, and each layer has one job. The screens never talk to the database directly. A screen asks a DAO (Data Access Object) class for data. The DAO class talks to the MySQL database through JDBC and gives the result back to the screen. This keeps the code clean and easy to change.", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: 2.1 ARCHITECTURE DIAGRAM & LAYER TABLE & 2.2 HOW WORK TOGETHER
    # =========================================================================
    if os.path.exists("layers_of_the_application.png"):
        story.append(Image("layers_of_the_application.png", width=460, height=260))
    story.append(Paragraph("<i>Figure 2.1 – Layers of the application</i>", caption_style))
    story.append(Spacer(1, 4))

    layer_data = [
        [Paragraph("Layer (package)", cell_bold), Paragraph("Main classes", cell_bold), Paragraph("What it does", cell_bold)],
        [Paragraph("Screens (gui)", cell_style), Paragraph("MainFrame, AuthPanel, AdminDashboardPanel, CustomerDashboardPanel, ReservationDialog, TablesDialog, SearchReservationDialog, ModifyReservationDialog, CancelReservationDialog", cell_style), Paragraph("Shows windows and forms, handles button clicks and shows messages", cell_style)],
        [Paragraph("Rules (util)", cell_style), Paragraph("ValidationUtil, PasswordUtil, UserSession, DBConnection", cell_style), Paragraph("Checks user input, protects passwords with salt+hash, and remembers who is logged in", cell_style)],
        [Paragraph("Database access (dao)", cell_style), Paragraph("TableDAO, CustomerDAO, ReservationDAO, UserDAO", cell_style), Paragraph("Holds all the SQL code and talks to the MySQL database", cell_style)],
        [Paragraph("Data objects (model)", cell_style), Paragraph("RestaurantTable, Customer, Reservation, ReservationDetail, User", cell_style), Paragraph("Simple objects that carry data between the layers", cell_style)],
        [Paragraph("Database", cell_style), Paragraph("MySQL tables: restaurant_tables, customers, reservations, users", cell_style), Paragraph("Stores all the dining and reservation data permanently", cell_style)],
    ]
    t_layer = Table(layer_data, colWidths=[100, 180, 180])
    t_layer.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_layer)

    story.append(Paragraph("2.2 How the Screens and the Database Work Together", h2_style))
    story.append(Paragraph("Every action in the application follows the same simple path. For example, this is what happens when a user books a table:", body_style))
    story.append(Paragraph("1. The user clicks the Confirm Booking button. An event listener in the screen catches the click.", bullet_style))
    story.append(Paragraph("2. The screen checks the input using the ValidationUtil class. If something is wrong, a red message appears and nothing is saved.", bullet_style))
    story.append(Paragraph("3. If the input is correct, the screen calls a DAO method, for example <code>ReservationDAO.bookReservation()</code>.", bullet_style))
    story.append(Paragraph("4. The DAO opens a database connection and runs the SQL using a PreparedStatement inside a transaction.", bullet_style))
    story.append(Paragraph("5. The DAO turns the database result into Java objects and returns them to the screen.", bullet_style))
    story.append(Paragraph("6. The screen updates its table or shows a success message with the new reservation ID to the user.", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: 2.3 USERS, 2.4 DB DESIGN, 2.5 LIFE OF BOOKING, 3. CORE MODULES
    # =========================================================================
    story.append(Paragraph("2.3 Two Types of Users", h2_style))
    story.append(Paragraph("Both types of users sign in from the same login window. After login, each user sees only the screens meant for them.", body_style))

    user_data = [
        [Paragraph("User", cell_bold), Paragraph("Screen they see", cell_bold), Paragraph("What they can do", cell_bold)],
        [Paragraph("Admin (restaurant staff)", cell_style), Paragraph("Admin Operations Dashboard", cell_style), Paragraph("See free tables, book tables for walk-in guests, view live stats, search, change or cancel any booking, and check real-time slot availability", cell_style)],
        [Paragraph("Customer", cell_style), Paragraph("Customer Portal Dashboard", cell_style), Paragraph("Create an account, view free tables, book a table with prefilled details, see their own bookings, and cancel their own upcoming bookings", cell_style)]
    ]
    t_user = Table(user_data, colWidths=[90, 130, 240])
    t_user.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_user)

    story.append(Paragraph("2.4 Database Design", h2_style))
    story.append(Paragraph("The database has four tables. We do not store whether a table is permanently free. Instead, the program checks reservations for the chosen date and time slot. A table is free if no active booking occupies that slot.", body_style))

    db_data = [
        [Paragraph("Table", cell_bold), Paragraph("Important columns", cell_bold), Paragraph("What it stores", cell_bold)],
        [Paragraph("restaurant_tables", cell_style), Paragraph("table_id (PK), table_number, capacity, status", cell_style), Paragraph("The 8 dining tables: Table 1 to 2 (2 seats), Table 3 to 5 (4 seats), Table 6 to 7 (6 seats), Table 8 (8 seats)", cell_style)],
        [Paragraph("customers", cell_style), Paragraph("customer_id (PK), name, phone, email", cell_style), Paragraph("Guest contact information. Each customer has an ID, name, 10-digit phone and email.", cell_style)],
        [Paragraph("reservations", cell_style), Paragraph("reservation_id (PK), customer_id (FK), table_id (FK), reservation_date, reservation_time, guests, status", cell_style), Paragraph("One row for every table reservation. The status is BOOKED, COMPLETED or CANCELLED.", cell_style)],
        [Paragraph("users", cell_style), Paragraph("user_id (PK), username, password_hash, salt, full_name, role, customer_id (FK)", cell_style), Paragraph("Admin and customer login accounts. Passwords are stored in a safe, hashed form with salt.", cell_style)],
    ]
    t_db = Table(db_data, colWidths=[90, 160, 210])
    t_db.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_db)

    story.append(Paragraph("The database itself also checks key integrity rules:", body_style))
    story.append(Paragraph("• Foreign keys connect reservations to customers and tables, preventing invalid links.", bullet_style))
    story.append(Paragraph("• Status of a reservation can only be BOOKED, COMPLETED or CANCELLED.", bullet_style))
    story.append(Paragraph("• Each table has a defined seating capacity (2 to 8 guests).", bullet_style))

    story.append(Paragraph("2.5 Life of a Booking", h2_style))
    story.append(Paragraph("A reservation is never deleted during normal operations. It starts as BOOKED. When guests finish dining, staff can set it to COMPLETED. If cancelled, its status changes to CANCELLED. Only active BOOKED reservations block a table slot, so old bookings never stop a new guest from reserving the table for another date or time.", body_style))

    story.append(Paragraph("3. Core Modules Implemented", h1_style))
    story.append(Paragraph("The application has eleven core modules. The table below shows which module covers each part of the problem statement.", body_style))

    mod_data = [
        [Paragraph("Requirement in the problem statement", cell_bold), Paragraph("Covered by", cell_bold)],
        [Paragraph("View available dining tables", cell_style), Paragraph("Module 3.2 – Table Availability", cell_style)],
        [Paragraph("Enter customer details & party size", cell_style), Paragraph("Module 3.3 – Booking", cell_style)],
        [Paragraph("Make an atomic table reservation", cell_style), Paragraph("Module 3.3 – Booking", cell_style)],
        [Paragraph("Search for an existing reservation", cell_style), Paragraph("Module 3.4 – Search", cell_style)],
        [Paragraph("Modify reservation details", cell_style), Paragraph("Module 3.5 – Modify Booking", cell_style)],
        [Paragraph("Cancel an active reservation", cell_style), Paragraph("Module 3.6 – Cancel Booking", cell_style)],
        [Paragraph("Admin operations & metrics", cell_style), Paragraph("Module 3.7 – Admin Dashboard", cell_style)],
        [Paragraph("Customer personal portal", cell_style), Paragraph("Module 3.8 – Customer Screens", cell_style)],
        [Paragraph("GUI with event handling and validation", cell_style), Paragraph("All screens, and Module 3.9 – Validation and Design", cell_style)],
        [Paragraph("JDBC with a relational database", cell_style), Paragraph("Section 4 and all DAO classes", cell_style)],
    ]
    t_mod = Table(mod_data, colWidths=[230, 230])
    t_mod.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_mod)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: 3.1 LOGIN & REG, 3.2 TABLE AVAILABILITY, 3.3 BOOKING
    # =========================================================================
    story.append(Paragraph("3.1 Login and Registration", h2_style))
    story.append(Paragraph("<b>Classes:</b> AuthPanel, UserDAO, PasswordUtil, UserSession, User", body_style))
    story.append(Paragraph("• The login window has two segmented tabs: Sign In and Create Account.", bullet_style))
    story.append(Paragraph("• After a correct login, an admin goes to the Admin Dashboard and a customer goes to the Customer Portal.", bullet_style))
    story.append(Paragraph("• While registering, every field is checked: full name, unique username, 10-digit phone number, email, password and password confirmation. Wrong fields show a clear error message.", bullet_style))
    story.append(Paragraph("• Passwords are never saved as plain text. We add a random salt and save only the SHA-256 hash.", bullet_style))
    story.append(Paragraph("• The first time the program runs, it creates a default admin account (<code>admin / admin123</code>).", bullet_style))

    story.append(Paragraph("3.2 Table Availability", h2_style))
    story.append(Paragraph("<b>Classes:</b> TablesDialog, TableDAO, RestaurantTable", body_style))
    story.append(Paragraph("• The user selects a date and a time slot. The list of tables updates straight away.", bullet_style))
    story.append(Paragraph("• Only tables with no active booking for that exact slot are shown as AVAILABLE (Free). Booked tables are marked BOOKED (Occupied) in red.", bullet_style))
    story.append(Paragraph("• Tables are never permanently marked busy; availability is calculated dynamically per slot so guests can reserve ahead for future slots.", bullet_style))
    story.append(Paragraph("• Displays each table's number and maximum guest capacity (2, 4, 6 or 8 guests).", bullet_style))

    story.append(Paragraph("3.3 Booking (Entering Customer Details)", h2_style))
    story.append(Paragraph("<b>Classes:</b> ReservationDialog, ReservationDAO, CustomerDAO, TableDAO", body_style))
    story.append(Paragraph("• The booking form collects guest name, contact phone number, email, party size, date and time.", bullet_style))
    story.append(Paragraph("• For logged-in customers, their name, phone number and email are filled in automatically.", bullet_style))
    story.append(Paragraph("• Clicking Find Tables queries the database and populates only tables large enough for the party that are free at that slot.", bullet_style))
    story.append(Paragraph("• When the user clicks Confirm Booking, all details are checked again, including whether the table is still free.", bullet_style))
    story.append(Paragraph("• The customer row and reservation row are saved atomically in one transaction, so partial bookings can never occur.", bullet_style))
    story.append(Paragraph("• The user is shown the confirmed reservation ID.", bullet_style))

    story.append(Paragraph("3.4 Search", h2_style))
    story.append(Paragraph("<b>Classes:</b> SearchReservationDialog, ReservationDAO, ReservationListPanel", body_style))
    story.append(Paragraph("• Allows searching by Reservation ID, Customer Name, or Phone Number.", bullet_style))
    story.append(Paragraph("• Safe parameterized queries prevent SQL injection.", bullet_style))
    story.append(Paragraph("• Results appear in a clear table showing reservation ID, customer name, phone, table number, date, time and status.", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: 3.5 MODIFY, 3.6 CANCEL, 3.7 ADMIN DASHBOARD, 3.8 CUSTOMER SCREENS
    # =========================================================================
    story.append(Paragraph("3.5 Modify Booking", h2_style))
    story.append(Paragraph("<b>Classes:</b> ModifyReservationDialog, ReservationDAO, TableDAO", body_style))
    story.append(Paragraph("• An existing reservation is selected from the list, loading its date, time, table, guest count and status into editing fields.", bullet_style))
    story.append(Paragraph("• Before saving, the system checks whether the new table is free for the new date and time slot, ignoring the current reservation ID during conflict checks.", bullet_style))
    story.append(Paragraph("• Once confirmed, an SQL UPDATE updates the record and refreshes the schedule.", bullet_style))

    story.append(Paragraph("3.6 Cancel Booking", h2_style))
    story.append(Paragraph("<b>Classes:</b> CancelReservationDialog, CustomerDashboardPanel, ReservationDAO", body_style))
    story.append(Paragraph("• The program asks for user confirmation before cancelling a booking.", bullet_style))
    story.append(Paragraph("• Soft cancellation: sets the status to CANCELLED so that the booking history is preserved while immediately freeing the table slot.", bullet_style))
    story.append(Paragraph("• Admins also have the option to permanently delete a record if necessary.", bullet_style))
    story.append(Paragraph("• Customers can cancel their own active bookings directly from their portal.", bullet_style))

    story.append(Paragraph("3.7 Admin Dashboard", h2_style))
    story.append(Paragraph("<b>Classes:</b> AdminDashboardPanel, MainFrame", body_style))
    story.append(Paragraph("• Four metric cards show live system numbers: Total Tables (8), Active Bookings, Today's Scheduled Reservations, and Total Registered Customers.", bullet_style))
    story.append(Paragraph("• Quick action buttons open every administrative task: New Booking, View/Filter, Search, Modify, Cancel/Delete, Table Availability, and Refresh Data.", bullet_style))
    story.append(Paragraph("• An embedded live table displays recent system reservations with status filter (All, BOOKED, COMPLETED, CANCELLED).", bullet_style))

    story.append(Paragraph("3.8 Customer Screens", h2_style))
    story.append(Paragraph("<b>Classes:</b> CustomerDashboardPanel, MainFrame", body_style))
    story.append(Paragraph("• Personalized greeting and stat cards showing the customer's active bookings, total reservations made, and registered contact phone.", bullet_style))
    story.append(Paragraph("• Action buttons to reserve a table, browse available tables, cancel a selected reservation, and refresh history.", bullet_style))
    story.append(Paragraph("• Displays only the logged-in customer's own booking history, ensuring privacy.", bullet_style))

    story.append(Paragraph("3.9 Validation and Design", h2_style))
    story.append(Paragraph("<b>Classes:</b> ValidationUtil, GUITheme", body_style))
    story.append(Paragraph("• ValidationUtil centralizes all validation rules: phone format (10-15 digits), email format, date parsing, past slot prevention, and guest count within table capacity.", bullet_style))
    story.append(Paragraph("• GUITheme provides clean fonts, colors, rounded buttons, styled tables and stat cards across all screens.", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: 4. JDBC CONNECTIVITY & OPERATIONS
    # =========================================================================
    story.append(Paragraph("4. JDBC Connectivity", h1_style))
    story.append(Paragraph("JDBC (Java Database Connectivity) lets a Java program talk to a database. Our project uses the MySQL Connector/J driver (<code>mysql-connector-j-9.7.0.jar</code>) to connect to MySQL Server. All database code is kept in the <code>dao</code> package. Every query uses a PreparedStatement, which keeps user input separate from the SQL and protects the database from SQL injection.", body_style))

    story.append(Paragraph("4.1 Steps to Connect to the Database", h2_style))
    story.append(Paragraph("1. Load the driver: The MySQL Connector/J driver class is registered automatically by JDBC 4.x service provider mechanisms.", bullet_style))
    story.append(Paragraph("2. Read login details: The URL, username (<code>root</code>) and password are kept inside <code>DBConnection.java</code>.", bullet_style))
    story.append(Paragraph("3. Open a connection: <code>DriverManager.getConnection(URL, USER, PASSWORD)</code> gives a Connection object.", bullet_style))
    story.append(Paragraph("4. Prepare and run the SQL: We create a PreparedStatement, bind values with <code>setString()</code>, <code>setInt()</code>, <code>setDate()</code> and <code>setTime()</code>, and execute it.", bullet_style))
    story.append(Paragraph("5. Read the results: The ResultSet is read row by row and converted into Java model objects.", bullet_style))
    story.append(Paragraph("6. Close everything: We use try-with-resources, so connections, statements and result sets close automatically.", bullet_style))

    conn_table = [
        [Paragraph("Setting", cell_bold), Paragraph("Value", cell_bold)],
        [Paragraph("Driver class", cell_style), Paragraph("com.mysql.cj.jdbc.Driver", cell_style)],
        [Paragraph("Connection URL", cell_style), Paragraph("jdbc:mysql://localhost:3306/restaurant_db", cell_style)],
        [Paragraph("Database user", cell_style), Paragraph("root", cell_style)],
        [Paragraph("Quick connection test", cell_style), Paragraph("Run Main.java – checks connection.isValid(3) on boot before opening GUI", cell_style)]
    ]
    t_conn = Table(conn_table, colWidths=[140, 320])
    t_conn.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_conn)
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.2 Database Operations Used", h2_style))
    ops_data = [
        [Paragraph("Operation", cell_bold), Paragraph("Where it is used", cell_bold), Paragraph("What the SQL does", cell_bold)],
        [Paragraph("INSERT", cell_style), Paragraph("Customer registration, adding a customer, booking a table", cell_style), Paragraph("Adds a new row to customers, users or reservations", cell_style)],
        [Paragraph("SELECT", cell_style), Paragraph("Checking table slot availability", cell_style), Paragraph("Finds tables that have no active booking on the chosen date and time slot", cell_style)],
        [Paragraph("SELECT with JOIN", cell_style), Paragraph("Admin reservation list, search, customer bookings", cell_style), Paragraph("Joins reservations, customers and restaurant_tables to display full names and table numbers", cell_style)],
        [Paragraph("SELECT with LIKE", cell_style), Paragraph("Search screen", cell_style), Paragraph("Finds reservations matching partial customer name or phone number", cell_style)],
        [Paragraph("SELECT", cell_style), Paragraph("Login", cell_style), Paragraph("Finds user by username, then Java compares the salted password hash", cell_style)],
        [Paragraph("UPDATE", cell_style), Paragraph("Modify reservation", cell_style), Paragraph("Changes table, date, time slot, guest count or status of an active booking", cell_style)],
        [Paragraph("UPDATE", cell_style), Paragraph("Cancel reservation", cell_style), Paragraph("Changes the reservation status to CANCELLED", cell_style)],
        [Paragraph("DELETE", cell_style), Paragraph("Delete reservation", cell_style), Paragraph("Permanently deletes a reservation row", cell_style)],
        [Paragraph("COUNT", cell_style), Paragraph("Dashboard numbers", cell_style), Paragraph("Counts total tables, active bookings, today's reservations and registered customers", cell_style)],
    ]
    t_ops = Table(ops_data, colWidths=[90, 150, 220])
    t_ops.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_ops)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: 4.3 TRANSACTIONS, 4.4 HANDLING ERRORS, 5. CODE SNIPPETS
    # =========================================================================
    story.append(Paragraph("4.3 Transactions (Keeping Data Safe)", h2_style))
    story.append(Paragraph("Making a booking writes to two tables: customers and reservations. Both changes must be saved together, or not at all. So we use a transaction:", body_style))
    story.append(Paragraph("1. <code>conn.setAutoCommit(false)</code> starts the transaction.", bullet_style))
    story.append(Paragraph("2. The customer row is inserted, and the new customer ID is read using <code>getGeneratedKeys()</code>.", bullet_style))
    story.append(Paragraph("3. The reservation row is inserted with the new customer ID and chosen table ID.", bullet_style))
    story.append(Paragraph("4. <code>conn.commit()</code> saves both changes together.", bullet_style))
    story.append(Paragraph("5. If anything goes wrong, <code>conn.rollback()</code> cancels all changes so no orphaned customer row is left.", bullet_style))

    story.append(Paragraph("4.4 Handling Errors", h2_style))
    story.append(Paragraph("• Every DAO method handles SQLExceptions gracefully, logging details and returning safe values.", bullet_style))
    story.append(Paragraph("• The screen shows user-friendly error dialogs instead of raw technical stack traces.", bullet_style))
    story.append(Paragraph("• If MySQL is not running on startup, Main.java catches the connection failure and warns the user before opening the GUI.", bullet_style))

    story.append(Paragraph("5. Code Snippets", h1_style))
    story.append(Paragraph("This section shows the most important parts of our code. Each snippet has a short note that explains what it does.", body_style))

    story.append(Paragraph("5.1 Connecting to the Database (DBConnection.java)", h2_style))
    story.append(Paragraph("The database connection is created using DriverManager. Every DAO class gets its connection from this helper method.", body_style))

    snippet_conn = """public class DBConnection {
    private static final String URL = "jdbc:mysql://localhost:3306/restaurant_db";
    private static final String USER = "root";
    private static final String PASSWORD = "Gokul@1612";

    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }
}"""
    story.append(Paragraph(f"<pre>{snippet_conn}</pre>", code_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: 5.2 AVAILABILITY, 5.3 TRANSACTIONAL BOOKING
    # =========================================================================
    story.append(Paragraph("5.2 Finding Free Tables for the Chosen Slot (TableDAO.java)", h2_style))
    story.append(Paragraph("A table is available only if no non-cancelled reservation exists for that table at the chosen date and time slot.", body_style))

    snippet_avail = """public List<RestaurantTable> getAvailableTables(LocalDate date, LocalTime time,
                                                int minCapacity, int excludeReservationId) throws SQLException {
    String sql = \"\"\"
        SELECT t.* FROM restaurant_tables t
        WHERE t.capacity >= ?
          AND NOT EXISTS (
              SELECT 1 FROM reservations r
              WHERE r.table_id = t.table_id
                AND r.reservation_date = ?
                AND r.reservation_time = ?
                AND r.status <> 'CANCELLED'
                AND r.reservation_id <> ?
          )
        ORDER BY t.table_number\"\"\";

    try (Connection conn = DBConnection.getConnection();
         PreparedStatement ps = conn.prepareStatement(sql)) {
        ps.setInt(1, minCapacity);
        ps.setDate(2, Date.valueOf(date));
        ps.setTime(3, Time.valueOf(time));
        ps.setInt(4, excludeReservationId);
        try (ResultSet rs = ps.executeQuery()) {
            List<RestaurantTable> tables = new ArrayList<>();
            while (rs.next()) {
                tables.add(new RestaurantTable(
                    rs.getInt("table_id"), rs.getInt("table_number"),
                    rs.getInt("capacity"), rs.getString("status")));
            }
            return tables;
        }
    }
}"""
    story.append(Paragraph(f"<pre>{snippet_avail}</pre>", code_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("5.3 Saving a Booking in One Transaction (ReservationDAO.java)", h2_style))
    story.append(Paragraph("Customer and reservation details are saved inside one database transaction. If anything fails, everything is rolled back.", body_style))

    snippet_book = """public int bookReservation(Customer customer, Reservation reservation) throws SQLException {
    try (Connection conn = DBConnection.getConnection()) {
        boolean autoCommit = conn.getAutoCommit();
        conn.setAutoCommit(false);
        try {
            int customerId;
            try (PreparedStatement ps = conn.prepareStatement(insertCustomer, Statement.RETURN_GENERATED_KEYS)) {
                ps.setString(1, customer.getName());
                ps.setString(2, customer.getPhone());
                ps.setString(3, customer.getEmail());
                ps.executeUpdate();
                try (ResultSet rs = ps.getGeneratedKeys()) {
                    if (!rs.next()) throw new SQLException("Customer insert failed.");
                    customerId = rs.getInt(1);
                }
            }
            int reservationId;
            try (PreparedStatement ps = conn.prepareStatement(insertReservation, Statement.RETURN_GENERATED_KEYS)) {
                ps.setInt(1, customerId);
                ps.setInt(2, reservation.getTableId());
                ps.setDate(3, Date.valueOf(reservation.getReservationDate()));
                ps.setTime(4, Time.valueOf(reservation.getReservationTime()));
                ps.setInt(5, reservation.getGuests());
                ps.setString(6, reservation.getStatus());
                ps.executeUpdate();
                try (ResultSet rs = ps.getGeneratedKeys()) {
                    if (!rs.next()) throw new SQLException("Reservation insert failed.");
                    reservationId = rs.getInt(1);
                }
            }
            conn.commit();
            return reservationId;
        } catch (SQLException e) {
            conn.rollback();
            throw e;
        } finally {
            conn.setAutoCommit(autoCommit);
        }
    }
}"""
    story.append(Paragraph(f"<pre>{snippet_book}</pre>", code_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: 5.4 SEARCH, 5.5 CANCEL, 5.6 VALIDATION
    # =========================================================================
    story.append(Paragraph("5.4 Searching Reservations (ReservationDAO.java)", h2_style))
    story.append(Paragraph("Search values are safely bound with PreparedStatement to prevent SQL injection.", body_style))

    snippet_search = """public List<ReservationDetail> searchReservationDetails(String searchBy, String text) throws SQLException {
    String where = switch (searchBy) {
        case SEARCH_ID -> " WHERE r.reservation_id = ?";
        case SEARCH_NAME -> " WHERE c.name LIKE ?";
        case SEARCH_PHONE -> " WHERE c.phone LIKE ?";
        default -> throw new IllegalArgumentException("Unknown field: " + searchBy);
    };
    String sql = DETAIL_SELECT + where + " ORDER BY r.reservation_date DESC, r.reservation_time DESC";
    try (Connection conn = DBConnection.getConnection();
         PreparedStatement ps = conn.prepareStatement(sql)) {
        if (SEARCH_ID.equals(searchBy)) ps.setInt(1, Integer.parseInt(text.trim()));
        else ps.setString(1, "%" + text.trim() + "%");
        try (ResultSet rs = ps.executeQuery()) {
            List<ReservationDetail> details = new ArrayList<>();
            while (rs.next()) details.add(mapDetail(rs));
            return details;
        }
    }
}"""
    story.append(Paragraph(f"<pre>{snippet_search}</pre>", code_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("5.5 Cancelling a Booking (ReservationDAO.java)", h2_style))
    story.append(Paragraph("Cancelling only changes status to CANCELLED, freeing the table slot while keeping history.", body_style))

    snippet_cancel = """public boolean updateReservation(Reservation reservation) throws SQLException {
    String sql = "UPDATE reservations SET table_id=?, reservation_date=?, reservation_time=?, guests=?, status=? WHERE reservation_id=?";
    try (Connection conn = DBConnection.getConnection();
         PreparedStatement ps = conn.prepareStatement(sql)) {
        ps.setInt(1, reservation.getTableId());
        ps.setDate(2, Date.valueOf(reservation.getReservationDate()));
        ps.setTime(3, Time.valueOf(reservation.getReservationTime()));
        ps.setInt(4, reservation.getGuests());
        ps.setString(5, reservation.getStatus());
        ps.setInt(6, reservation.getReservationId());
        return ps.executeUpdate() > 0;
    }
}"""
    story.append(Paragraph(f"<pre>{snippet_cancel}</pre>", code_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("5.6 Checking User Input (ValidationUtil.java)", h2_style))
    story.append(Paragraph("Validation rules ensure valid phone numbers, valid email formats, and prevent bookings in the past.", body_style))

    snippet_val = """public static boolean isValidPhone(String phone) {
    if (isBlank(phone)) return false;
    String cleaned = phone.trim().replace(" ", "").replace("-", "");
    return PHONE_PATTERN.matcher(cleaned).matches();
}

public static boolean isPastSlot(LocalDate date, LocalTime time) {
    LocalDate today = LocalDate.now();
    return date.isBefore(today) || (date.isEqual(today) && time.isBefore(LocalTime.now()));
}

public static boolean isValidGuestCount(int guests, int capacity) {
    return guests > 0 && guests <= capacity;
}"""
    story.append(Paragraph(f"<pre>{snippet_val}</pre>", code_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: 5.7 PASSWORDS, 5.8 EVENT HANDLING, 5.9 SCREEN OPENING
    # =========================================================================
    story.append(Paragraph("5.7 Keeping Passwords Safe (PasswordUtil.java)", h2_style))
    story.append(Paragraph("The password is mixed with a random 32-character salt and converted into a SHA-256 hash. Plaintext passwords are never stored in the database.", body_style))

    snippet_pass = """public static String hashPassword(String password, String salt) {
    try {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] hash = digest.digest((salt + password).getBytes(StandardCharsets.UTF_8));
        return bytesToHex(hash);
    } catch (NoSuchAlgorithmException e) {
        throw new RuntimeException("SHA-256 is unavailable", e);
    }
}

public static boolean verifyPassword(String password, String salt, String expectedHash) {
    String calculated = hashPassword(password, salt);
    return MessageDigest.isEqual(calculated.getBytes(StandardCharsets.UTF_8),
                                 expectedHash.getBytes(StandardCharsets.UTF_8));
}"""
    story.append(Paragraph(f"<pre>{snippet_pass}</pre>", code_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("5.8 Event Handling in the Booking Form (ReservationDialog.java)", h2_style))
    story.append(Paragraph("Action listeners validate user input, verify slot availability, and trigger database persistence on click.", body_style))

    snippet_evt = """findButton.addActionListener(e -> findAvailableTables(true));
confirmButton.addActionListener(e -> confirmBooking());

private void confirmBooking() {
    String name = nameField.getText().trim();
    String phone = phoneField.getText().trim();
    if (ValidationUtil.isBlank(name)) { GUITheme.error(this, "Please enter customer name."); return; }
    if (!ValidationUtil.isValidPhone(phone)) { GUITheme.error(this, "Please enter valid 10-digit phone."); return; }
    RestaurantTable table = (RestaurantTable) tableCombo.getSelectedItem();
    if (table == null) { GUITheme.error(this, "Please select an available table."); return; }
    // Proceed to atomic transaction booking...
}"""
    story.append(Paragraph(f"<pre>{snippet_evt}</pre>", code_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("5.9 Opening the Right Screen After Login (MainFrame.java)", h2_style))
    story.append(Paragraph("After a correct login, an admin sees the Admin Dashboard and a customer sees the Customer Portal.", body_style))

    snippet_login = """User user = userDAO.login(usernameField.getText().trim(), new String(passwordField.getPassword()));
if (user == null) {
    loginErrorLabel.setText("Invalid username or password.");
    return;
}
UserSession.login(user);
if (user.isAdmin()) showView("ADMIN_DASHBOARD");
else showView("CUSTOMER_DASHBOARD");"""
    story.append(Paragraph(f"<pre>{snippet_login}</pre>", code_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGES 12 - 20: 6. SCREENSHOTS (ONE BY ONE MATCHING REFERENCE REPORT)
    # =========================================================================
    story.append(Paragraph("6. Screenshots", h1_style))
    story.append(Paragraph("The screenshots below show the main features of the application, in the order a user would use them.", body_style))
    story.append(Paragraph("6.1 Login and Registration", h2_style))

    if os.path.exists("01_Login_Screen.png"):
        story.append(Image("01_Login_Screen.png", width=440, height=295))
        story.append(Paragraph("Figure 6.1 – Login screen for both admin and customers", caption_style))
    story.append(PageBreak())

    # Page 13: Admin Dashboard & Booking
    story.append(Paragraph("6.2 Admin Dashboard and Live Numbers", h2_style))
    if os.path.exists("02_Admin_Dashboard.png"):
        story.append(Image("02_Admin_Dashboard.png", width=440, height=295))
        story.append(Paragraph("Figure 6.2 – Admin dashboard with live numbers, free tables and quick action buttons", caption_style))
    story.append(PageBreak())

    # Page 14: Booking a Table
    story.append(Paragraph("6.3 Booking a Table (Entering Customer Details)", h2_style))
    if os.path.exists("03_Reservation_Dialog.png"):
        story.append(Image("03_Reservation_Dialog.png", width=360, height=350))
        story.append(Paragraph("Figure 6.3 – Booking form with customer name, phone, dates, time and party size", caption_style))
    story.append(PageBreak())

    # Page 15: Table Availability
    story.append(Paragraph("6.4 Real-Time Table Slot Availability", h2_style))
    if os.path.exists("04_Tables_Dialog.png"):
        story.append(Image("04_Tables_Dialog.png", width=420, height=270))
        story.append(Paragraph("Figure 6.4 – Table availability screen showing free and booked tables for a chosen slot", caption_style))
    story.append(PageBreak())

    # Page 16: Search Reservation
    story.append(Paragraph("6.5 Searching for a Reservation", h2_style))
    if os.path.exists("05_Search_Dialog.png"):
        story.append(Image("05_Search_Dialog.png", width=440, height=250))
        story.append(Paragraph("Figure 6.5 – Search screen finding reservations by customer name or phone number", caption_style))
    story.append(PageBreak())

    # Page 17: Modify Reservation
    story.append(Paragraph("6.6 Changing a Booking", h2_style))
    if os.path.exists("06_Modify_Dialog.png"):
        story.append(Image("06_Modify_Dialog.png", width=440, height=300))
        story.append(Paragraph("Figure 6.6 – Change booking screen with real-time slot conflict checking", caption_style))
    story.append(PageBreak())

    # Page 18: Cancel Reservation
    story.append(Paragraph("6.7 Cancelling a Booking", h2_style))
    if os.path.exists("07_Cancel_Dialog.png"):
        story.append(Image("07_Cancel_Dialog.png", width=440, height=260))
        story.append(Paragraph("Figure 6.7 – Cancellation screen with confirmation to free up the table", caption_style))
    story.append(PageBreak())

    # Page 19: Customer Dashboard
    story.append(Paragraph("6.8 Customer Screens", h2_style))
    if os.path.exists("08_Customer_Dashboard.png"):
        story.append(Image("08_Customer_Dashboard.png", width=440, height=295))
        story.append(Paragraph("Figure 6.8 – Customer portal showing personal bookings and quick booking action", caption_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 20: 7. TEST CASES AND RESULTS - 7.1 UNIT TESTS
    # =========================================================================
    story.append(Paragraph("7. Test Cases and Results", h1_style))
    story.append(Paragraph("We tested the project in two ways. First, we ran unit tests on the rules for input checking and passwords. All 24 unit tests passed. Second, we tested complete tasks through the screens, with the MySQL database running.", body_style))

    story.append(Paragraph("7.1 Unit Tests", h2_style))
    story.append(Paragraph("These tests give fixed input to the ValidationUtil and PasswordUtil classes and compare the output with the expected result.", body_style))

    ut_data = [
        [Paragraph("Test ID", cell_bold), Paragraph("Input", cell_bold), Paragraph("Expected result", cell_bold), Paragraph("Result", cell_bold)],
        [Paragraph("UT-01", cell_style), Paragraph("Customer name left empty", cell_style), Paragraph("Error: isBlank() returns true", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-02", cell_style), Paragraph("Customer name 'Gokul Hari Rajan'", cell_style), Paragraph("Accepted", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-03", cell_style), Paragraph("Customer name with special characters", cell_style), Paragraph("Accepted", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-04", cell_style), Paragraph("Phone number '98765' (5 digits)", cell_style), Paragraph("Error: must be 10 to 15 digits", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-05", cell_style), Paragraph("Phone number '9876543210'", cell_style), Paragraph("Accepted", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-06", cell_style), Paragraph("Phone number '98765abc10'", cell_style), Paragraph("Error: only digits allowed", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-07", cell_style), Paragraph("Phone with country code '+919876543210'", cell_style), Paragraph("Accepted", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-08", cell_style), Paragraph("Reservation date in the past (yesterday)", cell_style), Paragraph("Error: cannot book in the past", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-09", cell_style), Paragraph("Reservation date tomorrow", cell_style), Paragraph("Accepted", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-10", cell_style), Paragraph("Reservation time '19:00'", cell_style), Paragraph("Accepted and parsed correctly", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-11", cell_style), Paragraph("Reservation time '25:99' (invalid)", cell_style), Paragraph("Error: DateTimeParseException", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-12", cell_style), Paragraph("Guest count 0 for a 4-seat table", cell_style), Paragraph("Error: needs at least 1 guest", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-13", cell_style), Paragraph("Guest count 4 for a 4-seat table", cell_style), Paragraph("Accepted", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-14", cell_style), Paragraph("Guest count 6 for a 4-seat table", cell_style), Paragraph("Error: exceeds table capacity", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-15", cell_style), Paragraph("Email 'gokul@gmail.com'", cell_style), Paragraph("Accepted", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-16", cell_style), Paragraph("Email 'gokul@' (invalid syntax)", cell_style), Paragraph("Error: invalid email address", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-17", cell_style), Paragraph("Email left empty", cell_style), Paragraph("Accepted (email is optional)", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-18", cell_style), Paragraph("Length of a new salt", cell_style), Paragraph("32 hexadecimal characters", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-19", cell_style), Paragraph("Length of a password hash", cell_style), Paragraph("64 hexadecimal characters (SHA-256)", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-20", cell_style), Paragraph("Correct password checked against hash", cell_style), Paragraph("Match", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-21", cell_style), Paragraph("Wrong password checked against hash", cell_style), Paragraph("No match", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-22", cell_style), Paragraph("Same password hashed with two salts", cell_style), Paragraph("Two completely different hashes", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-23", cell_style), Paragraph("User role 'ADMIN' checked via isAdmin()", cell_style), Paragraph("Returns true", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("UT-24", cell_style), Paragraph("User role 'CUSTOMER' checked via isCustomer()", cell_style), Paragraph("Returns true", cell_style), Paragraph("Pass", cell_style)],
    ]
    t_ut = Table(ut_data, colWidths=[45, 175, 195, 45])
    t_ut.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_ut)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 21: 7.2 FUNCTIONAL TEST CASES
    # =========================================================================
    story.append(Paragraph("7.2 Functional Test Cases", h2_style))
    story.append(Paragraph("Each test below is done through the application screens with MySQL running.", body_style))

    ft_data = [
        [Paragraph("Test ID", cell_bold), Paragraph("Module", cell_bold), Paragraph("Steps", cell_bold), Paragraph("Expected result", cell_bold), Paragraph("Result", cell_bold)],
        [Paragraph("FT-01", cell_style), Paragraph("Login", cell_style), Paragraph("Sign in as admin / admin123", cell_style), Paragraph("The admin dashboard opens with live numbers", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("FT-02", cell_style), Paragraph("Login", cell_style), Paragraph("Enter a wrong password", cell_style), Paragraph("Error message 'Invalid username or password' is shown", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("FT-03", cell_style), Paragraph("Registration", cell_style), Paragraph("Fill all fields correctly and click Create Account", cell_style), Paragraph("Account is created and Customer Portal opens", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("FT-04", cell_style), Paragraph("Registration", cell_style), Paragraph("Sign up with a username that already exists", cell_style), Paragraph("'Username is already taken' is shown. No duplicate row created", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("FT-05", cell_style), Paragraph("View Tables", cell_style), Paragraph("Choose date and time slot", cell_style), Paragraph("Only tables free on that slot are shown as AVAILABLE", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("FT-06", cell_style), Paragraph("Booking", cell_style), Paragraph("Enter customer name, 10-digit phone, date, time and table, click Confirm", cell_style), Paragraph("A reservation ID is assigned and table slot becomes booked", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("FT-07", cell_style), Paragraph("Booking", cell_style), Paragraph("Enter a 5-digit phone number and click Confirm", cell_style), Paragraph("Error dialog is shown and nothing is saved", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("FT-08", cell_style), Paragraph("Booking", cell_style), Paragraph("Try booking the same table for the same slot from another account", cell_style), Paragraph("Table does not appear in available list; double booking prevented", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("FT-09", cell_style), Paragraph("Search", cell_style), Paragraph("Search by reservation ID or customer name", cell_style), Paragraph("Matching reservations appear in table", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("FT-10", cell_style), Paragraph("Search", cell_style), Paragraph("Customer searches their own bookings", cell_style), Paragraph("Customers see only their own bookings; other records are hidden", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("FT-11", cell_style), Paragraph("Modify", cell_style), Paragraph("Change time slot of a future booking to an open slot", cell_style), Paragraph("Record is updated and new time appears in list", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("FT-12", cell_style), Paragraph("Modify", cell_style), Paragraph("Move a booking to a table already booked for that slot", cell_style), Paragraph("Warning shown: 'Table is not available for this slot'. Nothing changed", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("FT-13", cell_style), Paragraph("Cancel", cell_style), Paragraph("Customer cancels active booking and clicks Yes", cell_style), Paragraph("Status changes to CANCELLED and table slot is freed", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("FT-14", cell_style), Paragraph("Delete", cell_style), Paragraph("Admin selects reservation in cancel screen and clicks Delete Permanently", cell_style), Paragraph("Reservation row is deleted after user confirmation", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("FT-15", cell_style), Paragraph("Logout", cell_style), Paragraph("Click Logout on top navigation bar", cell_style), Paragraph("Session cleared and app returns to Login screen", cell_style), Paragraph("Pass", cell_style)],
        [Paragraph("FT-16", cell_style), Paragraph("Errors", cell_style), Paragraph("Stop MySQL server and start the application", cell_style), Paragraph("Warning shown on launch without app crashing", cell_style), Paragraph("Pass", cell_style)],
    ]
    t_ft = Table(ft_data, colWidths=[40, 65, 140, 175, 40])
    t_ft.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_ft)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 22: 8. RESULTS, 9. CONCLUSION, 10. REFERENCES & GITHUB
    # =========================================================================
    story.append(Paragraph("8. Results", h1_style))
    story.append(Paragraph("The Restaurant Table Reservation System was fully tested and verified against our local MySQL database. The system successfully accomplishes:", body_style))
    story.append(Paragraph("• Dual role authentication separating front-desk staff administration from customer self-service.", bullet_style))
    story.append(Paragraph("• Conflict-free table management where table availability is computed dynamically per slot.", bullet_style))
    story.append(Paragraph("• Atomic multi-table transactions inserting customer and reservation records safely.", bullet_style))
    story.append(Paragraph("• Comprehensive search, modification and cancellation workflows preserving booking history.", bullet_style))
    story.append(Paragraph("• Cryptographic salted SHA-256 password protection ensuring high security standards.", bullet_style))

    story.append(Paragraph("9. Conclusion", h1_style))
    story.append(Paragraph("The project demonstrates all core competencies required for <b>UIT3361 – Object-Oriented Programming Using Java</b>. By adopting a strict layered architecture, the user interface remains completely decoupled from database mechanics. The application illustrates practical mastery of Java Swing event handling, JDBC PreparedStatement execution, transaction demarcation (commit/rollback), defensive input checking, and object-oriented encapsulation.", body_style))

    story.append(Paragraph("10. Future Enhancements", h1_style))
    story.append(Paragraph("• SMS and email reservation confirmation alerts using JavaMail API.", bullet_style))
    story.append(Paragraph("• Interactive visual floor map allowing guests to pick tables by spatial location.", bullet_style))
    story.append(Paragraph("• Advance deposit online payment gateway integration.", bullet_style))
    story.append(Paragraph("• Mobile companion app sharing the central MySQL database.", bullet_style))

    story.append(Paragraph("11. References", h1_style))
    story.append(Paragraph("1. Oracle Corporation, <i>Java Platform, Standard Edition (Java SE 21) Documentation</i>, 2023.", bullet_style))
    story.append(Paragraph("2. Oracle Corporation, <i>Lesson: JDBC Database Access</i>, The Java Tutorials.", bullet_style))
    story.append(Paragraph("3. Oracle Corporation, <i>Creating a GUI with Swing</i>, The Java Tutorials.", bullet_style))
    story.append(Paragraph("4. MySQL AB / Oracle Corporation, <i>MySQL 8.0 Reference Manual</i>, 2024.", bullet_style))
    story.append(Paragraph("5. Herbert Schildt, <i>Java: The Complete Reference</i>, 12th Edition, McGraw-Hill, 2021.", bullet_style))

    story.append(Paragraph("12. GitHub Repository Link", h1_style))
    story.append(Paragraph("<u>https://github.com/GokulHariRajan/RestaurantReservationSystem</u>", body_style))

    doc.build(story, canvasmaker=PlainNumberedCanvas)
    print(f"Generated clean plain PDF report: {pdf_filename}")

if __name__ == '__main__':
    build_pdf()
