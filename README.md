# Play It Forward

A smart supply chain platform connecting donors, retailers, and nonprofits across South Africa.  
The platform enables the distribution of donated sports equipment to underprivileged communities by connecting donors with non-profit organizations (NPOs). It streamlines donation logistics—capturing donations, scheduling pickups, tracking deliveries, and enabling feedback—to ensure efficiency, transparency, and accountability.

## Group Members
- Wian Wentzel: u23552035
- Martinus van der Merwe: u23524210
- Eunice Scherman: u23524279
- Judith Schnackenberg: u22717022

---

## Features

### **User Management**
- Register and login as Donor or NPO.
- Dashboard access restricted to authenticated users.

### **Donor Dashboard**
- Log and manage donations.
- Track scheduled pickups.
- Track delivery progress.
- Submit feedback on NPO interactions.
- **Metrics:** total donations, total pickups, average feedback rating.

### **NPO Dashboard**
- Request equipment from donors.
- Track received donations and deliveries.
- Submit feedback on donations.
- **Metrics:** total donations received, number of pickups, average feedback rating.

### **Pickup Scheduling**
- Donors can schedule pickups.
- Track pickup status (Scheduled, Completed, etc.)

### **Inventory & Distribution Centers**
- Manage items stored in distribution centers.
- Track sorted items and distributed items.

### **Feedback System**
- Donors and NPOs can leave ratings and comments.

### **Authentication**
- Secure login using hashed passwords.
- Session-based access control.
- Sign-out functionality.

---

## Technology Stack

**Backend:**  
- Python, Flask  
- Flask-SQLAlchemy  
- SQLite  
- Flask-CORS  
- Werkzeug (Password hashing)

**Frontend:**  
- HTML  
- CSS  
- JavaScript  
- Bootstrap 5  

---

## Setup Instructions

### **1. Clone the Repository**
```bash
git clone https://github.com/WianW122/Group-17
cd Group-17
```
### 2. Create a Virtual Environment and Install Dependencies
```bash
python -m venv venv
```
#### Activate the environment:
Windows:
```bash
venv\Scripts\activate
```
Mac/Linux:
```bash
source venv/bin/activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the Flask Application
```bash
python app.py
```

### 4. Open the Application
Visit:
http://127.0.0.1:5000

### 5. Use the Application
- Register as a Donor or NPO.
- Explore dashboards, submit donations/requests.
- Track deliveries and provide feedback.
- API Endpoints (Summary)
- Function	Endpoint
- Register user	/api/register
- Login user	/api/login
- Manage users	/api/users/<id>
- Donations CRUD	/api/donations
- Pickup scheduling	/api/pickups
- Inventory management	/api/inventory
- Feedback reviews	/api/feedback
- Distribution centers	/api/centers
- NPO metrics	/api/metrics/npo/<id>
- Deliveries for NPO	/api/deliveries/<id>
## Database Overview
The SQLite database supports the end-to-end supply chain:

### Core Tables
- users – donor and NPO accounts
- npo_profiles – NPO information
- donor_store_profiles – donor details
- donation_records – all past donations
- donation_item_detail – detailed item data per donation
- pickup_scheduling – logistics and pickup details
- collected_items – items collected from donors
- inventory – items stored at distribution centers
- distribution_centres – warehouse locations
- sorting_records – category sorting details
- distributed_items – items sent to communities
- delivery_confirmation – proof of delivery
- feedback_reviews – ratings and comments
- notifications – communication logs
- admin_logs – admin activity tracking

### Sample Data Included
- 5 user accounts
- 2 NPO profiles
- 3 donation records
- 2 collected item records
- 2 inventory entries
- Multiple feedback, pickup, and distribution records

## File Structure 
```bash

├─ aplay-it-forward/
├─.venv
├─sqlite
├─ app.py
├─ donation_management.db
├─ templates/
│   ├─ index.html
│   ├─ login.html
│   ├─ register.html
│   ├─ donor-dashboard.html
│   └─ npo-dashboard.html
│   └─ schedule-pickup.html
├─ static/
│   ├─ css/
│   └─ js/
├─ requirements.txt
└─ README.md

```
 ⁠
## Notes
- A default admin user is created on first run:
- Email: admin@example.com
- Password: admin123
- Ensure your virtual environment is activated before running the backend.
- Use multiple browsers or private windows to simulate Donor/NPO interactions.

## The application works with all modern browsers that support HTML5 and CSS3, including:

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
   
## Database Schema

![ERD diagram](https://github.com/user-attachments/assets/2b47a592-9819-4e43-b241-047e84bb3a18)

### Entity Relationship Diagram (ERD)

The database includes the following tables:
## Tables
1. users: Client information when logging on.
2. admin_logs: Administrator information.
3. npo_profiles: Information regarding NPO's.
4. feedback_reviews: Client ratings and feedback.
5. donor_store_profiles: Information regarding donors.
6. donation_item_detial: Information regarding donated items.
7. donation_records: Previouse donations made.
8. pickup_scheduling: Logistics information regarding pickup.
9. collected_items: Items collected from stores.
10. inventory: Items stored in inventory.
11. distribution_centres: Information regarding distribution centres.
12. sorting_records: Category item is sorted in. 
13. delivery_routes: Information regarding transport routes.
14. distributed_items: Information regarding delivered items. 
15. delivery_confirmation: Confirming completed delivery.
16. notifications: Client communication.

## Sample Data
The database includes sample data for testing:

1. Five different users with unique:
    user_id, name, email, password, and role.
2. Two NPO profiles with details such as:
    npo_id, npo_name, contact_person, email, phone_number, address, city, state, zip_code, and country.
3. Three donation records containing:
    donation_id, donor_store_id, donation_amount, donation_type, and notes.
4. Two donation item details specifying:
    item_id, donation_id, item_name, item_description, item_quantity, and item_value.
5. One pickup scheduling record with:
    pickup_id, donor_store_id, scheduled_date, pickup_address, contact_person, and contact_phone.
6. Two collected items including:
    collected_item_id, pickup_id, item_name, item_quantity, and item_condition.
7. One distribution center defined by:
    center_id, center_name, address, city, state, zip_code, country, contact_person, and contact_phone.
8. Two sorting records showing:
    sorting_id, collected_item_id, center_id, sorted_category, and sorted_quantity.
9. Two inventory entries with:
    inventory_id, center_id, item_name, and quantity.
10. Two distributed items tracking:
    distribution_id, center_id, item_name, and item_quantity.
11. Two delivery confirmations including:
    confirmation_id, distribution_id, received_by, and notes.
12. Two feedback reviews containing:
    review_id, donor_store_id, npo_id, rating, and comments.
13. Two notifications defined by:
    notification_id, sender_role, recipient_role, message, related_item_id, and notification_type.
14. Two admin logs with:
    log_id, admin_id, action_type, target_table, target_id, and notes.

