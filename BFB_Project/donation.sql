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






