from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "donation_management.db")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

# Models 

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DonorProfile(db.Model):
    __tablename__ = 'donor_store_profiles'
    donor_store_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class NPOProfile(db.Model):
    __tablename__ = 'npo_profiles'
    npo_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    npo_name = db.Column(db.String(200), nullable=False)
    contact_person = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DonationRecord(db.Model):
    __tablename__ = 'donation_records'
    donation_id = db.Column(db.Integer, primary_key=True)
    donor_store_id = db.Column(db.Integer, db.ForeignKey('donor_store_profiles.donor_store_id'))
    donation_date = db.Column(db.DateTime, default=datetime.utcnow)
    donation_amount = db.Column(db.Float, nullable=False)
    donation_type = db.Column(db.String(100))
    notes = db.Column(db.Text)

class DonationItem(db.Model):
    __tablename__ = 'donation_item_details'
    item_id = db.Column(db.Integer, primary_key=True)
    donation_id = db.Column(db.Integer, db.ForeignKey('donation_records.donation_id'))
    item_name = db.Column(db.String(200), nullable=False)
    item_description = db.Column(db.Text)
    item_quantity = db.Column(db.Integer, nullable=False)
    item_value = db.Column(db.Float)

class Notification(db.Model):
    __tablename__ = 'notifications'
    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_role = db.Column(db.String(50))
    recipient_role = db.Column(db.String(50))
    message = db.Column(db.Text)
    related_item_id = db.Column(db.Integer)
    notification_type = db.Column(db.String(50))
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

class Pickup(db.Model):
    __tablename__ = 'pickup_scheduling'
    pickup_id = db.Column(db.Integer, primary_key=True)
    donor_store_id = db.Column(db.Integer, db.ForeignKey('donor_store_profiles.donor_store_id'))
    scheduled_date = db.Column(db.DateTime, nullable=False)
    pickup_address = db.Column(db.Text)
    contact_person = db.Column(db.String(200))
    contact_phone = db.Column(db.String(50))
    status = db.Column(db.String(50), default='Scheduled')

class CollectedItem(db.Model):
    __tablename__ = 'collected_items'
    collected_item_id = db.Column(db.Integer, primary_key=True)
    pickup_id = db.Column(db.Integer, db.ForeignKey('pickup_scheduling.pickup_id'))
    item_name = db.Column(db.String(200), nullable=False)
    item_quantity = db.Column(db.Integer, nullable=False)
    item_condition = db.Column(db.String(100))

class DistributionCenter(db.Model):
    __tablename__ = 'distribution_centers'
    center_id = db.Column(db.Integer, primary_key=True)
    center_name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    contact_person = db.Column(db.String(200))
    contact_phone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SortingRecord(db.Model):
    __tablename__ = 'sorting_records'
    sorting_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    collected_item_id = db.Column(db.Integer, db.ForeignKey('collected_items.collected_item_id'))
    center_id = db.Column(db.Integer, db.ForeignKey('distribution_centers.center_id'))
    sorted_category = db.Column(db.String(200))
    sorted_quantity = db.Column(db.Integer)
    sorted_date = db.Column(db.DateTime, default=datetime.utcnow)

class DeliveryRoute(db.Model):
    __tablename__ = 'delivery_routes'
    route_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    distribution_id = db.Column(db.Integer, db.ForeignKey('distributed_items.distribution_id'))
    origin_address = db.Column(db.Text)
    destination_address = db.Column(db.Text)
    estimated_delivery_time = db.Column(db.String(50))
    route_status = db.Column(db.String(50), default='planned')

class Inventory(db.Model):
    __tablename__ = 'inventory'
    inventory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    center_id = db.Column(db.Integer, db.ForeignKey('distribution_centers.center_id'))
    item_name = db.Column(db.String(200))
    quantity = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class DistributedItem(db.Model):
    __tablename__ = 'distributed_items'
    distribution_id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, db.ForeignKey('distribution_centers.center_id'))
    item_name = db.Column(db.String(200), nullable=False)
    item_quantity = db.Column(db.Integer, nullable=False)
    distribution_date = db.Column(db.DateTime, default=datetime.utcnow)

class DeliveryConfirmation(db.Model):
    __tablename__ = 'delivery_confirmations'
    confirmation_id = db.Column(db.Integer, primary_key=True)
    distribution_id = db.Column(db.Integer, db.ForeignKey('distributed_items.distribution_id'))
    received_by = db.Column(db.String(200))
    received_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

class FeedbackReview(db.Model):
    __tablename__ = 'feedback_reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    donor_store_id = db.Column(db.Integer, db.ForeignKey('donor_store_profiles.donor_store_id'))
    npo_id = db.Column(db.Integer, db.ForeignKey('npo_profiles.npo_id'))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text)
    review_date = db.Column(db.DateTime, default=datetime.utcnow)

class AdminLog(db.Model):
    __tablename__ = 'admin_logs'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    action_type = db.Column(db.String(200))
    target_table = db.Column(db.String(200))
    target_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

# Utility: create and seed

def init_db(seed=True):
    db.create_all()
    if seed:
        if not User.query.filter_by(email='admin@example.com').first():
            u1 = User(name='Admin User', email='admin@example.com', password_hash=generate_password_hash('admin123'), role='donor')
            u2 = User(name='Alice Donor', email='alice@example.com', password_hash=generate_password_hash('alice123'), role='donor')
            u3 = User(name='Bob Donor', email='bob@example.com', password_hash=generate_password_hash('bob123'), role='donor')
            u4 = User(name='Hope Foundation', email='hope@example.com', password_hash=generate_password_hash('hope123'), role='npo')
            u5 = User(name='Care Connect', email='care@example.com', password_hash=generate_password_hash('care123'), role='npo')
            db.session.add_all([u1,u2,u3,u4,u5])
            db.session.commit()
            # donor profiles
            d2 = DonorProfile(donor_store_id=2, first_name='Alice', last_name='Smith', email='alice@example.com', phone_number='0123456789', address='123 Elm St', city='Pretoria', state='Gauteng', zip_code='0001', country='South Africa', date_of_birth=datetime(1985,6,15))
            d3 = DonorProfile(donor_store_id=3, first_name='Bob', last_name='Moyo', email='bob@example.com', phone_number='0987654321', address='456 Oak St', city='Pretoria', state='Gauteng', zip_code='0002', country='South Africa', date_of_birth=datetime(1990,9,20))
            db.session.add_all([d2,d3])
            # npo profiles
            n4 = NPOProfile(npo_id=4, npo_name='Hope Foundation', contact_person='Lindiwe Khumalo', email='hope@example.com', phone_number='0112233445', address='789 Charity Rd', city='Pretoria', state='Gauteng', zip_code='0003', country='South Africa')
            n5 = NPOProfile(npo_id=5, npo_name='Care Connect', contact_person='Thabo Ncube', email='care@example.com', phone_number='0119988776', address='321 Help Ave', city='Pretoria', state='Gauteng', zip_code='0004', country='South Africa')
            db.session.add_all([n4,n5])
            # donations
            dr1 = DonationRecord(donation_id=1, donor_store_id=2, donation_amount=500.00, donation_type='monetary', notes='Monthly donation')
            dr2 = DonationRecord(donation_id=2, donor_store_id=3, donation_amount=0.00, donation_type='in-kind', notes='Winter supplies')
            dr3 = DonationRecord(donation_id=3, donor_store_id=2, donation_amount=250.00, donation_type='monetary', notes='Emergency relief')
            db.session.add_all([dr1,dr2,dr3])
            # items
            it1 = DonationItem(item_id=1, donation_id=2, item_name='Blanket', item_description='Warm fleece blanket', item_quantity=10, item_value=50.00)
            it2 = DonationItem(item_id=2, donation_id=2, item_name='Jacket', item_description='Winter jacket, assorted sizes', item_quantity=5, item_value=75.00)
            db.session.add_all([it1,it2])
            # pickup + collected
            p1 = Pickup(pickup_id=1, donor_store_id=3, scheduled_date=datetime(2025,10,28,10,0,0), pickup_address='456 Oak St, Pretoria', contact_person='Bob Moyo', contact_phone='0987654321', status='Scheduled')
            db.session.add(p1)
            c1 = CollectedItem(collected_item_id=1, pickup_id=1, item_name='Blanket', item_quantity=10, item_condition='Good')
            c2 = CollectedItem(collected_item_id=2, pickup_id=1, item_name='Jacket', item_quantity=5, item_condition='Excellent')
            db.session.add_all([c1,c2])
            # distribution center
            dc = DistributionCenter(center_id=1, center_name='Pretoria Distribution Hub', address='1 Hub Way', city='Pretoria', state='Gauteng', zip_code='0010', country='South Africa', contact_person='Sibongile Dlamini', contact_phone='0113344556')
            db.session.add(dc)
            # sorting, inventory, distributed items, confirmations
            sr1 = SortingRecord(sorting_id=1, collected_item_id=1, center_id=1, sorted_category='Blankets', sorted_quantity=10)
            sr2 = SortingRecord(sorting_id=2, collected_item_id=2, center_id=1, sorted_category='Clothing', sorted_quantity=5)
            db.session.add_all([sr1,sr2])
            inv1 = Inventory(inventory_id=1, center_id=1, item_name='Blanket', quantity=10)
            inv2 = Inventory(inventory_id=2, center_id=1, item_name='Jacket', quantity=5)
            db.session.add_all([inv1,inv2])
            di1 = DistributedItem(distribution_id=1, center_id=1, item_name='Blanket', item_quantity=5)
            di2 = DistributedItem(distribution_id=2, center_id=1, item_name='Jacket', item_quantity=2)
            db.session.add_all([di1,di2])
            dc1 = DeliveryConfirmation(confirmation_id=1, distribution_id=1, received_by='Hope Foundation', notes='Received in good condition')
            dc2 = DeliveryConfirmation(confirmation_id=2, distribution_id=2, received_by='Care Connect', notes='Delivered successfully')
            db.session.add_all([dc1,dc2])
            fr1 = FeedbackReview(review_id=1, donor_store_id=2, npo_id=4, rating=5, comments='Great communication and impact')
            fr2 = FeedbackReview(review_id=2, donor_store_id=3, npo_id=5, rating=4, comments='Smooth pickup and delivery')
            db.session.add_all([fr1,fr2])
            notif1 = Notification(notification_id=1, sender_role='system', recipient_role='npo', message='New donation ready for pickup', related_item_id=1, notification_type='donation_ready')
            notif2 = Notification(notification_id=2, sender_role='admin', recipient_role='npo', message='Stock available at distribution center', related_item_id=2, notification_type='stock_available')
            db.session.add_all([notif1,notif2])
            log1 = AdminLog(log_id=1, admin_id=1, action_type='INSERT', target_table='donation_records', target_id=3, notes='Emergency donation logged')
            log2 = AdminLog(log_id=2, admin_id=1, action_type='UPDATE', target_table='inventory', target_id=1, notes='Inventory adjusted after sorting')
            db.session.add_all([log1,log2])
            db.session.commit()

# REST API endpoints

# 1) Register 
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json or {}
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')  # expected 'donor' or 'npo'
    if not (name and email and password and role):
        return jsonify({"error": "Missing required fields"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400
    user = User(name=name, email=email, password_hash=generate_password_hash(password), role=role)
    db.session.add(user)
    db.session.commit()
    # Create profile stub
    if role == 'donor':
        profi = DonorProfile(donor_store_id=user.user_id, first_name=name.split()[0], last_name=' '.join(name.split()[1:]) or '', email=email)
        db.session.add(profi)
    elif role == 'npo':
        profi = NPOProfile(npo_id=user.user_id, npo_name=name, email=email)
        db.session.add(profi)
    db.session.commit()
    return jsonify({"message": "Registered", "user_id": user.user_id}), 201

# 2) Login 
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')
    if not (email and password):
        return jsonify({"error": "Missing credentials"}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401
    return jsonify({"message": "OK", "user": {"user_id": user.user_id, "name": user.name, "email": user.email, "role": user.role}})

# 3) Create donation 
@app.route('/api/donations', methods=['POST'])
def create_donation():
    data = request.json or {}
    donor_store_id = data.get('donor_store_id')
    donation_amount = data.get('donation_amount', 0.0)
    donation_type = data.get('donation_type')
    notes = data.get('notes')
    items = data.get('items', []) 
    if not donor_store_id:
        return jsonify({"error": "donor_store_id required"}), 400
    # compute new donation_id
    max_id = db.session.query(db.func.max(DonationRecord.donation_id)).scalar() or 0
    dr = DonationRecord(donation_id=max_id+1, donor_store_id=donor_store_id, donation_amount=donation_amount, donation_type=donation_type, notes=notes)
    db.session.add(dr)
    db.session.commit()
    for it in items:
        max_item = db.session.query(db.func.max(DonationItem.item_id)).scalar() or 0
        di = DonationItem(item_id=max_item+1, donation_id=dr.donation_id, item_name=it.get('item_name'), item_description=it.get('item_description'), item_quantity=it.get('item_quantity',0), item_value=it.get('item_value'))
        db.session.add(di)
    db.session.commit()
    return jsonify({"message":"Donation created","donation_id": dr.donation_id}), 201

# 4) Get donations 
@app.route('/api/donations', methods=['GET'])
def list_donations():
    donor_id = request.args.get('donor_store_id')
    if donor_id:
        recs = DonationRecord.query.filter_by(donor_store_id=donor_id).all()
    else:
        recs = DonationRecord.query.all()
    out = []
    for r in recs:
        items = DonationItem.query.filter_by(donation_id=r.donation_id).all()
        out.append({
            "donation_id": r.donation_id,
            "donor_store_id": r.donor_store_id,
            "donation_amount": r.donation_amount,
            "donation_type": r.donation_type,
            "notes": r.notes,
            "items": [{"item_id":i.item_id,"item_name":i.item_name,"qty":i.item_quantity,"value":i.item_value} for i in items]
        })
    return jsonify(out)

# 5) Schedule pickup
@app.route('/api/pickups', methods=['POST'])
def schedule_pickup():
    data = request.json or {}
    donor_store_id = data.get('donor_store_id')
    scheduled_date = data.get('scheduled_date')  # ISO string
    pickup_address = data.get('pickup_address')
    contact_person = data.get('contact_person')
    contact_phone = data.get('contact_phone')
    if not (donor_store_id and scheduled_date):
        return jsonify({"error":"donor_store_id and scheduled_date required"}), 400
    max_id = db.session.query(db.func.max(Pickup.pickup_id)).scalar() or 0
    p = Pickup(pickup_id=max_id+1, donor_store_id=donor_store_id, scheduled_date=datetime.fromisoformat(scheduled_date), pickup_address=pickup_address, contact_person=contact_person, contact_phone=contact_phone, status='Scheduled')
    db.session.add(p)
    db.session.commit()
    return jsonify({"message":"Pickup scheduled","pickup_id":p.pickup_id}), 201

# 6) Update pickup status
@app.route('/api/pickups/<int:pid>/status', methods=['PUT'])
def update_pickup_status(pid):
    data = request.json or {}
    status = data.get('status')
    if not status:
        return jsonify({"error":"status required"}), 400
    p = Pickup.query.get(pid)
    if not p:
        return jsonify({"error":"pickup not found"}), 404
    p.status = status
    db.session.commit()
    return jsonify({"message":"Updated","pickup_id":pid,"status":status})

# 7) KPIs endpoint 
@app.route('/api/kpis', methods=['GET'])
def kpis():
    total_donations = db.session.query(db.func.count(DonationRecord.donation_id)).scalar() or 0
    total_monetary = db.session.query(db.func.sum(DonationRecord.donation_amount)).scalar() or 0.0
    total_items = db.session.query(db.func.sum(DonationItem.item_quantity)).scalar() or 0
    pickups_scheduled = db.session.query(db.func.count(Pickup.pickup_id)).filter(Pickup.status=='Scheduled').scalar() or 0
    inventory_count = db.session.query(db.func.sum(Inventory.quantity)).scalar() or 0
    return jsonify({
        "total_donations": int(total_donations),
        "total_monetary": float(total_monetary),
        "total_items_in_kind": int(total_items) if total_items is not None else 0,
        "pickups_scheduled": int(pickups_scheduled),
        "inventory_total_units": int(inventory_count) if inventory_count is not None else 0
    })

# 8) basic read endpoints for inventory / distribution centers
@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    rows = Inventory.query.all()
    return jsonify([{"inventory_id":r.inventory_id,"center_id":r.center_id,"item_name":r.item_name,"quantity":r.quantity} for r in rows])

@app.route('/api/centers', methods=['GET'])
def get_centers():
    rows = DistributionCenter.query.all()
    return jsonify([{"center_id":r.center_id,"center_name":r.center_name,"city":r.city} for r in rows])

# Run / init

if __name__ == '__main__':
    init_db(seed=True)
    print("DB initialised (donation_management.db). Run flask with 'python app.py' or 'flask run' after setting FLASK_APP=app.py")
    app.run(debug=True, host='0.0.0.0', port=5000)
