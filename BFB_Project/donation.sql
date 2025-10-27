--Donation Management System - SQlite database schema
-- Database: donation_management.db

--Enable foreign key constraints
PRAGMA foreign_keys = ON;

--Drop existing tables if they exist
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS donor_store_profiles;
DROP TABLE IF EXISTS npo_profiles;
DROP TABLE IF EXISTS donation_records;
DROP TABLE IF EXISTS donation_item_details;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS pickup_scheduling;
DROP TABLE IF EXISTS collected_items;
DROP TABLE IF EXISTS distribution_centers;
DROP TABLE IF EXISTS sorting_records;
DROP TABLE IF EXISTS delivery_routes;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS distributed_items;
DROP TABLE IF EXISTS delivery_confirmations;
DROP TABLE IF EXISTS feedback_reviews;
DROP TABLE IF EXISTS admin_logs;

--- SQL script to create a table for storing user information
CREATE TABLE users (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('donor', 'npo') NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

--- SQL script to create a table for storing donor store profiles
CREATE TABLE donor_store_profiles (
    donor_store_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(15),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    country VARCHAR(50),
    date_of_birth DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    FOREIGN KEY (donor_store_id) REFERENCES users(user_id)
);

--- SQL script to create a table for storing non-profit organization profiles
CREATE TABLE npo_profiles (
    npo_id INT PRIMARY KEY,
    npo_name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(15),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    FOREIGN KEY (npo_id) REFERENCES users(user_id)
);
--- SQL script to create a table for storing donation records
CREATE TABLE donation_records (
    donation_id INT PRIMARY KEY,
    donor_store_id INT,
    donation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    donation_amount DECIMAL(10, 2) NOT NULL,
    donation_type VARCHAR(50),
    notes TEXT,
    FOREIGN KEY (donor_store_id) REFERENCES donor_store_profiles(donor_store_id)
);

--- SQL script to create a table for storing donation item details
CREATE TABLE donation_item_details (
    item_id INT PRIMARY KEY,
    donation_id INT,
    item_name VARCHAR(100) NOT NULL,
    item_description TEXT,
    item_quantity INT NOT NULL,
    item_value DECIMAL(10, 2),
    FOREIGN KEY (donation_id) REFERENCES donation_records(donation_id)
);

--- SQL script to create a table for storing notifications
CREATE TABLE notifications (
  notification_id INT PRIMARY KEY AUTO_INCREMENT,
  sender_role ENUM('store', 'system', 'admin'),
  recipient_role ENUM('admin', 'npo'),
  message TEXT,
  related_item_id INT,
  notification_type ENUM('donation_ready', 'stock_available', 'pickup_scheduled'),
  sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


--- SQL script to create a table for storing pickup scheduling information
CREATE TABLE pickup_scheduling (
    pickup_id INT PRIMARY KEY,
    donor_store_id INT,
    scheduled_date TIMESTAMP NOT NULL,
    pickup_address TEXT,
    contact_person VARCHAR(100),
    contact_phone VARCHAR(15),
    status VARCHAR(50) DEFAULT 'Scheduled',
    FOREIGN KEY (donor_store_id) REFERENCES donor_store_profiles(donor_store_id)
);

--- SQL script to create a table for storing collected items during pickups
CREATE TABLE collected_items (
    collected_item_id INT PRIMARY KEY,
    pickup_id INT,
    item_name VARCHAR(100) NOT NULL,
    item_quantity INT NOT NULL,
    item_condition VARCHAR(100),
    FOREIGN KEY (pickup_id) REFERENCES pickup_scheduling(pickup_id)
);

--- SQL script to create a table for storing distribution center information
CREATE TABLE distribution_centers (
    center_id INT PRIMARY KEY,
    center_name VARCHAR(100) NOT NULL,
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    country VARCHAR(50),
    contact_person VARCHAR(100),
    contact_phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--- SQL script to create a table for storing sorting records
CREATE TABLE sorting_records (
  sorting_id INT PRIMARY KEY AUTO_INCREMENT,
  collected_item_id INT,
  center_id INT,
  sorted_category VARCHAR(100),
  sorted_quantity INT,
  sorted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (collected_item_id) REFERENCES collected_items(collected_item_id),
  FOREIGN KEY (center_id) REFERENCES distribution_centers(center_id)
);

--- SQL script to create a table for storing delivery routes
CREATE TABLE delivery_routes (
  route_id INT PRIMARY KEY AUTO_INCREMENT,
  distribution_id INT,
  origin_address TEXT,
  destination_address TEXT,
  estimated_delivery_time TIME,
  route_status ENUM('planned', 'in_transit', 'completed') DEFAULT 'planned',
  FOREIGN KEY (distribution_id) REFERENCES distributed_items(distribution_id)
);

--- SQL script to create a table for storing inventory at distribution centers
CREATE TABLE inventory (
  inventory_id INT PRIMARY KEY AUTO_INCREMENT,
  center_id INT,
  item_name VARCHAR(100),
  quantity INT,
  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (center_id) REFERENCES distribution_centers(center_id)
);

--- SQL script to create a table for storing distributed items
CREATE TABLE distributed_items (
    distribution_id INT PRIMARY KEY,
    center_id INT,
    item_name VARCHAR(100) NOT NULL,
    item_quantity INT NOT NULL,
    distribution_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (center_id) REFERENCES distribution_centers(center_id)
);

--- SQL script to create a table for storing delivery confirmations
CREATE TABLE delivery_confirmations (
    confirmation_id INT PRIMARY KEY,
    distribution_id INT,
    received_by VARCHAR(100),
    received_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (distribution_id) REFERENCES distributed_items(distribution_id)
);

--- SQL script to create a table for storing feedback and reviews
CREATE TABLE feedback_reviews (
    review_id INT PRIMARY KEY,
    donor_store_id INT,
    npo_id INT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comments TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_store_id) REFERENCES donor_store_profiles(donor_store_id),
    FOREIGN KEY (npo_id) REFERENCES npo_profiles(npo_id)
);

--- SQL script to create a table for storing admin logs
CREATE TABLE admin_logs (
  log_id INT PRIMARY KEY AUTO_INCREMENT,
  admin_id INT,
  action_type VARCHAR(100),
  target_table VARCHAR(100),
  target_id INT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  notes TEXT,
  FOREIGN KEY (admin_id) REFERENCES users(user_id)
);

-- Seed users
INSERT INTO users (user_id, name, email, password_hash, role) VALUES
(1, 'Admin User', 'admin@example.com', 'admin123hash', 'donor'),
(2, 'Alice Donor', 'alice@example.com', 'alice123hash', 'donor'),
(3, 'Bob Donor', 'bob@example.com', 'bob123hash', 'donor'),
(4, 'Hope Foundation', 'hope@example.com', 'hope123hash', 'npo'),
(5, 'Care Connect', 'care@example.com', 'care123hash', 'npo');

-- Donor profiles
INSERT INTO donor_store_profiles (donor_store_id, first_name, last_name, email, phone_number, address, city, state, zip_code, country, date_of_birth)
VALUES
(2, 'Alice', 'Smith', 'alice@example.com', '0123456789', '123 Elm St', 'Pretoria', 'Gauteng', '0001', 'South Africa', '1985-06-15'),
(3, 'Bob', 'Moyo', 'bob@example.com', '0987654321', '456 Oak St', 'Pretoria', 'Gauteng', '0002', 'South Africa', '1990-09-20');

-- NPO profiles
INSERT INTO npo_profiles (npo_id, npo_name, contact_person, email, phone_number, address, city, state, zip_code, country)
VALUES
(4, 'Hope Foundation', 'Lindiwe Khumalo', 'hope@example.com', '0112233445', '789 Charity Rd', 'Pretoria', 'Gauteng', '0003', 'South Africa'),
(5, 'Care Connect', 'Thabo Ncube', 'care@example.com', '0119988776', '321 Help Ave', 'Pretoria', 'Gauteng', '0004', 'South Africa');

-- Donations
INSERT INTO donation_records (donation_id, donor_store_id, donation_amount, donation_type, notes)
VALUES
(1, 2, 500.00, 'monetary', 'Monthly donation'),
(2, 3, 0.00, 'in-kind', 'Winter supplies'),
(3, 2, 250.00, 'monetary', 'Emergency relief');

-- Donation items
INSERT INTO donation_item_details (item_id, donation_id, item_name, item_description, item_quantity, item_value)
VALUES
(1, 2, 'Blanket', 'Warm fleece blanket', 10, 50.00),
(2, 2, 'Jacket', 'Winter jacket, assorted sizes', 5, 75.00);

-- Pickup scheduling
INSERT INTO pickup_scheduling (pickup_id, donor_store_id, scheduled_date, pickup_address, contact_person, contact_phone)
VALUES
(1, 3, '2025-10-28 10:00:00', '456 Oak St, Pretoria', 'Bob Moyo', '0987654321');

-- Collected items
INSERT INTO collected_items (collected_item_id, pickup_id, item_name, item_quantity, item_condition)
VALUES
(1, 1, 'Blanket', 10, 'Good'),
(2, 1, 'Jacket', 5, 'Excellent');

-- Distribution center
INSERT INTO distribution_centers (center_id, center_name, address, city, state, zip_code, country, contact_person, contact_phone)
VALUES
(1, 'Pretoria Distribution Hub', '1 Hub Way', 'Pretoria', 'Gauteng', '0010', 'South Africa', 'Sibongile Dlamini', '0113344556');

-- Sorting records
INSERT INTO sorting_records (sorting_id, collected_item_id, center_id, sorted_category, sorted_quantity)
VALUES
(1, 1, 1, 'Blankets', 10),
(2, 2, 1, 'Clothing', 5);

-- Inventory
INSERT INTO inventory (inventory_id, center_id, item_name, quantity)
VALUES
(1, 1, 'Blanket', 10),
(2, 1, 'Jacket', 5);

-- Distributed items
INSERT INTO distributed_items (distribution_id, center_id, item_name, item_quantity)
VALUES
(1, 1, 'Blanket', 5),
(2, 1, 'Jacket', 2);

-- Delivery confirmations
INSERT INTO delivery_confirmations (confirmation_id, distribution_id, received_by, notes)
VALUES
(1, 1, 'Hope Foundation', 'Received in good condition'),
(2, 2, 'Care Connect', 'Delivered successfully');

-- Feedback reviews
INSERT INTO feedback_reviews (review_id, donor_store_id, npo_id, rating, comments)
VALUES
(1, 2, 4, 5, 'Great communication and impact'),
(2, 3, 5, 4, 'Smooth pickup and delivery');

-- Notifications
INSERT INTO notifications (notification_id, sender_role, recipient_role, message, related_item_id, notification_type)
VALUES
(1, 'system', 'npo', 'New donation ready for pickup', 1, 'donation_ready'),
(2, 'admin', 'npo', 'Stock available at distribution center', 2, 'stock_available');

-- Admin logs
INSERT INTO admin_logs (log_id, admin_id, action_type, target_table, target_id, notes)
VALUES
(1, 1, 'INSERT', 'donation_records', 3, 'Emergency donation logged'),
(2, 1, 'UPDATE', 'inventory', 1, 'Inventory adjusted after sorting');





