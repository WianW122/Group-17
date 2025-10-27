# Play It Forward – Supply Chain App

A web platform connecting donor stores and nonprofits to manage sports equipment donations.

## Features
- Log donations
- Schedule pickups
- Track deliveries
- Submit feedback

## Setup
1. Clone the repo
2. Run `npm install`
3. Start the server with `npm start`

## License
MIT

## ERD diagram
![ERD diagram](BFB_Project/Images/ERD.jpg)

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


## File Structure

```
├── index.html              # Main dashboard
├── login.html              # Vendor login page
├── register.html           # Vendor registration page
├── schedule-pickup.html    # Schedule pickup for donated items
├── donation.sql            # Database schema and sample data
├── donation_management.db  # SQLite database (created after running setup)
└── readme.md               # This file

## Usage

1. Initialize the database using the SQLite command line method above
2. Open `index.html` in your web browser
3. Navigate through the different pages to manage your inventory

## Technologies Used

- **HTML5**: Structure and forms
- **Bootstrap 5.3.8**: UI framework and styling
- **Bootstrap Icons**: Icon set
- **SQLite**: Database for data persistence

## Browser Compatibility

The application works with all modern browsers that support HTML5 and CSS3, including:

Chrome 90+
Firefox 88+
Safari 14+
Edge 90+
Note: This is a static HTML application. For production use, you would need to add backend functionality for database connectivity and form processing.

