-- init.sql
-- Bank Management System - Database Initialization
-- Creates the database, the users table, and inserts sample data.

CREATE DATABASE IF NOT EXISTS bank_system;
USE bank_system;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    balance DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample data (password values shown are placeholders;
-- the backend hashes real passwords with bcrypt on registration)
INSERT INTO users (username, password, balance)
VALUES
    ('mohamed', '$2b$12$placeholderhashvalueplaceholderhashvalueplaceh', 5000.00),
    ('sara', '$2b$12$placeholderhashvalueplaceholderhashvalueplaceh', 1200.50)
ON DUPLICATE KEY UPDATE username = username;
