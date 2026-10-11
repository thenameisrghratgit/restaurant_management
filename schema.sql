-- Restaurant Reservation System Database Schema

CREATE DATABASE IF NOT EXISTS restaurant_db;
USE restaurant_db;

-- 1. Customers Table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100)
);

-- 2. Restaurant Tables Table
CREATE TABLE IF NOT EXISTS restaurant_tables (
    table_id INT AUTO_INCREMENT PRIMARY KEY,
    table_number INT NOT NULL UNIQUE,
    capacity INT NOT NULL,
    status VARCHAR(20) DEFAULT 'AVAILABLE'
);

-- 3. Reservations Table
CREATE TABLE IF NOT EXISTS reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    table_id INT NOT NULL,
    reservation_date DATE NOT NULL,
    reservation_time TIME NOT NULL,
    guests INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'BOOKED',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (table_id) REFERENCES restaurant_tables(table_id) ON DELETE CASCADE
);

-- 4. Users Table (Authentication & RBAC)
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    salt VARCHAR(32) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    role VARCHAR(20) NOT NULL,
    customer_id INT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE SET NULL
);

-- Seed Initial Tables (8 standard tables with varying capacities)
INSERT IGNORE INTO restaurant_tables (table_number, capacity, status) VALUES
(1, 2, 'AVAILABLE'),
(2, 2, 'AVAILABLE'),
(3, 4, 'AVAILABLE'),
(4, 4, 'AVAILABLE'),
(5, 6, 'AVAILABLE'),
(6, 6, 'AVAILABLE'),
(7, 8, 'AVAILABLE'),
(8, 8, 'AVAILABLE');
