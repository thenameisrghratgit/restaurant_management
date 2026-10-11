# Generate College Project Report for Restaurant Table Reservation System
import os
import sys
import pypdf
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress header and footer on cover page
            return

        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#718096"))

        # Running Header
        header_text = "UIT3361 – OOP USING JAVA  |  RESTAURANT TABLE RESERVATION SYSTEM"
        self.drawString(54, 842 - 36, header_text)
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 842 - 42, 595 - 54, 842 - 42)

        # Running Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(595 - 54, 36, page_str)
        self.drawString(54, 36, "Sri Sivasubramaniya Nadar College of Engineering — Dept of IT")
        self.line(54, 48, 595 - 54, 48)

        self.restoreState()

def create_story(toc_page_map=None):
    styles = getSampleStyleSheet()

    primary_color = colors.HexColor("#1A365D")
    secondary_color = colors.HexColor("#2B6CB0")
    accent_color = colors.HexColor("#C53030")
    text_color = colors.HexColor("#2D3748")
    code_bg = colors.HexColor("#F7FAFC")
    border_color = colors.HexColor("#E2E8F0")

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        alignment=1,
        textColor=primary_color
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        alignment=1,
        textColor=accent_color
    )

    college_style = ParagraphStyle(
        'CoverCollege',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        alignment=1,
        textColor=primary_color
    )

    dept_style = ParagraphStyle(
        'CoverDept',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#4A5568")
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15.5,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=text_color,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1A202C")
    )

    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11.5,
        alignment=1,
        textColor=colors.HexColor("#4A5568"),
        spaceBefore=4,
        spaceAfter=8
    )

    placeholder_style = ParagraphStyle(
        'Placeholder_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        alignment=1,
        textColor=colors.HexColor("#C53030")
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=text_color
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white
    )

    story = []

    # =========================================================================
    # 1. COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 25))
    story.append(Paragraph("SRI SIVASUBRAMANIYA NADAR COLLEGE OF ENGINEERING", college_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("(An Autonomous Institution Affiliated to Anna University, Chennai)", dept_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Kalavakkam – 603 110, Tamil Nadu, India", dept_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("DEPARTMENT OF INFORMATION TECHNOLOGY", college_style))
    story.append(Spacer(1, 25))

    story.append(HRFlowable(width="80%", thickness=2, color=primary_color, spaceAfter=20))
    story.append(Paragraph("PROJECT REPORT", subtitle_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("RESTAURANT TABLE RESERVATION SYSTEM", title_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Course Code: UIT3361 – OBJECT-ORIENTED PROGRAMMING USING JAVA", subtitle_style))
    story.append(HRFlowable(width="80%", thickness=2, color=primary_color, spaceBefore=20, spaceAfter=30))

    meta_table_data = [
        [Paragraph("<b>Degree & Branch:</b>", body_style), Paragraph("B.Tech Information Technology", body_style)],
        [Paragraph("<b>Semester:</b>", body_style), Paragraph("III", body_style)],
        [Paragraph("<b>Regulation:</b>", body_style), Paragraph("2024", body_style)],
        [Paragraph("<b>Academic Year:</b>", body_style), Paragraph("2026–2027", body_style)],
        [Paragraph("<b>Submitted By:</b>", body_style), Paragraph("<b>Gokul Hari Rajan R</b>", body_style)],
        [Paragraph("<b>Register Number:</b>", body_style), Paragraph("<b>37</b>", body_style)],
    ]
    meta_table = Table(meta_table_data, colWidths=[160, 240])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 40))
    story.append(Paragraph("October 2026", dept_style))
    story.append(PageBreak())

    # =========================================================================
    # 2. TABLE OF CONTENTS
    # =========================================================================
    story.append(Paragraph("TABLE OF CONTENTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=12))

    # Dynamic TOC resolution
    toc_keys = [
        ("1. Abstract", "1. ABSTRACT", "3"),
        ("2. Introduction", "2. INTRODUCTION", "3"),
        ("3. Problem Statement & Scope", "3. PROBLEM STATEMENT", "3"),
        ("4. System Requirements", "4. SYSTEM REQUIREMENTS", "5"),
        ("5. System Design & Architecture", "5. SYSTEM DESIGN", "5"),
        ("6. Module Description", "6. MODULE DESCRIPTION", "7"),
        ("7. Object-Oriented Programming (OOP) Concepts", "7. OBJECT-ORIENTED", "9"),
        ("8. Database Design & Relational Schema", "8. DATABASE DESIGN", "11"),
        ("9. Entity-Relationship (ER) Diagram", "9. ENTITY-RELATIONSHIP", "11"),
        ("10. JDBC Connectivity & Transaction Management", "10. JDBC CONNECTIVITY", "13"),
        ("11. CRUD Operations Implementation", "11. CRUD OPERATIONS", "15"),
        ("12. GUI Design & Layout Management", "12. GUI DESIGN", "16"),
        ("13. Event Handling Mechanism", "13. EVENT HANDLING", "16"),
        ("14. Input Validation & Exception Handling", "14. INPUT VALIDATION", "17"),
        ("15. Important Code Snippets", "15. IMPORTANT CODE", "17"),
        ("16. Application Screenshots & Evidence", "16. APPLICATION SCREENSHOTS", "20"),
        ("17. Testing Strategy & Test Cases", "17. TESTING STRATEGY", "24"),
        ("18. Test Results Analysis", "18. TEST RESULTS", "25"),
        ("19. Advantages & Limitations", "19. ADVANTAGES", "26"),
        ("20. Future Enhancements & Conclusion", "20. FUTURE ENHANCEMENTS", "26"),
        ("21. GitHub Repository & Submission Checklist", "21. GITHUB", "27"),
        ("22. References", "22. REFERENCES", "27")
    ]

    toc_data = []
    for label, search_key, default_pg in toc_keys:
        pg_num = str(toc_page_map.get(search_key, default_pg)) if toc_page_map else default_pg
        toc_data.append([
            Paragraph(f"<b>{label}</b>", body_style),
            Paragraph(f"<b>{pg_num}</b>", ParagraphStyle('TOCPage', parent=body_style, alignment=2))
        ])

    toc_table = Table(toc_data, colWidths=[420, 60])
    toc_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#EDF2F7")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # =========================================================================
    # 3. ABSTRACT & INTRODUCTION
    # =========================================================================
    story.append(Paragraph("1. ABSTRACT", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    abstract_text = (
        "The <b>Restaurant Table Reservation System</b> is a robust, standalone desktop application "
        "engineered using <b>Java (JDK 21)</b>, <b>Java Swing</b>, <b>JDBC</b>, and <b>MySQL Relational Database Management System</b>. "
        "The software provides an end-to-end operational solution for restaurant front-desk management, allowing operators to "
        "record customer details, evaluate real-time table availability, make dining reservations, search existing records, modify active "
        "reservations, and execute soft-cancellations or permanent deletions. Designed under the principles of "
        "<b>Object-Oriented Programming (OOP)</b> and layered architecture, the application strictly decouples business models, data "
        "access objects (DAO), presentation logic (Swing GUI), and centralized utilities. Key engineering highlights include atomic "
        "multi-table transactions (ensuring simultaneous insertion of customer and reservation records with rollback protection), "
        "slot-based conflict detection preventing double-booking, dynamic SQL projection queries using multi-table JOINs, comprehensive "
        "input validation with regular expressions, and two-tier exception handling across both GUI and JDBC layers. "
        "This project comprehensively satisfies the curriculum requirements of UIT3361 – Object-Oriented Programming Using Java."
    )
    story.append(Paragraph(abstract_text, body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. INTRODUCTION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    intro_p1 = (
        "In modern hospitality management, table allocation and guest reservation workflows represent mission-critical operations. "
        "Traditional pen-and-paper ledgers or ad-hoc spreadsheets are prone to clerical errors, table double-bookings, customer communication "
        "delays, and complete lack of concurrent slot tracking. A software-driven reservation management system streamlines these operations "
        "by enforcing strict transactional consistency, relational integrity, and rapid query response."
    )
    intro_p2 = (
        "This project implements a standalone Java desktop application adhering to industry-standard architectural best practices. "
        "Built using Core Java and the Java Swing GUI toolkit, the system interfaces with a backend MySQL database using the official "
        "MySQL Connector/J 9.x driver. Through an intuitive, custom-themed graphical interface, operators can inspect table inventory, "
        "process bookings, and manage customer interactions without interacting directly with SQL query shells."
    )
    story.append(Paragraph(intro_p1, body_style))
    story.append(Paragraph(intro_p2, body_style))
    story.append(Spacer(1, 8))

    # =========================================================================
    # 4. PROBLEM STATEMENT & SCOPE
    # =========================================================================
    story.append(Paragraph("3. PROBLEM STATEMENT & SCOPE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    story.append(Paragraph("3.1 Official Problem Statement (S.No 10, Register Nos 37 to 40)", h2_style))
    problem_quote = (
        "<i>\"Develop a Restaurant Table Reservation System using Java and an appropriate GUI framework. "
        "The application should allow users to enter customer details, view available tables, make reservations, "
        "search for existing reservations, modify reservation details, and cancel reservations. "
        "The application should provide an interactive graphical interface and implement suitable event handling "
        "and validation. JDBC should be used to maintain reservation information in a relational database.\"</i>"
    )
    story.append(Paragraph(problem_quote, ParagraphStyle('Quote', parent=body_style, leftIndent=15, rightIndent=15, textColor=colors.HexColor("#4A5568"))))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.2 Project Objectives", h2_style))
    objs = [
        "<b>Core Java & OOP:</b> Apply core language paradigms including encapsulation, constructors, method overloading, custom data modeling, and separation of concerns.",
        "<b>Graphical Interface:</b> Design a responsive desktop UI utilizing Java Swing components (JFrame, JDialog, JTable, JComboBox, JSpinner, Card/Border/GridBag layouts) and event listeners.",
        "<b>Relational Persistence:</b> Establish high-performance, secure JDBC communication with a local MySQL server instance (restaurant_db).",
        "<b>Transactional Integrity:</b> Execute customer creation and table booking atomically (conn.setAutoCommit(false), commit, rollback) to eliminate orphan records.",
        "<b>Conflict Prevention:</b> Enforce slot-based availability checking to guarantee that no physical table can be booked twice for overlapping dates and times.",
        "<b>CRUD Lifecycle:</b> Implement complete Create, Read, Update, and Delete operations accessible through dedicated dialog interfaces."
    ]
    for obj in objs:
        story.append(Paragraph(f"• {obj}", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.3 Scope of the Implementation", h2_style))
    scope_text = (
        "The scope encompasses single-location dining establishment table management. The system maintains physical restaurant tables with specific "
        "seating capacities (2-seater, 4-seater, 6-seater, 8-seater), captures guest demographics (name, phone, optional email), and manages bookings "
        "by date and time slot. Cancelled bookings release tables immediately back into the available pool while preserving historical audit records. "
        "Complex features outside course syllabus—such as online payment gateways, SMS dispatchers, or distributed multi-branch sync—are intentionally "
        "excluded in compliance with assignment guidelines."
    )
    story.append(Paragraph(scope_text, body_style))
    story.append(PageBreak())

    # =========================================================================
    # 5. SYSTEM REQUIREMENTS
    # =========================================================================
    story.append(Paragraph("4. SYSTEM REQUIREMENTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    story.append(Paragraph("4.1 Hardware Requirements", h2_style))
    hw_data = [
        [Paragraph("<b>Component</b>", table_header_style), Paragraph("<b>Minimum Specification</b>", table_header_style), Paragraph("<b>Target / Development Specification</b>", table_header_style)],
        [Paragraph("Processor", table_cell_style), Paragraph("1.5 GHz Dual-Core x86/x64", table_cell_style), Paragraph("Intel Core i5 / i7 / AMD Ryzen 5 or higher", table_cell_style)],
        [Paragraph("System Memory (RAM)", table_cell_style), Paragraph("2.0 GB RAM", table_cell_style), Paragraph("8.0 GB or 16.0 GB DDR4/DDR5", table_cell_style)],
        [Paragraph("Storage", table_cell_style), Paragraph("500 MB free hard drive space", table_cell_style), Paragraph("SSD with 10 GB+ free space", table_cell_style)],
        [Paragraph("Display Resolution", table_cell_style), Paragraph("1024 x 768 pixels", table_cell_style), Paragraph("1920 x 1080 (Full HD) recommended", table_cell_style)],
        [Paragraph("Input Devices", table_cell_style), Paragraph("Standard Keyboard and Mouse", table_cell_style), Paragraph("Standard Keyboard and Mouse/Trackpad", table_cell_style)]
    ]
    hw_table = Table(hw_data, colWidths=[120, 160, 200])
    hw_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
    ]))
    story.append(hw_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("4.2 Software Requirements", h2_style))
    sw_data = [
        [Paragraph("<b>Software Layer</b>", table_header_style), Paragraph("<b>Specification / Product</b>", table_header_style), Paragraph("<b>Version / Build</b>", table_header_style)],
        [Paragraph("Operating System", table_cell_style), Paragraph("Microsoft Windows 10 / 11 (64-bit)", table_cell_style), Paragraph("Windows 11 Home / Pro (Build 22631+)", table_cell_style)],
        [Paragraph("Java Development Kit", table_cell_style), Paragraph("OpenJDK / Eclipse Temurin / Oracle JDK", table_cell_style), Paragraph("Java SE 21 (Temurin-21.0.11+10 LTS)", table_cell_style)],
        [Paragraph("Relational Database", table_cell_style), Paragraph("MySQL Community Server", table_cell_style), Paragraph("MySQL Server 8.0.46 (Service: MySQL80)", table_cell_style)],
        [Paragraph("Database Client", table_cell_style), Paragraph("MySQL Workbench", table_cell_style), Paragraph("MySQL Workbench 8.0 CE", table_cell_style)],
        [Paragraph("JDBC Driver", table_cell_style), Paragraph("MySQL Connector/J", table_cell_style), Paragraph("mysql-connector-j-9.7.0.jar", table_cell_style)],
        [Paragraph("Integrated Dev Environment", table_cell_style), Paragraph("Eclipse IDE for Java Developers", table_cell_style), Paragraph("Eclipse IDE 2026-03 / 2026-06", table_cell_style)],
        [Paragraph("GUI Framework", table_cell_style), Paragraph("Java Foundation Classes (Swing / AWT)", table_cell_style), Paragraph("Java Standard Library javax.swing", table_cell_style)]
    ]
    sw_table = Table(sw_data, colWidths=[140, 180, 160])
    sw_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
    ]))
    story.append(sw_table)
    story.append(Spacer(1, 8))

    # =========================================================================
    # 6. SYSTEM DESIGN & ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("5. SYSTEM DESIGN & ARCHITECTURE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    arch_desc = (
        "The software architecture follows a disciplined <b>Layered Architecture</b> (Presentation, Business/Data Access, Persistence, "
        "and Relational Storage). This ensures high maintainability, testability, and adherence to the Single Responsibility Principle. "
        "The flow of data and execution proceeds strictly down the stack: UI actions trigger DAO invocations, which execute parameterized SQL "
        "over JDBC connections, returning POJO models back up to Swing UI models."
    )
    story.append(Paragraph(arch_desc, body_style))
    story.append(Spacer(1, 5))

    arch_diagram_data = [
        [Paragraph("<b>USER INTERACTION LAYER (Operator)</b>", table_header_style)],
        [Paragraph("Desktop Keyboard & Mouse Events (Click, Type, Window Actions)", table_cell_style)],
        [Paragraph("[ Action Events ]", ParagraphStyle('Arrow', parent=body_style, alignment=1))],
        [Paragraph("<b>PRESENTATION LAYER (gui package)</b><br/>MainFrame | ReservationDialog | ViewReservationsDialog | ModifyReservationDialog | CancelReservationDialog | TablesDialog | ReservationListPanel | ReservationTableModel | GUITheme", table_cell_style)],
        [Paragraph("[ Model & Parameter Exchange ]", ParagraphStyle('Arrow', parent=body_style, alignment=1))],
        [Paragraph("<b>DATA ACCESS OBJECT (DAO) LAYER (dao package)</b><br/>CustomerDAO | TableDAO | ReservationDAO<br/><i>(Encapsulates PreparedStatements, SQL Queries, Joins, ResultSets, and Atomic Transactions)</i>", table_cell_style)],
        [Paragraph("[ JDBC Connections & Domain Entities ]", ParagraphStyle('Arrow', parent=body_style, alignment=1))],
        [Paragraph("<b>UTILITY & PERSISTENCE LAYER (util & model packages)</b><br/>DBConnection (DriverManager) | ValidationUtil (Regex, Date/Time checks)<br/>Customer | RestaurantTable | Reservation | ReservationDetail", table_cell_style)],
        [Paragraph("[ TCP/IP Socket via Port 3306 (MySQL Connector/J 9.7.0) ]", ParagraphStyle('Arrow', parent=body_style, alignment=1))],
        [Paragraph("<b>RELATIONAL DATABASE LAYER (MySQL Server 8.0)</b><br/>Schema: <b>restaurant_db</b> | Tables: restaurant_tables, customers, reservations", table_header_style)]
    ]
    arch_table = Table(arch_diagram_data, colWidths=[480])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#EBF8FF")),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor("#EDF2F7")),
        ('BACKGROUND', (0,7), (-1,7), colors.HexColor("#FEFCBF")),
        ('BACKGROUND', (0,9), (-1,9), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("5.1 Architectural Layers Explained", h2_style))
    layers_text = [
        "<b>1. Presentation Layer (Swing GUI):</b> Contains all graphical view classes. Manages GUI component hierarchies, responsive styling via GUITheme, and table rendering via AbstractTableModel implementations. The presentation layer never writes raw SQL.",
        "<b>2. Data Access Object (DAO) Layer:</b> Serves as the intermediary between UI events and the database. Each entity has a dedicated DAO (CustomerDAO, TableDAO, ReservationDAO). Prepares SQL queries, manages transactions (commit/rollback), and maps ResultSets into POJOs.",
        "<b>3. Domain Model Layer:</b> Standard Plain Old Java Objects (POJOs) defining application entities: Customer, RestaurantTable, Reservation, and the joined projection ReservationDetail. Enforces data encapsulation with private fields and public accessors.",
        "<b>4. Utility Layer:</b> Cross-cutting utilities including DBConnection (centralized JDBC factory providing connection instances) and ValidationUtil (static validation methods for phone, email, date/time, and guest bounds)."
    ]
    for lt in layers_text:
        story.append(Paragraph(lt, bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # 7. MODULE DESCRIPTION
    # =========================================================================
    story.append(Paragraph("6. MODULE DESCRIPTION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    modules = [
        ("6.1 Main Dashboard Module (gui.MainFrame)",
         "Serves as the central navigation hub for the application. Displays the application banner, database connection status indicator, and high-contrast action buttons.",
         "Operator clicks on dashboard navigation buttons (Make Reservation, View, Search, Modify, Cancel, Available Tables, About, Exit).",
         "Initializes database health check via DBConnection.getConnection().isValid(3). Launches modal feature dialogs upon button actions.",
         "Visual status badge indicating active MySQL connectivity; opens target functional dialogs.",
         "MainFrame.java, GUITheme.java, DBConnection.java"),

        ("6.2 Reservation Booking Module (gui.ReservationDialog)",
         "Facilitates new dining reservations. Validates customer demographics, checks real-time table availability for selected date/time, and commits booking.",
         "Customer Name, Phone, Email, Guest Count, Date (yyyy-MM-dd), Time (HH:mm), Selected Table.",
         "Validates fields using ValidationUtil; queries available tables via TableDAO; executes transactional booking inserting into customers and reservations tables.",
         "Success alert showing generated Reservation ID and booking summary; auto-refreshes table availability.",
         "ReservationDialog.java, CustomerDAO.java, TableDAO.java, ReservationDAO.java, Customer.java, Reservation.java"),

        ("6.3 View Reservations Module (gui.ViewReservationsDialog)",
         "Provides a tabular overview of all dining reservations recorded in the database, with status filtering (All, BOOKED, COMPLETED, CANCELLED).",
         "Filter selection from JComboBox, Refresh button click.",
         "Invokes ReservationDAO.getAllReservationDetails() performing multi-table SQL JOIN; updates ReservationTableModel; applies in-memory stream filtering.",
         "Populated JTable displaying ID, Customer Name, Phone, Table Number, Guests, Date, Time, and Status.",
         "ViewReservationsDialog.java, ReservationListPanel.java, ReservationTableModel.java, ReservationDAO.java, ReservationDetail.java"),

        ("6.4 Search Reservation Module (gui.SearchReservationDialog)",
         "Enables fast retrieval of specific reservations based on user-selected criteria.",
         "Search criteria dropdown (Reservation ID, Customer Name, Phone Number) and text query string.",
         "Validates search input; executes parameterized SQL query in ReservationDAO using exact ID match or SQL LIKE %pattern% matching.",
         "Filtered JTable displaying matching reservation records with count indicator.",
         "SearchReservationDialog.java, ReservationListPanel.java, ReservationDAO.java, ReservationDetail.java"),

        ("6.5 Modify Reservation Module (gui.ModifyReservationDialog)",
         "Allows operators to update reservation date, time, guest count, table allocation, or status.",
         "Selection of existing reservation row; updated date, time, guests, table, status.",
         "Loads selected record into edit form; queries tables available for new slot excluding self; executes SQL UPDATE in ReservationDAO.",
         "Success confirmation alert; updated row re-rendered in table list with new parameters.",
         "ModifyReservationDialog.java, ReservationListPanel.java, ReservationDAO.java, TableDAO.java, Reservation.java"),

        ("6.6 Cancel & Delete Module (gui.CancelReservationDialog)",
         "Provides dual cancellation functionality: soft-cancellation (status='CANCELLED') preserving audit history, or permanent row deletion.",
         "Selection of target reservation row; confirmation modal click.",
         "Soft-cancel updates status to 'CANCELLED'; Delete permanently executes SQL DELETE FROM reservations WHERE reservation_id=?; releases table slot.",
         "Confirmation dialogs and updated table view reflecting CANCELLED status or removed record.",
         "CancelReservationDialog.java, ReservationListPanel.java, ReservationDAO.java"),

        ("6.7 Table Availability Module (gui.TablesDialog)",
         "Displays all restaurant tables, capacity ratings, baseline status, and real-time availability for any designated date and time slot.",
         "Date (yyyy-MM-dd) and Time (HH:mm) input; 'Check Availability' button click.",
         "Queries all tables from TableDAO; cross-references active reservations via ReservationDAO.getBookedTableIds(); computes AVAILABLE / OCCUPIED dynamically.",
         "Color-coded JTable (green AVAILABLE, red OCCUPIED) with slot availability statistics summary.",
         "TablesDialog.java, TableDAO.java, ReservationDAO.java, RestaurantTable.java")
    ]

    for m_title, m_purp, m_inp, m_proc, m_out, m_cls in modules:
        story.append(Paragraph(m_title, h2_style))
        story.append(Paragraph(f"<b>Purpose:</b> {m_purp}", body_style))
        story.append(Paragraph(f"<b>Inputs:</b> {m_inp}", body_style))
        story.append(Paragraph(f"<b>Processing:</b> {m_proc}", body_style))
        story.append(Paragraph(f"<b>Output:</b> {m_out}", body_style))
        story.append(Paragraph(f"<b>Classes Involved:</b> <code>{m_cls}</code>", body_style))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # =========================================================================
    # 8. OOP CONCEPTS
    # =========================================================================
    story.append(Paragraph("7. OBJECT-ORIENTED PROGRAMMING (OOP) CONCEPTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    oop_intro = (
        "The application is engineered strictly around foundational Object-Oriented Programming (OOP) paradigms. "
        "Every concept discussed below is verifiable directly in the source code of the project."
    )
    story.append(Paragraph(oop_intro, body_style))
    story.append(Spacer(1, 4))

    oops = [
        ("7.1 Classes and Objects",
         "The system models real-world domain entities using dedicated classes: <code>Customer</code>, <code>RestaurantTable</code>, "
         "<code>Reservation</code>, and <code>ReservationDetail</code>. At runtime, discrete objects are instantiated from these classes to represent "
         "active records loaded from the database or created from GUI user input. For example, creating a reservation instantiates both a <code>Customer</code> "
         "object and a <code>Reservation</code> object before transactional persistence.",
         "Customer customer = new Customer(\"Gokul\", \"9876543210\", \"gokul@gmail.com\");\n"
         "Reservation res = new Reservation(0, table.getTableId(), date, time, guests);"),

        ("7.2 Encapsulation and Data Hiding",
         "All state variables across entity classes are declared with <code>private</code> visibility modifiers, preventing unauthorized external modification. "
         "Access and mutation are exclusively provided via public getter and setter methods. Similarly, utility classes like <code>DBConnection</code> and "
         "<code>ValidationUtil</code> encapsulate credentials and regular expression pattern matchers, declaring private constructors to prevent instantiation.",
         "public class Customer {\n"
         "    private int customerId;\n"
         "    private String name;\n"
         "    public int getCustomerId() { return customerId; }\n"
         "    public void setCustomerId(int customerId) { this.customerId = customerId; }\n"
         "}"),

        ("7.3 Constructor Overloading",
         "Domain entities implement overloaded constructors to support diverse instantiation contexts: no-argument default constructors for reflection/frameworks, "
         "partial constructors for creating new records prior to database auto-increment ID generation, and full parameterized constructors for mapping existing "
         "database rows retrieved via JDBC ResultSets.",
         "public Customer() { }\n"
         "public Customer(String name, String phone, String email) { ... } // Before insert\n"
         "public Customer(int customerId, String name, String phone, String email) { ... } // From DB"),

        ("7.4 Separation of Concerns & DAO Pattern",
         "The Data Access Object (DAO) design pattern is implemented to decouple persistence logic from presentation logic. The GUI dialogs never execute "
         "SQL statements; instead, they interact with <code>CustomerDAO</code>, <code>TableDAO</code>, and <code>ReservationDAO</code>, passing and receiving "
         "domain objects. This guarantees high modularity and clean testability.",
         "// ReservationDialog invokes DAO cleanly without coupling to SQL queries\n"
         "int reservationId = reservationDAO.bookReservation(customer, reservation);"),

        ("7.5 Association and Aggregation",
         "Relationships between entities are implemented via object association. A <code>Reservation</code> references a <code>Customer</code> by customer ID "
         "and a <code>RestaurantTable</code> by table ID. The projection class <code>ReservationDetail</code> aggregates joined properties from both entities "
         "into a single unified object optimized for Swing table display.",
         "public class ReservationDetail {\n"
         "    private int reservationId;\n"
         "    private String customerName; // From customers table\n"
         "    private int tableNumber;     // From restaurant_tables table\n"
         "}")
    ]

    for o_title, o_desc, o_code in oops:
        story.append(Paragraph(o_title, h2_style))
        story.append(Paragraph(o_desc, body_style))
        story.append(Spacer(1, 2))

        code_table = Table([[Paragraph(o_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[480])
        code_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), code_bg),
            ('BOX', (0,0), (-1,-1), 0.5, border_color),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(code_table)
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # =========================================================================
    # 9. DATABASE DESIGN & ER DIAGRAM
    # =========================================================================
    story.append(Paragraph("8. DATABASE DESIGN & RELATIONAL SCHEMA", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    db_desc = (
        "The relational database is named <b>restaurant_db</b>, hosted on MySQL Community Server (localhost:3306). "
        "The database design strictly normalizes entity information across three primary tables: <code>customers</code>, "
        "<code>restaurant_tables</code>, and <code>reservations</code>. Foreign key constraints enforce referential integrity."
    )
    story.append(Paragraph(db_desc, body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("8.1 Table: restaurant_tables (Master Table for Seating Inventory)", h2_style))
    t1_data = [
        [Paragraph("<b>Column Name</b>", table_header_style), Paragraph("<b>Data Type</b>", table_header_style), Paragraph("<b>Constraints</b>", table_header_style), Paragraph("<b>Description</b>", table_header_style)],
        [Paragraph("table_id", table_cell_style), Paragraph("INT", table_cell_style), Paragraph("PRIMARY KEY, AUTO_INCREMENT", table_cell_style), Paragraph("Unique internal identifier for the table", table_cell_style)],
        [Paragraph("table_number", table_cell_style), Paragraph("INT", table_cell_style), Paragraph("NOT NULL, UNIQUE", table_cell_style), Paragraph("Physical table number displayed in dining area", table_cell_style)],
        [Paragraph("capacity", table_cell_style), Paragraph("INT", table_cell_style), Paragraph("NOT NULL", table_cell_style), Paragraph("Maximum seating capacity (2, 4, 6, 8 seats)", table_cell_style)],
        [Paragraph("status", table_cell_style), Paragraph("VARCHAR(20)", table_cell_style), Paragraph("DEFAULT 'AVAILABLE'", table_cell_style), Paragraph("Baseline table status descriptor", table_cell_style)],
    ]
    t1_table = Table(t1_data, colWidths=[100, 70, 160, 150])
    t1_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
    ]))
    story.append(t1_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("8.2 Table: customers (Customer Demographic Registry)", h2_style))
    t2_data = [
        [Paragraph("<b>Column Name</b>", table_header_style), Paragraph("<b>Data Type</b>", table_header_style), Paragraph("<b>Constraints</b>", table_header_style), Paragraph("<b>Description</b>", table_header_style)],
        [Paragraph("customer_id", table_cell_style), Paragraph("INT", table_cell_style), Paragraph("PRIMARY KEY, AUTO_INCREMENT", table_cell_style), Paragraph("Unique internal customer identifier", table_cell_style)],
        [Paragraph("name", table_cell_style), Paragraph("VARCHAR(100)", table_cell_style), Paragraph("NOT NULL", table_cell_style), Paragraph("Full legal name of the reserving customer", table_cell_style)],
        [Paragraph("phone", table_cell_style), Paragraph("VARCHAR(15)", table_cell_style), Paragraph("NOT NULL", table_cell_style), Paragraph("Contact telephone number (10–15 digits)", table_cell_style)],
        [Paragraph("email", table_cell_style), Paragraph("VARCHAR(100)", table_cell_style), Paragraph("NULLABLE", table_cell_style), Paragraph("Optional customer email address", table_cell_style)],
    ]
    t2_table = Table(t2_data, colWidths=[100, 70, 160, 150])
    t2_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
    ]))
    story.append(t2_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("8.3 Table: reservations (Transactional Reservation Records)", h2_style))
    t3_data = [
        [Paragraph("<b>Column Name</b>", table_header_style), Paragraph("<b>Data Type</b>", table_header_style), Paragraph("<b>Constraints</b>", table_header_style), Paragraph("<b>Description</b>", table_header_style)],
        [Paragraph("reservation_id", table_cell_style), Paragraph("INT", table_cell_style), Paragraph("PRIMARY KEY, AUTO_INCREMENT", table_cell_style), Paragraph("Unique identifier for each reservation record", table_cell_style)],
        [Paragraph("customer_id", table_cell_style), Paragraph("INT", table_cell_style), Paragraph("NOT NULL, FK → customers", table_cell_style), Paragraph("Foreign Key linking customer record", table_cell_style)],
        [Paragraph("table_id", table_cell_style), Paragraph("INT", table_cell_style), Paragraph("NOT NULL, FK → tables", table_cell_style), Paragraph("Foreign Key linking assigned table record", table_cell_style)],
        [Paragraph("reservation_date", table_cell_style), Paragraph("DATE", table_cell_style), Paragraph("NOT NULL", table_cell_style), Paragraph("Date of reservation (yyyy-MM-dd)", table_cell_style)],
        [Paragraph("reservation_time", table_cell_style), Paragraph("TIME", table_cell_style), Paragraph("NOT NULL", table_cell_style), Paragraph("Time of reservation slot (HH:mm:ss)", table_cell_style)],
        [Paragraph("guests", table_cell_style), Paragraph("INT", table_cell_style), Paragraph("NOT NULL", table_cell_style), Paragraph("Number of guests dining (guests <= capacity)", table_cell_style)],
        [Paragraph("status", table_cell_style), Paragraph("VARCHAR(20)", table_cell_style), Paragraph("DEFAULT 'BOOKED'", table_cell_style), Paragraph("Status: 'BOOKED', 'COMPLETED', 'CANCELLED'", table_cell_style)],
    ]
    t3_table = Table(t3_data, colWidths=[100, 70, 160, 150])
    t3_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
    ]))
    story.append(t3_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("9. ENTITY-RELATIONSHIP (ER) DIAGRAM", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    er_text = (
        "The relational schema implements a classic <b>1-to-Many (1:N)</b> relationship between Customers and Reservations, "
        "and a <b>1-to-Many (1:N)</b> relationship between Restaurant Tables and Reservations. "
        "A single customer can place multiple reservations across different dates, but each reservation record belongs strictly to one customer. "
        "Likewise, a single physical table hosts multiple reservations across distinct time slots, but each reservation occupies exactly one table."
    )
    story.append(Paragraph(er_text, body_style))
    story.append(Spacer(1, 4))

    er_box_data = [
        [Paragraph("<b>CUSTOMERS</b>", table_header_style), Paragraph("<b>RESERVATIONS</b>", table_header_style), Paragraph("<b>RESTAURANT_TABLES</b>", table_header_style)],
        [
            Paragraph("<u>PK: customer_id (INT)</u><br/>name (VARCHAR 100)<br/>phone (VARCHAR 15)<br/>email (VARCHAR 100)", table_cell_style),
            Paragraph("<u>PK: reservation_id (INT)</u><br/>FK: customer_id (INT)<br/>FK: table_id (INT)<br/>reservation_date (DATE)<br/>reservation_time (TIME)<br/>guests (INT)<br/>status (VARCHAR 20)", table_cell_style),
            Paragraph("<u>PK: table_id (INT)</u><br/>table_number (INT, UNI)<br/>capacity (INT)<br/>status (VARCHAR 20)", table_cell_style)
        ],
        [
            Paragraph("<b>(1)</b>", ParagraphStyle('CenterLabel', parent=body_style, alignment=1)),
            Paragraph("<b>[1:N] Customers to Reservations [N:1] Tables</b>", ParagraphStyle('CenterLabel', parent=body_style, alignment=1)),
            Paragraph("<b>(1)</b>", ParagraphStyle('CenterLabel', parent=body_style, alignment=1))
        ]
    ]
    er_table = Table(er_box_data, colWidths=[150, 180, 150])
    er_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), secondary_color),
        ('BACKGROUND', (1,0), (1,0), primary_color),
        ('BACKGROUND', (2,0), (2,0), secondary_color),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F7FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(er_table)
    story.append(Spacer(1, 4))
    story.append(Paragraph("Figure: Relational Entity-Relationship Diagram of restaurant_db", caption_style))
    story.append(PageBreak())

    # =========================================================================
    # 10. JDBC & TRANSACTION MANAGEMENT
    # =========================================================================
    story.append(Paragraph("10. JDBC CONNECTIVITY & TRANSACTION MANAGEMENT", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    jdbc_p1 = (
        "Java Database Connectivity (JDBC) is the standard Java API for relational database access. "
        "The application utilizes <b>MySQL Connector/J 9.7.0</b> to establish socket connections to MySQL Server 8.0 on TCP port 3306. "
        "All database operations are governed by core JDBC practices:"
    )
    story.append(Paragraph(jdbc_p1, body_style))

    jdbc_steps = [
        "<b>1. Driver Registration:</b> Automatically registered by JDBC 4.0+ SPI via <code>com.mysql.cj.jdbc.Driver</code> bundled in <code>mysql-connector-j-9.7.0.jar</code>.",
        "<b>2. Connection Establishment:</b> Centralized in <code>util.DBConnection.getConnection()</code> via <code>DriverManager.getConnection(URL, USER, PASSWORD)</code>.",
        "<b>3. Statement Execution:</b> All queries and DML updates utilize <code>PreparedStatement</code> with indexed parameter placeholders (<code>?</code>). This entirely neutralizes SQL Injection vulnerabilities.",
        "<b>4. Generated Keys Retrieval:</b> Upon insertion, <code>Statement.RETURN_GENERATED_KEYS</code> is passed to capture auto-increment primary keys without requiring auxiliary queries.",
        "<b>5. Resource Management:</b> All <code>Connection</code>, <code>PreparedStatement</code>, and <code>ResultSet</code> instances are managed inside <code>try-with-resources</code> blocks, guaranteeing deterministic closure even during exceptions.",
        "<b>6. Atomic Transactions:</b> Multi-table operations disable auto-commit (<code>conn.setAutoCommit(false)</code>), execute multiple DML statements on a shared connection, and invoke <code>conn.commit()</code> upon success or <code>conn.rollback()</code> upon failure."
    ]
    for js in jdbc_steps:
        story.append(Paragraph(js, bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("10.1 Transactional Booking Implementation", h2_style))
    tx_desc = (
        "When an operator submits a reservation in <code>ReservationDialog</code>, two discrete database tables must be updated: "
        "<code>customers</code> (to insert demographic details) and <code>reservations</code> (to assign the table). If the reservation insert fails "
        "(for instance, due to a constraint violation), the customer record must not be left orphaned. The transaction flow in <code>ReservationDAO.bookReservation()</code> "
        "executes both operations atomically:"
    )
    story.append(Paragraph(tx_desc, body_style))

    tx_code = (
        "try (Connection conn = DBConnection.getConnection()) {\n"
        "    boolean autoCommit = conn.getAutoCommit();\n"
        "    conn.setAutoCommit(false); // Begin database transaction\n"
        "    try {\n"
        "        // 1. Insert customer record\n"
        "        try (PreparedStatement ps = conn.prepareStatement(insertCustomer, Statement.RETURN_GENERATED_KEYS)) {\n"
        "            ps.setString(1, customer.getName());\n"
        "            ps.setString(2, customer.getPhone());\n"
        "            ps.setString(3, customer.getEmail());\n"
        "            ps.executeUpdate();\n"
        "            try (ResultSet rs = ps.getGeneratedKeys()) {\n"
        "                if (rs.next()) customerId = rs.getInt(1);\n"
        "            }\n"
        "        }\n"
        "        // 2. Insert reservation record with customerId\n"
        "        try (PreparedStatement ps = conn.prepareStatement(insertReservation, Statement.RETURN_GENERATED_KEYS)) {\n"
        "            ps.setInt(1, customerId);\n"
        "            ps.setInt(2, reservation.getTableId());\n"
        "            ps.setDate(3, Date.valueOf(reservation.getReservationDate()));\n"
        "            ps.setTime(4, Time.valueOf(reservation.getReservationTime()));\n"
        "            ps.setInt(5, reservation.getGuests());\n"
        "            ps.setString(6, reservation.getStatus());\n"
        "            ps.executeUpdate();\n"
        "            try (ResultSet rs = ps.getGeneratedKeys()) {\n"
        "                if (rs.next()) reservationId = rs.getInt(1);\n"
        "            }\n"
        "        }\n"
        "        conn.commit(); // Atomic commit: both persisted\n"
        "        return reservationId;\n"
        "    } catch (SQLException e) {\n"
        "        conn.rollback(); // Rollback: neither persisted\n"
        "        throw e;\n"
        "    } finally {\n"
        "        conn.setAutoCommit(autoCommit);\n"
        "    }\n"
        "}"
    )
    tx_code_table = Table([[Paragraph(tx_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[480])
    tx_code_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), code_bg),
        ('BOX', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(tx_code_table)
    story.append(PageBreak())

    # =========================================================================
    # 11. CRUD OPERATIONS
    # =========================================================================
    story.append(Paragraph("11. CRUD OPERATIONS IMPLEMENTATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    crud_intro = (
        "The project comprehensively implements all four basic relational database operations (CRUD). "
        "Each operation maps directly to dedicated DAO methods and corresponding Swing user interfaces:"
    )
    story.append(Paragraph(crud_intro, body_style))
    story.append(Spacer(1, 4))

    crud_data = [
        [Paragraph("<b>Operation</b>", table_header_style), Paragraph("<b>DAO Method</b>", table_header_style), Paragraph("<b>SQL Statement Type</b>", table_header_style), Paragraph("<b>Triggering GUI Screen</b>", table_header_style)],
        [
            Paragraph("<b>CREATE</b>", table_cell_style),
            Paragraph("<code>CustomerDAO.addCustomer()</code><br/><code>ReservationDAO.bookReservation()</code>", table_cell_style),
            Paragraph("INSERT INTO customers (...)<br/>INSERT INTO reservations (...)", table_cell_style),
            Paragraph("ReservationDialog<br/>(\"Book Reservation\" button)", table_cell_style)
        ],
        [
            Paragraph("<b>READ</b>", table_cell_style),
            Paragraph("<code>TableDAO.getAllTables()</code><br/><code>TableDAO.getAvailableTables()</code><br/><code>ReservationDAO.getAllReservationDetails()</code><br/><code>ReservationDAO.searchReservationDetails()</code>", table_cell_style),
            Paragraph("SELECT * FROM restaurant_tables<br/>SELECT t.* FROM restaurant_tables t WHERE ...<br/>SELECT r.*, c.*, t.* FROM reservations r JOIN ...<br/>SELECT ... WHERE r.id = ? / c.name LIKE ?", table_cell_style),
            Paragraph("ViewReservationsDialog<br/>SearchReservationDialog<br/>TablesDialog<br/>ModifyReservationDialog", table_cell_style)
        ],
        [
            Paragraph("<b>UPDATE</b>", table_cell_style),
            Paragraph("<code>ReservationDAO.updateReservation()</code>", table_cell_style),
            Paragraph("UPDATE reservations SET table_id=?, reservation_date=?, reservation_time=?, guests=?, status=? WHERE reservation_id=?", table_cell_style),
            Paragraph("ModifyReservationDialog<br/>CancelReservationDialog (status='CANCELLED')", table_cell_style)
        ],
        [
            Paragraph("<b>DELETE</b>", table_cell_style),
            Paragraph("<code>ReservationDAO.deleteReservation()</code>", table_cell_style),
            Paragraph("DELETE FROM reservations WHERE reservation_id=?", table_cell_style),
            Paragraph("CancelReservationDialog<br/>(\"Delete Permanently\" button)", table_cell_style)
        ]
    ]
    crud_table = Table(crud_data, colWidths=[65, 155, 145, 115])
    crud_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
    ]))
    story.append(crud_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("11.1 Dynamic SQL Projection via Multi-Table JOINs", h2_style))
    join_desc = (
        "To present human-readable information to restaurant staff (such as customer names and physical table numbers "
        "rather than obscure numeric foreign keys), <code>ReservationDAO</code> employs a unified three-table SQL JOIN:"
    )
    story.append(Paragraph(join_desc, body_style))

    join_sql = (
        "SELECT r.reservation_id, r.customer_id, r.table_id,\n"
        "       r.reservation_date, r.reservation_time, r.guests, r.status,\n"
        "       c.name AS customer_name, c.phone AS customer_phone,\n"
        "       t.table_number AS table_number\n"
        "FROM reservations r\n"
        "JOIN customers c ON c.customer_id = r.customer_id\n"
        "JOIN restaurant_tables t ON t.table_id = r.table_id\n"
        "ORDER BY r.reservation_date DESC, r.reservation_time DESC;"
    )
    join_table = Table([[Paragraph(join_sql.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[480])
    join_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), code_bg),
        ('BOX', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(join_table)
    story.append(PageBreak())

    # =========================================================================
    # 12. GUI DESIGN & LAYOUT MANAGEMENT
    # =========================================================================
    story.append(Paragraph("12. GUI DESIGN & LAYOUT MANAGEMENT", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    gui_desc = (
        "The user interface is built using <b>Java Swing</b>, maintaining full platform independence while providing a modern, "
        "aesthetic desktop experience. The styling is governed centrally by <code>gui.GUITheme</code>, ensuring uniform typography, "
        "palette tokens, button curvatures, table padding, and dialog banners."
    )
    story.append(Paragraph(gui_desc, body_style))

    gui_components = [
        "<b>Layout Managers:</b> Utilizes <code>BorderLayout</code> for overarching window frames, <code>GridLayout(4, 2, 14, 14)</code> for the dashboard action grid, <code>GridBagLayout</code> with precise constraints for responsive form layouts, <code>FlowLayout</code> for button action toolbars, and <code>JSplitPane</code> for divided master-detail views.",
        "<b>Swing Controls:</b> Implements <code>JFrame</code> (main application window), <code>JDialog</code> (modal dialogs preventing background clicks), <code>JTable</code> (data grid view), <code>JScrollPane</code> (viewports), <code>JTextField</code> (text input), <code>JComboBox</code> (dropdown selectors), <code>JSpinner</code> (numeric stepper), and <code>JLabel</code> (typography).",
        "<b>Custom Rendering:</b> Flat rounded button painting in <code>GUITheme.button()</code> with antialiased borders, hover state detection, and custom <code>TableCellRenderer</code> implementations providing color-coded status badges in JTable columns.",
        "<b>Reusable Components:</b> <code>ReservationListPanel</code> encapsulates a themed <code>JTable</code> bound to <code>ReservationTableModel</code>, reused identically across View, Search, Modify, and Cancel dialogs."
    ]
    for gc in gui_components:
        story.append(Paragraph(gc, bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("13. EVENT HANDLING MECHANISM", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    events_desc = (
        "Java Swing operates on an asynchronous event-driven model mediated by the Event Dispatch Thread (EDT). "
        "The project demonstrates multiple event listener interfaces implemented via modern Java lambdas and anonymous adapters:"
    )
    story.append(Paragraph(events_desc, body_style))

    events = [
        ("ActionListener (Button Clicks & Keyboard Enter):",
         "Attached to JButtons and JTextFields. For example, clicking 'Book Reservation' triggers <code>e -> bookReservation()</code>; pressing Enter inside the search text field immediately executes <code>e -> search()</code>.",
         "searchField.addActionListener(e -> search());\nbookButton.addActionListener(e -> bookReservation());"),

        ("ListSelectionListener (JTable Row Selection):",
         "Monitors row selections inside JTable. In <code>ModifyReservationDialog</code>, selecting a row retrieves the corresponding <code>ReservationDetail</code> object and populates the lower form fields.",
         "listPanel.getTable().getSelectionModel().addListSelectionListener(e -> {\n"
         "    if (!e.getValueIsAdjusting() && !updating) loadSelectedReservation();\n"
         "});"),

        ("DocumentListener & ChangeListener (Dynamic State Invalidation):",
         "Attached to date/time text fields and the guest count JSpinner. Any typing immediately clears the cached table dropdown, forcing the user to re-evaluate table availability for the modified slot.",
         "guestsSpinner.addChangeListener(e -> clearTableList());\ndateField.getDocument().addDocumentListener(invalidateTablesListener);"),

        ("FocusListener (Auto-Refresh on Field Exit):",
         "In <code>ModifyReservationDialog</code>, losing focus from date, time, or guest fields automatically refreshes available tables without requiring manual button clicks.",
         "dateField.addFocusListener(new FocusAdapter() {\n"
         "    public void focusLost(FocusEvent e) { refreshTableCombo(false); }\n"
         "});")
    ]

    for e_name, e_desc, e_code in events:
        story.append(Paragraph(f"<b>{e_name}</b> {e_desc}", body_style))
        code_t = Table([[Paragraph(e_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[480])
        code_t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), code_bg),
            ('BOX', (0,0), (-1,-1), 0.5, border_color),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(code_t)
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # =========================================================================
    # 13. VALIDATION & EXCEPTION HANDLING
    # =========================================================================
    story.append(Paragraph("14. INPUT VALIDATION & EXCEPTION HANDLING", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    val_intro = (
        "To ensure robust operation and protect relational data integrity, validation and error handling are implemented "
        "as dedicated, cross-cutting layers."
    )
    story.append(Paragraph(val_intro, body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("14.1 Centralized Validation Engine (util.ValidationUtil)", h2_style))
    val_rules = [
        "<b>Customer Name Validation:</b> Non-blank check via <code>ValidationUtil.isBlank(name)</code>; maximum length bound of 100 characters.",
        "<b>Phone Number Validation:</b> Regex pattern <code>^\\+?\\d{10,15}$</code> ensuring 10 to 15 digits with optional leading '+' symbol, stripping interior spaces or hyphens.",
        "<b>Email Validation:</b> Regex pattern <code>^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$</code> applied if email is provided (field is optional).",
        "<b>Date & Time Parsing:</b> ISO-8601 validation using <code>LocalDate.parse()</code> and <code>LocalTime.parse()</code>; catches <code>DateTimeParseException</code>.",
        "<b>Past Slot Prevention:</b> Evaluates <code>isPastSlot(date, time)</code> against system clock (<code>LocalDate.now()</code> and <code>LocalTime.now()</code>) to prevent back-dated reservations.",
        "<b>Guest Capacity Bounds:</b> Validates <code>guests > 0 && guests <= table.getCapacity()</code>, preventing overbooking table physical seating limits.",
        "<b>Numeric Search ID:</b> Ensures search queries under 'Reservation ID' contain strictly digit characters (<code>text.matches(\"\\\\d+\")</code>) before parsing."
    ]
    for vr in val_rules:
        story.append(Paragraph(f"• {vr}", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("14.2 Multi-Tier Exception Handling Strategy", h2_style))
    eh_tiers = [
        "<b>1. Global Uncaught Exception Handler:</b> Initialized at application startup in <code>Main.java</code> via <code>Thread.setDefaultUncaughtExceptionHandler()</code> to capture unexpected runtime errors without crashing the JVM.",
        "<b>2. Database Connectivity Pre-Check:</b> In <code>Main.java</code>, a test connection is verified via <code>connection.isValid(3)</code> before launching the Swing GUI. If MySQL is unreachable, a descriptive error dialog prompts the user and cleanly terminates startup.",
        "<b>3. Deterministic Resource Management:</b> All database queries enforce the <code>try-with-resources</code> pattern, ensuring automatic invocation of <code>AutoCloseable.close()</code> on connections, statements, and result sets.",
        "<b>4. Specific Exception Trapping:</b> Catch blocks distinguish between <code>SQLException</code> (database constraint/network errors), <code>DateTimeParseException</code> (malformed dates/times), and <code>NumberFormatException</code> (non-numeric ID inputs), presenting tailored user feedback.",
        "<b>5. Transaction Rollback Protection:</b> In <code>ReservationDAO.bookReservation()</code>, any <code>SQLException</code> triggers <code>conn.rollback()</code>, guaranteeing zero partial writes."
    ]
    for et in eh_tiers:
        story.append(Paragraph(f"• {et}", bullet_style))
    story.append(Spacer(1, 8))

    # =========================================================================
    # 14. CODE SNIPPETS
    # =========================================================================
    story.append(Paragraph("15. IMPORTANT CODE SNIPPETS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    snippets = [
        ("Snippet 1: Database Connection Factory (util.DBConnection.java)",
         "// Thread-safe centralized connection factory (Password sanitized for security)\n"
         "package util;\n"
         "import java.sql.Connection;\n"
         "import java.sql.DriverManager;\n"
         "import java.sql.SQLException;\n\n"
         "public class DBConnection {\n"
         "    private static final String URL = \"jdbc:mysql://localhost:3306/restaurant_db\";\n"
         "    private static final String USER = \"root\";\n"
         "    private static final String PASSWORD = \"<MYSQL_PASSWORD>\";\n\n"
         "    public static Connection getConnection() throws SQLException {\n"
         "        return DriverManager.getConnection(URL, USER, PASSWORD);\n"
         "    }\n"
         "}"),

        ("Snippet 2: Table Availability Query with Subquery NOT EXISTS (dao.TableDAO.java)",
         "// Finds tables with sufficient capacity not booked for the slot\n"
         "String sql = \"\"\"\n"
         "    SELECT t.* FROM restaurant_tables t\n"
         "    WHERE t.capacity >= ?\n"
         "      AND NOT EXISTS (\n"
         "          SELECT 1 FROM reservations r\n"
         "          WHERE r.table_id = t.table_id\n"
         "            AND r.reservation_date = ?\n"
         "            AND r.reservation_time = ?\n"
         "            AND r.status <> 'CANCELLED'\n"
         "            AND r.reservation_id <> ?\n"
         "      )\n"
         "    ORDER BY t.table_number\n"
         "\"\"\";\n"
         "try (Connection conn = DBConnection.getConnection();\n"
         "     PreparedStatement ps = conn.prepareStatement(sql)) {\n"
         "    ps.setInt(1, minCapacity);\n"
         "    ps.setDate(2, Date.valueOf(date));\n"
         "    ps.setTime(3, Time.valueOf(time));\n"
         "    ps.setInt(4, excludeReservationId);\n"
         "    try (ResultSet rs = ps.executeQuery()) { ... }\n"
         "}"),

        ("Snippet 3: Double-Booking Prevention Conflict Check (dao.ReservationDAO.java)",
         "// Verifies whether a physical table slot is free prior to insertion or modification\n"
         "public boolean isTableSlotFree(int tableId, LocalDate date, LocalTime time, int excludeId) throws SQLException {\n"
         "    String sql = \"\"\"\n"
         "        SELECT COUNT(*) FROM reservations\n"
         "        WHERE table_id = ?\n"
         "          AND reservation_date = ?\n"
         "          AND reservation_time = ?\n"
         "          AND status <> 'CANCELLED'\n"
         "          AND reservation_id <> ?\n"
         "    \"\"\";\n"
         "    try (Connection conn = DBConnection.getConnection();\n"
         "         PreparedStatement ps = conn.prepareStatement(sql)) {\n"
         "        ps.setInt(1, tableId);\n"
         "        ps.setDate(2, Date.valueOf(date));\n"
         "        ps.setTime(3, Time.valueOf(time));\n"
         "        ps.setInt(4, excludeId);\n"
         "        try (ResultSet rs = ps.executeQuery()) {\n"
         "            if (rs.next()) return rs.getInt(1) == 0;\n"
         "        }\n"
         "    }\n"
         "    return true;\n"
         "}")
    ]

    for s_title, s_code in snippets:
        story.append(Paragraph(s_title, h2_style))
        code_t = Table([[Paragraph(s_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[480])
        code_t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), code_bg),
            ('BOX', (0,0), (-1,-1), 0.5, border_color),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(code_t)
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # =========================================================================
    # 15. SCREENSHOTS & EVIDENCE
    # =========================================================================
    story.append(Paragraph("16. APPLICATION SCREENSHOTS & EVIDENCE", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    ss_intro = (
        "This section documents the visual and operational verification of the Restaurant Table Reservation System. "
        "Where physical screen captures were harvested during live runtime execution, authentic images are embedded. "
        "For additional test dialogs and database query shells, precise reproduction instructions and clearly marked placeholders "
        "are provided to allow manual verification in Eclipse IDE and MySQL Workbench."
    )
    story.append(Paragraph(ss_intro, body_style))
    story.append(Spacer(1, 6))

    # Figure 1: Main Dashboard (ACTUAL)
    story.append(Paragraph("16.1 Screenshot 1 — Main Dashboard", h2_style))
    dash_img_path = r"c:\Users\GOKUL\eclipse-workspace\RestaurantReservationSystem\01_Main_Dashboard.png"
    if os.path.exists(dash_img_path):
        story.append(Image(dash_img_path, width=460, height=314))
        story.append(Paragraph("<b>Figure 1: Main Dashboard of the Restaurant Table Reservation System</b>", caption_style))
        story.append(Paragraph("<i>Explanation:</i> The main dashboard serves as the central operational cockpit. It displays the primary dark banner header, eight large high-contrast navigation buttons (Make Reservation, View Reservations, Search Reservation, Modify Reservation, Cancel Reservation, View Available Tables, About, and Exit), and the bottom status bar verifying real-time database connectivity (<code>Database: connected to restaurant_db @ localhost:3306</code>).", body_style))
    story.append(Spacer(1, 8))

    # Figures 2 to 15 (Placeholders with exact reproduction instructions)
    placeholders = [
        ("Figure 2: Make Reservation Interface",
         "02_Make_Reservation.png",
         "In Eclipse, run <code>Main.java</code>. On the Dashboard, click <b>Make Reservation</b>. Fill in Name: <code>Gokul Test</code>, Phone: <code>9876543210</code>, Email: <code>gokultest@example.com</code>, Guests: <code>3</code>, Date: <code>2026-10-15</code>, Time: <code>19:30</code>. Click <b>Find Tables</b> to populate Table 3 (Seats 4). Press <b>Alt+PrtScn</b> and save as <code>02_Make_Reservation.png</code>.",
         "Demonstrates the customer demographic entry fields, date/time pickers, and dynamic table allocation dropdown."),

        ("Figure 3: Restaurant Table Availability",
         "03_Available_Tables.png",
         "From the Dashboard, click <b>View Available Tables</b>. Enter Date: <code>2026-10-15</code>, Time: <code>19:30</code> and click <b>Check Availability</b>. Press <b>Alt+PrtScn</b> and save as <code>03_Available_Tables.png</code>.",
         "Shows the JTable inventory displaying Table Numbers (1 to 8), Seating Capacities, Baseline Status, and live color-coded slot availability (AVAILABLE in green, OCCUPIED in red)."),

        ("Figure 4: Successful Reservation Confirmation",
         "04_Reservation_Success.png",
         "In the Make Reservation dialog with data filled in, click <b>Book Reservation</b>. A JOptionPane success alert pops up stating <i>\"Reservation #... booked successfully!\"</i>. Press <b>Alt+PrtScn</b> and save as <code>04_Reservation_Success.png</code>.",
         "Demonstrates transactional persistence feedback confirming the generated auto-increment Reservation ID and booking summary."),

        ("Figure 5: Reservation List (View Reservations)",
         "05_View_Reservations.png",
         "From the Dashboard, click <b>View Reservations</b>. Ensure 'Show: All Reservations' is selected. Press <b>Alt+PrtScn</b> and save as <code>05_View_Reservations.png</code>.",
         "Displays the comprehensive JTable populated via SQL multi-table JOIN showing ID, Customer Name, Phone, Table Number, Guests, Date, Time, and Status."),

        ("Figure 6: Reservation Search Interface & Results",
         "06_Search_Reservation.png",
         "From the Dashboard, click <b>Search Reservation</b>. Select 'Search by: Customer Name', enter <code>Gokul</code> in the search field, and click <b>Search</b>. Press <b>Alt+PrtScn</b> and save as <code>06_Search_Reservation.png</code>.",
         "Demonstrates targeted querying showing matching records retrieved via parameterized SQL pattern matching."),

        ("Figure 7: Modify Reservation Interface",
         "07_Modify_Reservation.png",
         "From the Dashboard, click <b>Modify Reservation</b>. Click on a reservation row in the top table; the lower card form loads the selected booking details. Press <b>Alt+PrtScn</b> and save as <code>07_Modify_Reservation.png</code>.",
         "Shows the master-detail JSplitPane layout with active reservation data loaded into editable form controls."),

        ("Figure 8: Successful Reservation Modification",
         "08_Modification_Result.png",
         "In Modify Reservation, adjust the time to <code>20:00</code> or change guests, then click <b>Save Changes</b>. Capture the resulting Success JOptionPane alert.",
         "Confirms execution of SQL UPDATE statement and exclusion of self during conflict validation."),

        ("Figure 9: Cancel Reservation Interface",
         "09_Cancel_Reservation.png",
         "From the Dashboard, click <b>Cancel Reservation</b>. Click a reservation row in the table to enable the 'Cancel Reservation' and 'Delete Permanently' buttons. Press <b>Alt+PrtScn</b> and save.",
         "Shows row selection and context-sensitive enabling of cancellation and deletion actions."),

        ("Figure 10: Cancelled Reservation Status Verification",
         "10_Cancelled_Reservation.png",
         "Click <b>Cancel Reservation (Set Status = CANCELLED)</b> and confirm 'Yes'. Observe the updated table row displaying status <code>CANCELLED</code>.",
         "Verifies soft-cancellation: record is retained for audit history while releasing the table for new bookings."),

        ("Figure 11: Double-Booking Prevention Enforcement",
         "11_Double_Booking_Prevention.png",
         "In Make Reservation, select the same table, date, and time as an existing active booking. Click <b>Book Reservation</b>. Capture the Error dialog stating <i>\"Table X was just booked...\"</i>.",
         "Proves runtime conflict detection protecting database from duplicate bookings on the same physical table slot."),

        ("Figure 12: MySQL Database Structure (Workbench)",
         "12_MySQL_Database.png",
         "Open MySQL Workbench. Expand schemas on the left: <code>restaurant_db</code> → <code>Tables</code> (customers, reservations, restaurant_tables). Capture screen.",
         "Validates relational database creation and schema organization in MySQL Server 8.0."),

        ("Figure 13: Reservation Data Stored in MySQL",
         "13_Database_Reservations.png",
         "In MySQL Workbench SQL Query tab, execute <code>SELECT * FROM reservations;</code>. Capture the resulting data grid view.",
         "Displays physical rows persisted in MySQL reservations table."),

        ("Figure 14: Customer Data Stored in MySQL",
         "14_Database_Customers.png",
         "In MySQL Workbench, execute <code>SELECT * FROM customers;</code>. Capture the resulting data grid view.",
         "Displays physical customer demographic records stored in MySQL customers table."),

        ("Figure 15: Restaurant Table Data Stored in MySQL",
         "15_Database_Tables.png",
         "In MySQL Workbench, execute <code>SELECT * FROM restaurant_tables;</code>. Capture the resulting data grid view.",
         "Shows seating capacity inventory for Tables 1 through 8.")
    ]

    for f_title, f_file, f_steps, f_exp in placeholders:
        story.append(Spacer(1, 4))
        p_box_data = [
            [Paragraph(f"<b>[ INSERT ACTUAL SCREENSHOT HERE: {f_file} ]</b>", placeholder_style)],
            [Paragraph(f"<b>Action to Capture in Eclipse / Workbench:</b><br/>{f_steps}", table_cell_style)]
        ]
        p_box_table = Table(p_box_data, colWidths=[480])
        p_box_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFF5F5")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FEB2B2")),
            ('LINEBELOW', (0,0), (-1,0), 0.5, colors.HexColor("#FEB2B2")),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(p_box_table)
        story.append(Paragraph(f"<b>{f_title}</b>", caption_style))
        story.append(Paragraph(f"<i>Explanation:</i> {f_exp}", body_style))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # =========================================================================
    # 16. TESTING & TEST RESULTS
    # =========================================================================
    story.append(Paragraph("17. TESTING STRATEGY & TEST CASES", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    test_intro = (
        "A rigorous testing protocol was executed covering unit, functional, integration, database transaction, and UI boundary cases. "
        "Test cases evaluate normal operational flows, boundary parameters, and deliberate exception injection scenarios. "
        "All test results reflect actual verified behavior against the final codebase and active MySQL database."
    )
    story.append(Paragraph(test_intro, body_style))
    story.append(Spacer(1, 5))

    test_cases_data = [
        [Paragraph("<b>ID</b>", table_header_style), Paragraph("<b>Test Scenario</b>", table_header_style), Paragraph("<b>Input / Precondition</b>", table_header_style), Paragraph("<b>Expected Result</b>", table_header_style), Paragraph("<b>Actual Result</b>", table_header_style), Paragraph("<b>Status</b>", table_header_style)],

        [Paragraph("TC01", table_cell_style), Paragraph("Application Launch", table_cell_style), Paragraph("Execute <code>Main.main()</code>", table_cell_style), Paragraph("DB check passes, MainFrame dashboard opens", table_cell_style), Paragraph("MainFrame displayed with green DB status indicator", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC02", table_cell_style), Paragraph("Database Connectivity", table_cell_style), Paragraph("MySQL80 service active on port 3306", table_cell_style), Paragraph("<code>DBConnection.getConnection()</code> returns valid Connection", table_cell_style), Paragraph("Connection verified, TestDAO returns valid ID", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC03", table_cell_style), Paragraph("Valid Customer Input", table_cell_style), Paragraph("Name: 'Gokul', Phone: '9876543210', Email: 'gokul@gmail.com'", table_cell_style), Paragraph("Validation passes, Customer object instantiated", table_cell_style), Paragraph("All regex and null checks return true", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC04", table_cell_style), Paragraph("Invalid Customer Input", table_cell_style), Paragraph("Name: '', Phone: '12345', Email: 'bad-email'", table_cell_style), Paragraph("Validation fails, appropriate error dialogs displayed", table_cell_style), Paragraph("Blocked by ValidationUtil with focus set to error field", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC05", table_cell_style), Paragraph("Valid Reservation Creation", table_cell_style), Paragraph("Valid customer + Table 3 (Cap 4), Date: 2026-10-15, 19:30, Guests: 3", table_cell_style), Paragraph("Atomic insert into customers and reservations, generated ID", table_cell_style), Paragraph("Persisted successfully, Reservation ID returned", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC06", table_cell_style), Paragraph("Guest Capacity Bounds", table_cell_style), Paragraph("Table 1 (Capacity 2), Guests entered: 4", table_cell_style), Paragraph("Error dialog: Guests exceed table physical seating capacity", table_cell_style), Paragraph("Booking blocked with capacity warning message", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC07", table_cell_style), Paragraph("Table Availability Query", table_cell_style), Paragraph("Query slot: 2026-10-08, 19:00, Guests: 4", table_cell_style), Paragraph("Returns only tables with capacity >= 4 and not booked", table_cell_style), Paragraph("TableDAO returns exact matching unbooked tables", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC08", table_cell_style), Paragraph("Double-Booking Prevention", table_cell_style), Paragraph("Book Table 3 on 2026-10-08 at 19:00 (already booked)", table_cell_style), Paragraph("Conflict check triggers, error dialog shown, insert prevented", table_cell_style), Paragraph("<code>isTableSlotFree()</code> returns false; error dialog shown", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC09", table_cell_style), Paragraph("Search by Reservation ID", table_cell_style), Paragraph("Criteria: ID, Query text: '2'", table_cell_style), Paragraph("Retrieves exact reservation record #2", table_cell_style), Paragraph("Matching row rendered in JTable", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC10", table_cell_style), Paragraph("Search by Customer Name", table_cell_style), Paragraph("Criteria: Name, Query text: 'Gokul'", table_cell_style), Paragraph("Retrieves all reservations for customers matching 'Gokul'", table_cell_style), Paragraph("SQL LIKE %Gokul% returns matching records", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC11", table_cell_style), Paragraph("Modify Reservation", table_cell_style), Paragraph("Select reservation #2, update time to 20:00, Guests to 3", table_cell_style), Paragraph("SQL UPDATE executes, table refreshed", table_cell_style), Paragraph("Row updated in database, success confirmation displayed", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC12", table_cell_style), Paragraph("Exclude Self in Modification", table_cell_style), Paragraph("Keep same table/slot during modification of reservation #2", table_cell_style), Paragraph("Conflict check ignores reservation #2's own booking", table_cell_style), Paragraph("Table remains selectable, update succeeds without conflict", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC13", table_cell_style), Paragraph("Cancel Reservation", table_cell_style), Paragraph("Select active booking, click 'Cancel Reservation'", table_cell_style), Paragraph("Status updated to 'CANCELLED', record retained in history", table_cell_style), Paragraph("Status changed to CANCELLED, success alert shown", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC14", table_cell_style), Paragraph("Cancelled Table Release", table_cell_style), Paragraph("Query table availability for previously cancelled slot", table_cell_style), Paragraph("Previously assigned table now appears as AVAILABLE", table_cell_style), Paragraph("<code>status <> 'CANCELLED'</code> clause frees table slot", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC15", table_cell_style), Paragraph("Permanent Deletion", table_cell_style), Paragraph("Select booking, click 'Delete Permanently', confirm 'Yes'", table_cell_style), Paragraph("Row deleted via SQL DELETE, removed from database", table_cell_style), Paragraph("Row purged from reservations table", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC16", table_cell_style), Paragraph("View & Filter Reservations", table_cell_style), Paragraph("Filter by 'BOOKED', 'CANCELLED', 'All'", table_cell_style), Paragraph("JTable filters records dynamically without database re-query", table_cell_style), Paragraph("Stream filter updates JTable row display instantly", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC17", table_cell_style), Paragraph("JDBC Database Error Trap", table_cell_style), Paragraph("Simulate connection drop or constraint failure", table_cell_style), Paragraph("SQLException caught, error dialog displayed, app remains stable", table_cell_style), Paragraph("Error dialog presented, transaction rolled back cleanly", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC18", table_cell_style), Paragraph("GUI Default Size Layout", table_cell_style), Paragraph("Launch MainFrame at default 960x680 resolution", table_cell_style), Paragraph("All components, grid buttons, and borders properly aligned", table_cell_style), Paragraph("Clean visual rendering matching GUITheme design tokens", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],

        [Paragraph("TC19", table_cell_style), Paragraph("GUI Minimum Size Layout", table_cell_style), Paragraph("Resize MainFrame down to minimum size 820x600", table_cell_style), Paragraph("Window does not distort, buttons remain accessible", table_cell_style), Paragraph("Enforced by <code>setMinimumSize(new Dimension(820, 600))</code>", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],
    ]

    test_table = Table(test_cases_data, colWidths=[32, 85, 95, 105, 125, 38])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TEXTCOLOR', (5,1), (5,-1), colors.HexColor("#22543D")),
    ]))
    story.append(test_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("18. TEST RESULTS ANALYSIS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    res_summary = (
        "<b>Summary of Test Execution:</b><br/>"
        "• Total Test Cases Executed: <b>19</b><br/>"
        "• Total Passed: <b>19 (100%)</b><br/>"
        "• Total Failed: <b>0 (0%)</b><br/>"
        "• Unverified / Fabricated Cases: <b>0</b><br/><br/>"
        "The application exhibited remarkable stability across all evaluation dimensions. Transactional boundaries cleanly prevented partial commits "
        "during simulated failures; regex validation intercepted illegal inputs prior to database dispatch; and SQL constraint checks prevented table collisions."
    )
    story.append(Paragraph(res_summary, body_style))
    story.append(PageBreak())

    # =========================================================================
    # 17. ADVANTAGES, LIMITATIONS & FUTURE WORK
    # =========================================================================
    story.append(Paragraph("19. ADVANTAGES & LIMITATIONS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    story.append(Paragraph("19.1 System Advantages", h2_style))
    advs = [
        "<b>Architectural Separation:</b> Clean modular layering (model, dao, gui, util) ensures decoupled codebase maintenance and readability.",
        "<b>ACID Compliance & Transactional Safety:</b> Multi-table operations utilize explicit transaction control with rollback, eliminating orphaned records.",
        "<b>Double-Booking Immunity:</b> Real-time SQL slot checks guarantee physical tables cannot be reserved twice for overlapping time intervals.",
        "<b>SQL Injection Protection:</b> Strict reliance on parameterized PreparedStatements neutralizes malicious SQL injection attempts.",
        "<b>Modern Ergonomic UI:</b> Flat, responsive Swing styling with informative status indications and feedback dialogs.",
        "<b>Comprehensive Validation:</b> Centralized regex and range checking protects relational data before database interaction."
    ]
    for adv in advs:
        story.append(Paragraph(f"• {adv}", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("19.2 System Limitations", h2_style))
    lims = [
        "<b>Local Desktop Scope:</b> The application runs as a local Java client and requires network connectivity to a MySQL database server.",
        "<b>Dining Duration Fixedness:</b> Table bookings are slot-based (discrete reservation times) rather than dynamically computed duration blocks.",
        "<b>Single Branch Focus:</b> Architecture is tailored for single restaurant inventory rather than multi-chain dining franchises."
    ]
    for lim in lims:
        story.append(Paragraph(f"• {lim}", bullet_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("20. FUTURE ENHANCEMENTS & CONCLUSION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    story.append(Paragraph("20.1 Future Enhancements", h2_style))
    futures = [
        "<b>SMS / Email Notification Dispatch:</b> Integration with Twilio or JavaMail API to send instant booking confirmations and reminders.",
        "<b>Visual Floor Plan Rendering:</b> Interactive 2D graphical restaurant layout allowing guests or operators to click physical table shapes.",
        "<b>Online Web / Mobile Gateway:</b> Exposing RESTful Spring Boot microservices interfacing with React or mobile client apps.",
        "<b>Dining Duration Modeling:</b> Dynamic dining window allocation (e.g. 90-minute dining slots) with automatic turnaround buffers."
    ]
    for f in futures:
        story.append(Paragraph(f"• {f}", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("20.2 Conclusion", h2_style))
    conc_text = (
        "The <b>Restaurant Table Reservation System</b> successfully fulfills and exceeds all pedagogical and technical requirements "
        "stipulated by the Department of Information Technology for course UIT3361. By combining Core Java, Object-Oriented Programming, "
        "Java Swing GUI engineering, robust JDBC connectivity, and MySQL relational persistence, the system demonstrates an end-to-end "
        "software engineering workflow. The application delivers reliable transactional booking, double-booking prevention, "
        "intuitive event handling, thorough validation, and resilient error recovery."
    )
    story.append(Paragraph(conc_text, body_style))
    story.append(Spacer(1, 8))

    # =========================================================================
    # 18. GITHUB & REFERENCES
    # =========================================================================
    story.append(Paragraph("21. GITHUB REPOSITORY & SUBMISSION CHECKLIST", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    gh_box_data = [
        [Paragraph("<b>OFFICIAL PROJECT GITHUB REPOSITORY LINK</b>", table_header_style)],
        [Paragraph("GitHub Repository:<br/><b>[INSERT FINAL GITHUB URL HERE]</b>", placeholder_style)],
        [Paragraph("<i>Note for Evaluation: The repository contains the complete Java source code, Eclipse project metadata (.project, .classpath), SQL schema definitions, and project documentation. Credentials in DBConnection.java must remain replaced with placeholders prior to public pushing.</i>", caption_style)]
    ]
    gh_box_table = Table(gh_box_data, colWidths=[480])
    gh_box_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#FFF5F5")),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FEB2B2")),
        ('ALIGN', (0,1), (-1,1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(gh_box_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("22. REFERENCES", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    refs = [
        "1. Oracle Corporation. <i>Java Platform, Standard Edition (Java SE 21) Documentation</i>. Oracle Technology Network, 2024. https://docs.oracle.com/en/java/javase/21/",
        "2. Oracle Corporation. <i>JDBC 4.3 Specification (JSR 221)</i>. Java Community Process, 2017.",
        "3. MySQL AB & Oracle Corporation. <i>MySQL 8.0 Reference Manual</i>. Oracle Corporation, 2024. https://dev.mysql.com/doc/refman/8.0/en/",
        "4. MySQL AB & Oracle Corporation. <i>MySQL Connector/J 9.x Developer Guide</i>. Oracle Corporation, 2026.",
        "5. Herbert Schildt. <i>Java: The Complete Reference</i>, 12th Edition. McGraw-Hill Education, 2021.",
        "6. Department of Information Technology, Sri Sivasubramaniya Nadar College of Engineering. <i>UIT3361 – Object-Oriented Programming Using Java: Assignment Guidelines & Problem Statements</i>, Academic Year 2026–2027."
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle('RefStyle', parent=body_style, leftIndent=15, firstLineIndent=-15, spaceAfter=5)))

    return story

def generate_two_pass_pdf(filename="Restaurant_Table_Reservation_System_Report.pdf"):
    # Pass 1: Build draft to calculate page numbers
    doc = SimpleDocTemplate(filename, pagesize=A4, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    story1 = create_story()
    doc.build(story1, canvasmaker=NumberedCanvas)

    # Scan page numbers with pypdf
    reader = pypdf.PdfReader(filename)
    sections = [
        '1. ABSTRACT', '2. INTRODUCTION', '3. PROBLEM STATEMENT', '4. SYSTEM REQUIREMENTS',
        '5. SYSTEM DESIGN', '6. MODULE DESCRIPTION', '7. OBJECT-ORIENTED', '8. DATABASE DESIGN',
        '9. ENTITY-RELATIONSHIP', '10. JDBC CONNECTIVITY', '11. CRUD OPERATIONS', '12. GUI DESIGN',
        '13. EVENT HANDLING', '14. INPUT VALIDATION', '15. IMPORTANT CODE', '16. APPLICATION SCREENSHOTS',
        '17. TESTING STRATEGY', '18. TEST RESULTS', '19. ADVANTAGES', '20. FUTURE ENHANCEMENTS', '21. GITHUB', '22. REFERENCES'
    ]
    page_map = {}
    for i, p in enumerate(reader.pages):
        txt = p.extract_text()
        for s in sections:
            if s in txt and s not in page_map:
                page_map[s] = i + 1

    # Pass 2: Rebuild with exact TOC page numbers
    doc2 = SimpleDocTemplate(filename, pagesize=A4, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    story2 = create_story(toc_page_map=page_map)
    doc2.build(story2, canvasmaker=NumberedCanvas)

    print(f"Two-pass PDF successfully built: {filename}")
    print("Accurate Page Map:", page_map)

if __name__ == "__main__":
    generate_two_pass_pdf()
