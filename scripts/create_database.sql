-- Create GRADLINK database
CREATE DATABASE IF NOT EXISTS gradlink_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create a user for the application (optional)
-- CREATE USER 'gradlink_user'@'localhost' IDENTIFIED BY 'your_secure_password';
-- GRANT ALL PRIVILEGES ON gradlink_db.* TO 'gradlink_user'@'localhost';
-- FLUSH PRIVILEGES;

USE gradlink_db;

-- The Django ORM will create the actual tables when you run migrations
-- This script just ensures the database exists
