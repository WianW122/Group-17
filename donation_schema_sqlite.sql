PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS admin_logs;
DROP TABLE IF EXISTS feedback_reviews;
DROP TABLE IF EXISTS delivery_confirmations;
DROP TABLE IF EXISTS distributed_items;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS delivery_routes;
DROP TABLE IF EXISTS sorting_records;
DROP TABLE IF EXISTS distribution_centers;
DROP TABLE IF EXISTS collected_items;
DROP TABLE IF EXISTS pickup_scheduling;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS donation_item_details;
DROP TABLE IF EXISTS donation_records;
DROP TABLE IF EXISTS npo_profiles;
DROP TABLE IF EXISTS donor_store_profiles;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL CHECK(role IN ('donor','npo','admin')),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE donor_store_profiles (
  donor_store_id INTEGER PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  phone_number TEXT,
  address TEXT,
  city TEXT,
  state TEXT,
  zip_code TEXT,
  country TEXT,
  date_of_birth DATE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (donor_store_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE npo_profiles (
  npo_id INTEGER PRIMARY KEY,
  npo_name TEXT NOT NULL,
  contact_person TEXT,
  email TEXT UNIQUE NOT NULL,
  phone_number TEXT,
  address TEXT,
  city TEXT,
  state TEXT,
  zip_code TEXT,
  country TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (npo_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE donation_records (
  donation_id INTEGER PRIMARY KEY,
  donor_store_id INTEGER,
  donation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  donation_amount REAL NOT NULL,
  donation_type TEXT,
  notes TEXT,
  FOREIGN KEY (donor_store_id) REFERENCES donor_store_profiles(donor_store_id) ON DELETE SET NULL
);

CREATE TABLE donation_item_details (
  item_id INTEGER PRIMARY KEY,
  donation_id INTEGER,
  item_name TEXT NOT NULL,
  item_description TEXT,
  item_quantity INTEGER NOT NULL,
  item_value REAL,
  FOREIGN KEY (donation_id) REFERENCES donation_records(donation_id) ON DELETE CASCADE
);

CREATE TABLE notifications (
  notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
  sender_role TEXT CHECK(sender_role IN ('store','system','admin')),
  recipient_role TEXT CHECK(recipient_role IN ('admin','npo')),
  message TEXT,
  related_item_id INTEGER,
  notification_type TEXT CHECK(notification_type IN ('donation_ready','stock_available','pickup_scheduled')),
  sent_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pickup_scheduling (
  pickup_id INTEGER PRIMARY KEY,
  donor_store_id INTEGER,
  scheduled_date DATETIME NOT NULL,
  pickup_address TEXT,
  contact_person TEXT,
  contact_phone TEXT,
  status TEXT DEFAULT 'Scheduled',
  FOREIGN KEY (donor_store_id) REFERENCES donor_store_profiles(donor_store_id) ON DELETE SET NULL
);

CREATE TABLE collected_items (
  collected_item_id INTEGER PRIMARY KEY,
  pickup_id INTEGER,
  item_name TEXT NOT NULL,
  item_quantity INTEGER NOT NULL,
  item_condition TEXT,
  FOREIGN KEY (pickup_id) REFERENCES pickup_scheduling(pickup_id) ON DELETE CASCADE
);

CREATE TABLE distribution_centers (
  center_id INTEGER PRIMARY KEY,
  center_name TEXT NOT NULL,
  address TEXT,
  city TEXT,
  state TEXT,
  zip_code TEXT,
  country TEXT,
  contact_person TEXT,
  contact_phone TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sorting_records (
  sorting_id INTEGER PRIMARY KEY AUTOINCREMENT,
  collected_item_id INTEGER,
  center_id INTEGER,
  sorted_category TEXT,
  sorted_quantity INTEGER,
  sorted_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (collected_item_id) REFERENCES collected_items(collected_item_id) ON DELETE CASCADE,
  FOREIGN KEY (center_id) REFERENCES distribution_centers(center_id) ON DELETE SET NULL
);

CREATE TABLE delivery_routes (
  route_id INTEGER PRIMARY KEY AUTOINCREMENT,
  distribution_id INTEGER,
  origin_address TEXT,
  destination_address TEXT,
  estimated_delivery_time TEXT,
  route_status TEXT DEFAULT 'planned' CHECK(route_status IN ('planned','in_transit','completed')),
  FOREIGN KEY (distribution_id) REFERENCES distributed_items(distribution_id) ON DELETE CASCADE
);

CREATE TABLE inventory (
  inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
  center_id INTEGER,
  item_name TEXT,
  quantity INTEGER,
  last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (center_id) REFERENCES distribution_centers(center_id) ON DELETE CASCADE
);

CREATE TABLE distributed_items (
  distribution_id INTEGER PRIMARY KEY,
  center_id INTEGER,
  item_name TEXT NOT NULL,
  item_quantity INTEGER NOT NULL,
  distribution_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (center_id) REFERENCES distribution_centers(center_id) ON DELETE SET NULL
);

CREATE TABLE delivery_confirmations (
  confirmation_id INTEGER PRIMARY KEY,
  distribution_id INTEGER,
  received_by TEXT,
  received_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  notes TEXT,
  FOREIGN KEY (distribution_id) REFERENCES distributed_items(distribution_id) ON DELETE CASCADE
);

CREATE TABLE feedback_reviews (
  review_id INTEGER PRIMARY KEY,
  donor_store_id INTEGER,
  npo_id INTEGER,
  rating INTEGER CHECK(rating >= 1 AND rating <= 5),
  comments TEXT,
  review_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (donor_store_id) REFERENCES donor_store_profiles(donor_store_id) ON DELETE SET NULL,
  FOREIGN KEY (npo_id) REFERENCES npo_profiles(npo_id) ON DELETE SET NULL
);

CREATE TABLE admin_logs (
  log_id INTEGER PRIMARY KEY AUTOINCREMENT,
  admin_id INTEGER,
  action_type TEXT,
  target_table TEXT,
  target_id INTEGER,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  notes TEXT,
  FOREIGN KEY (admin_id) REFERENCES users(user_id) ON DELETE SET NULL
);
