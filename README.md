# Restaurant Table Reservation System 🍽️

A desktop-based Restaurant Table Reservation & Management System built with **Java (Swing GUI)** and **MySQL** utilizing the **DAO (Data Access Object) architectural pattern**.

---

## 📌 Features

### 🔐 Dual-Role Authentication & Security
- **Role-Based Access Control (RBAC)**: Separate portals for **Admin** (Staff) and **Customer**.
- **Password Security**: Passwords are cryptographically secured using **SHA-256** combined with a unique 32-character random salt per user (no plain text storage).
- **Default Admin Account**: Auto-seeded on first run (`admin` / `admin123`).

### 👨‍💼 Admin Dashboard
- **Live Metrics Cards**: Total Tables, Active Bookings, Today's Scheduled Reservations, Registered Customers.
- **Reservation Management**: View all reservations with filter tabs (`All`, `BOOKED`, `COMPLETED`, `CANCELLED`).
- **Table Management**: Real-time table status monitoring and slot-based availability computation.
- **Search & Filter**: Search reservations by customer name, phone number, or reservation ID.
- **Modification & Cancellation**: Update date, time, table, or guest count with conflict prevention.

### 👤 Customer Portal
- **Self-Service Booking**: Select dates, timeslots, and party size; automatically filters available tables.
- **Booking History**: Customers can view only their own past and upcoming reservations.
- **Self Cancellation**: Cancel active upcoming reservations directly from the customer dashboard.

### 🛡️ Database & Architectural Integrity
- **ACID Transactions**: Atomic transactions (`setAutoCommit(false)`) ensure customer registration and booking occur together or roll back on failure.
- **SQL Injection Prevention**: Safe parameter binding using `PreparedStatement` across all queries.
- **Defensive Validation**: Form input validation (phone format, email, party sizes, date/time logic).

---

## 🛠️ Tech Stack & Requirements

- **Language**: Java 21 (Java SE 21)
- **GUI Framework**: Java Swing & AWT
- **Database**: MySQL 8.0+
- **Connectivity**: MySQL Connector/J (`mysql-connector-j-9.7.0.jar`)
- **IDE**: Eclipse IDE / IntelliJ IDEA / VS Code

---

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/thenameisrghratgit/restaurant_management.git
cd restaurant_management
```

### 2. Database Setup
1. Start your local MySQL server.
2. Run the provided [`schema.sql`](schema.sql) in MySQL Workbench, MySQL CLI, or phpMyAdmin:
```sql
SOURCE schema.sql;
```
3. Update database credentials in [`src/util/DBConnection.java`](src/util/DBConnection.java) if your MySQL port/password differs:
```java
private static final String URL = "jdbc:mysql://localhost:3306/restaurant_db";
private static final String USER = "root";
private static final String PASSWORD = "your_mysql_password";
```

### 3. Build & Run
#### In Eclipse:
1. Open Eclipse > **File** > **Import...** > **Existing Projects into Workspace**.
2. Select the repository root folder.
3. Ensure MySQL Connector JAR is in your project build path.
4. Run `src/Main.java`.

#### From Command Line:
```powershell
# Compile
javac -cp ".;lib/mysql-connector-j-9.7.0.jar" -d bin src/**/*.java

# Run
java -cp "bin;lib/mysql-connector-j-9.7.0.jar" Main
```

---

## 📂 Project Structure

```text
RestaurantReservationSystem/
├── src/
│   ├── Main.java                  # Application entry point
│   ├── dao/                       # Data Access Objects (UserDAO, CustomerDAO, etc.)
│   ├── gui/                       # Swing UI panels, dialogs, and themes
│   ├── model/                     # Data entity models (Customer, Reservation, Table, User)
│   └── util/                      # DBConnection, PasswordUtil, ValidationUtil
├── schema.sql                     # Database schema definition & seed data
├── .gitignore                     # Git ignore rules
└── README.md                      # Project documentation
```

---

## 📄 License
This project is open-source and available for educational and commercial use.
