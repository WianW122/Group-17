# app.py
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "donation_management.db")

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)


# -----------------------------
# Models
# -----------------------------
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(50), nullable=False)  # donor | npo | admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    donor_profile = db.relationship("DonorProfile", back_populates="user", uselist=False)
    npo_profile = db.relationship("NPOProfile", back_populates="user", uselist=False)


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

    user = db.relationship("User", back_populates="donor_profile")
    donations = db.relationship("DonationRecord", back_populates="donor", cascade="all, delete-orphan")
    pickups = db.relationship("Pickup", back_populates="donor", cascade="all, delete-orphan")


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

    user = db.relationship("User", back_populates="npo_profile")
    feedbacks = db.relationship("FeedbackReview", back_populates="npo", cascade="all, delete-orphan")


class DonationRecord(db.Model):
    __tablename__ = 'donation_records'
    donation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donor_store_id = db.Column(db.Integer, db.ForeignKey('donor_store_profiles.donor_store_id'), nullable=True)
    donation_date = db.Column(db.DateTime, default=datetime.utcnow)
    donation_amount = db.Column(db.Float, nullable=False, default=0.0)
    donation_type = db.Column(db.String(100))  # e.g. "item", "financial", "request"
    notes = db.Column(db.Text)

    donor = db.relationship("DonorProfile", back_populates="donations")
    items = db.relationship("DonationItem", back_populates="donation", cascade="all, delete-orphan")


class DonationItem(db.Model):
    __tablename__ = 'donation_item_details'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donation_id = db.Column(db.Integer, db.ForeignKey('donation_records.donation_id'), nullable=False)
    item_name = db.Column(db.String(200), nullable=False)
    item_description = db.Column(db.Text)
    item_quantity = db.Column(db.Integer, nullable=False, default=1)
    item_value = db.Column(db.Float, default=0.0)

    donation = db.relationship("DonationRecord", back_populates="items")


class Pickup(db.Model):
    __tablename__ = 'pickup_scheduling'
    pickup_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donor_store_id = db.Column(db.Integer, db.ForeignKey('donor_store_profiles.donor_store_id'), nullable=True)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    pickup_address = db.Column(db.Text)
    contact_person = db.Column(db.String(200))
    contact_phone = db.Column(db.String(50))
    status = db.Column(db.String(50), default='Scheduled')  # Scheduled | Completed | Cancelled

    donor = db.relationship("DonorProfile", back_populates="pickups")


class Inventory(db.Model):
    __tablename__ = 'inventory'
    inventory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    center_id = db.Column(db.Integer, db.ForeignKey('distribution_centers.center_id'))
    item_name = db.Column(db.String(200))
    quantity = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    center = db.relationship("DistributionCenter", back_populates="inventory_items")


class DistributedItem(db.Model):
    __tablename__ = 'distributed_items'
    distribution_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    center_id = db.Column(db.Integer, db.ForeignKey('distribution_centers.center_id'), nullable=True)
    item_name = db.Column(db.String(200), nullable=False)
    item_quantity = db.Column(db.Integer, nullable=False, default=0)
    distribution_date = db.Column(db.DateTime, default=datetime.utcnow)

    center = db.relationship("DistributionCenter", back_populates="distributed_items")


class FeedbackReview(db.Model):
    __tablename__ = 'feedback_reviews'
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donor_store_id = db.Column(db.Integer, db.ForeignKey('donor_store_profiles.donor_store_id'), nullable=True)
    npo_id = db.Column(db.Integer, db.ForeignKey('npo_profiles.npo_id'), nullable=True)
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text)
    review_date = db.Column(db.DateTime, default=datetime.utcnow)

    npo = db.relationship("NPOProfile", back_populates="feedbacks")


class DistributionCenter(db.Model):
    __tablename__ = 'distribution_centers'
    center_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    center_name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    contact_person = db.Column(db.String(200))
    contact_phone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    inventory_items = db.relationship("Inventory", back_populates="center", cascade="all, delete-orphan")
    distributed_items = db.relationship("DistributedItem", back_populates="center", cascade="all, delete-orphan")


# -----------------------------
# Helpers
# -----------------------------
def json_error(message, status=400):
    return jsonify({"error": message}), status


# -----------------------------
# Database initialization and seed
# -----------------------------
def init_db(seed=True):
    db.create_all()
    if seed:
        if not User.query.filter_by(email='admin@example.com').first():
            admin = User(
                name='Admin User',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            # create small seed donor + npo so metrics can be tested
            donor_user = User(name='Seed Donor', email='donor@example.com', password_hash=generate_password_hash('donor123'), role='donor')
            npo_user = User(name='Seed NPO', email='npo@example.com', password_hash=generate_password_hash('npo123'), role='npo')
            db.session.add_all([donor_user, npo_user])
            db.session.flush()  # get ids
            donor_profile = DonorProfile(donor_store_id=donor_user.user_id, first_name='Seed', last_name='Donor', email=donor_user.email)
            npo_profile = NPOProfile(npo_id=npo_user.user_id, npo_name='Seed NPO', email=npo_user.email)
            db.session.add_all([donor_profile, npo_profile])
            db.session.commit()


# -----------------------------
# Auth / User endpoints
# -----------------------------
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not (name and email and password and role):
        return json_error("Missing required fields (name, email, password, role)", 400)
    if role not in ('donor', 'npo', 'admin'):
        return json_error("Invalid role. Allowed: donor, npo, admin", 400)
    if User.query.filter_by(email=email).first():
        return json_error("Email already registered", 400)

    user = User(name=name, email=email, password_hash=generate_password_hash(password), role=role)
    db.session.add(user)
    db.session.flush()

    if role == 'donor':
        dp = DonorProfile(donor_store_id=user.user_id, first_name=name.split()[0], last_name=' '.join(name.split()[1:]) or '', email=email)
        db.session.add(dp)
    elif role == 'npo':
        np = NPOProfile(npo_id=user.user_id, npo_name=name, email=email)
        db.session.add(np)
    db.session.commit()
    return jsonify({"message": "Registered", "user_id": user.user_id}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not (email and password):
        return json_error("Missing credentials", 400)
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return json_error("Invalid credentials", 401)
    return jsonify({"message": "OK", "user": {"user_id": user.user_id, "name": user.name, "email": user.email, "role": user.role}}), 200


@app.route('/api/users/<int:uid>', methods=['GET'])
def get_user(uid):
    user = User.query.get(uid)
    if not user:
        return json_error("User not found", 404)
    profile = None
    if user.role == 'donor':
        profile = DonorProfile.query.get(uid)
    elif user.role == 'npo':
        profile = NPOProfile.query.get(uid)
    result = {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "profile": {}
    }
    if profile:
        # convert profile columns to dict (simple)
        for col in profile.__table__.columns:
            result["profile"][col.name] = getattr(profile, col.name)
    return jsonify(result)


# -----------------------------
# Donations + items
# -----------------------------
@app.route('/api/donations', methods=['POST'])
def create_donation():
    """
    Create a donation record. donor_store_id optional (NPO requests).
    JSON: { donor_store_id?, donation_amount?, donation_type?, notes?, items: [{item_name, item_quantity, item_value?, item_description?}] }
    """
    data = request.get_json() or {}
    donor_store_id = data.get('donor_store_id')
    donation_amount = data.get('donation_amount', 0.0)
    donation_type = data.get('donation_type', 'item')
    notes = data.get('notes')
    items = data.get('items', [])

    dr = DonationRecord(donor_store_id=donor_store_id, donation_amount=donation_amount, donation_type=donation_type, notes=notes)
    db.session.add(dr)
    db.session.flush()  # get dr.donation_id

    created_items = []
    for it in items:
        di = DonationItem(
            donation_id=dr.donation_id,
            item_name=it.get('item_name'),
            item_description=it.get('item_description'),
            item_quantity=int(it.get('item_quantity', 0)),
            item_value=float(it.get('item_value', 0.0)) if it.get('item_value') is not None else 0.0
        )
        db.session.add(di)
        created_items.append(di)
    db.session.commit()

    return jsonify({
        "message": "Donation created",
        "donation_id": dr.donation_id,
        "items_created": [ {"item_id": i.item_id, "item_name": i.item_name} for i in created_items ]
    }), 201


@app.route('/api/donations', methods=['GET'])
def list_donations():
    donor_id = request.args.get('donor_store_id', type=int)
    query = DonationRecord.query
    if donor_id:
        query = query.filter_by(donor_store_id=donor_id)
    recs = query.order_by(DonationRecord.donation_date.desc()).all()
    out = []
    for r in recs:
        items = []
        for i in r.items:
            items.append({
                "item_id": i.item_id,
                "item_name": i.item_name,
                "item_quantity": i.item_quantity,
                "item_value": i.item_value,
                "item_description": i.item_description
            })
        out.append({
            "donation_id": r.donation_id,
            "donor_store_id": r.donor_store_id,
            "donation_date": r.donation_date.isoformat(),
            "donation_amount": r.donation_amount,
            "donation_type": r.donation_type,
            "notes": r.notes,
            "items": items
        })
    return jsonify(out)


# small convenience endpoint to add an item to existing donation
@app.route('/api/donations/<int:donation_id>/items', methods=['POST'])
def add_donation_item(donation_id):
    data = request.get_json() or {}
    donation = DonationRecord.query.get(donation_id)
    if not donation:
        return json_error("Donation not found", 404)
    item_name = data.get('item_name')
    item_quantity = int(data.get('item_quantity', 0))
    item_value = float(data.get('item_value', 0.0)) if data.get('item_value') is not None else 0.0
    item_description = data.get('item_description')
    if not item_name:
        return json_error("item_name required", 400)
    di = DonationItem(donation_id=donation_id, item_name=item_name, item_quantity=item_quantity, item_value=item_value, item_description=item_description)
    db.session.add(di)
    db.session.commit()
    return jsonify({"message": "Item added", "item_id": di.item_id}), 201


# -----------------------------
# Pickups
# -----------------------------
@app.route('/api/pickups', methods=['POST'])
def schedule_pickup():
    data = request.get_json() or {}
    donor_store_id = data.get('donor_store_id') or data.get('donor_id')
    scheduled_date = data.get('scheduled_date')
    pickup_address = data.get('pickup_address')
    contact_person = data.get('contact_person')
    contact_phone = data.get('contact_phone')

    if not scheduled_date:
        return json_error("scheduled_date required", 400)

    # parse date
    try:
        scheduled_dt = datetime.fromisoformat(scheduled_date)
    except Exception:
        try:
            scheduled_dt = datetime.strptime(scheduled_date.split("T")[0], "%Y-%m-%d")
        except Exception:
            return json_error("scheduled_date must be ISO format (YYYY-MM-DD or full ISO datetime)", 400)

    p = Pickup(donor_store_id=donor_store_id, scheduled_date=scheduled_dt, pickup_address=pickup_address, contact_person=contact_person, contact_phone=contact_phone, status='Scheduled')
    db.session.add(p)
    db.session.commit()
    return jsonify({"message": "Pickup scheduled", "pickup_id": p.pickup_id}), 201


# GET all pickups (optionally filter by query param donor_store_id)
@app.route('/api/pickups', methods=['GET'])
def get_pickups():
    donor_store_id = request.args.get('donor_store_id', type=int)
    if donor_store_id:
        pickups = Pickup.query.filter_by(donor_store_id=donor_store_id).order_by(Pickup.scheduled_date.desc()).all()
    else:
        pickups = Pickup.query.order_by(Pickup.scheduled_date.desc()).all()
    out = []
    for p in pickups:
        out.append({
            "pickup_id": p.pickup_id,
            "donor_store_id": p.donor_store_id,
            "scheduled_date": p.scheduled_date.isoformat(),
            "pickup_address": p.pickup_address,
            "contact_person": p.contact_person,
            "contact_phone": p.contact_phone,
            "status": p.status
        })
    return jsonify(out)


# Get pickups by donor id (convenience route frontend expects)
@app.route('/api/pickups/<int:donor_id>', methods=['GET'])
def get_pickups_by_donor(donor_id):
    pickups = Pickup.query.filter_by(donor_store_id=donor_id).order_by(Pickup.scheduled_date.desc()).all()
    out = [{
        "pickup_id": p.pickup_id,
        "donor_store_id": p.donor_store_id,
        "scheduled_date": p.scheduled_date.isoformat(),
        "pickup_address": p.pickup_address,
        "contact_person": p.contact_person,
        "contact_phone": p.contact_phone,
        "status": p.status
    } for p in pickups]
    return jsonify(out)


@app.route('/api/pickups/<int:pid>/status', methods=['PUT'])
def update_pickup_status(pid):
    data = request.get_json() or {}
    if "status" not in data:
        return json_error("status required", 400)
    p = Pickup.query.get(pid)
    if not p:
        return json_error("Pickup not found", 404)
    p.status = data["status"]
    db.session.commit()
    return jsonify({"message": "Updated", "pickup_id": pid, "status": p.status})


@app.route('/api/pickups/<int:pid>', methods=['DELETE'])
def delete_pickup(pid):
    p = Pickup.query.get(pid)
    if not p:
        return json_error("Pickup not found", 404)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "Pickup deleted", "pickup_id": pid})


# -----------------------------
# Inventory / Distribution / Deliveries
# -----------------------------
@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    rows = Inventory.query.all()
    return jsonify([{"inventory_id": r.inventory_id, "center_id": r.center_id, "item_name": r.item_name, "quantity": r.quantity, "last_updated": r.last_updated.isoformat() if r.last_updated else None} for r in rows])


@app.route('/api/inventory', methods=['POST'])
def create_inventory():
    data = request.get_json() or {}
    center_id = data.get("center_id")
    item_name = data.get("item_name")
    quantity = data.get("quantity", 0)
    if not (center_id and item_name):
        return json_error("center_id and item_name required", 400)
    inv = Inventory(center_id=center_id, item_name=item_name, quantity=int(quantity))
    db.session.add(inv)
    db.session.commit()
    return jsonify({"message": "Inventory created", "inventory_id": inv.inventory_id}), 201


@app.route('/api/distributed_items', methods=['POST'])
def create_distributed_item():
    data = request.get_json() or {}
    center_id = data.get("center_id")
    item_name = data.get("item_name")
    item_quantity = int(data.get("item_quantity", 0))
    if not (center_id and item_name):
        return json_error("center_id and item_name required", 400)
    di = DistributedItem(center_id=center_id, item_name=item_name, item_quantity=item_quantity)
    db.session.add(di)
    db.session.commit()
    return jsonify({"message": "Distributed item created", "distribution_id": di.distribution_id}), 201


@app.route('/api/distributed_items', methods=['GET'])
def list_distributed_items():
    rows = DistributedItem.query.order_by(DistributedItem.distribution_date.desc()).all()
    return jsonify([{"distribution_id": r.distribution_id, "center_id": r.center_id, "item_name": r.item_name, "item_quantity": r.item_quantity, "distribution_date": r.distribution_date.isoformat()} for r in rows])


@app.route('/api/deliveries/<int:npo_id>', methods=['GET'])
def get_deliveries(npo_id):
    """
    Return distributed items as 'deliveries' for the NPO dashboard.
    Since schema doesn't tie distributed_items to npo directly, this endpoint returns distributed items.
    """
    rows = DistributedItem.query.order_by(DistributedItem.distribution_date.desc()).all()
    return jsonify([{"delivery_id": r.distribution_id, "item_name": r.item_name, "quantity": r.item_quantity, "distribution_date": r.distribution_date.isoformat()} for r in rows])


# -----------------------------
# Feedback
# -----------------------------
@app.route('/api/feedback', methods=['POST'])
def create_feedback():
    data = request.get_json() or {}
    donor_store_id = data.get('donor_store_id')
    npo_id = data.get('npo_id')
    rating = data.get('rating')
    comments = data.get('comments', '')
    if npo_id is None or rating is None:
        return json_error("npo_id and rating required", 400)
    try:
        rating_int = int(rating)
    except Exception:
        return json_error("rating must be integer 1-5", 400)
    if rating_int < 1 or rating_int > 5:
        return json_error("rating must be between 1 and 5", 400)
    fr = FeedbackReview(donor_store_id=donor_store_id, npo_id=npo_id, rating=rating_int, comments=comments)
    db.session.add(fr)
    db.session.commit()
    return jsonify({"message": "Feedback submitted", "review_id": fr.review_id}), 201


@app.route('/api/feedback', methods=['GET'])
def get_feedback():
    donor_id = request.args.get("donor_store_id", type=int)
    npo_id = request.args.get("npo_id", type=int)
    q = FeedbackReview.query
    if donor_id:
        q = q.filter_by(donor_store_id=donor_id)
    if npo_id:
        q = q.filter_by(npo_id=npo_id)
    rows = q.order_by(FeedbackReview.review_date.desc()).all()
    return jsonify([{"review_id": r.review_id, "donor_store_id": r.donor_store_id, "npo_id": r.npo_id, "rating": r.rating, "comments": r.comments, "review_date": r.review_date.isoformat()} for r in rows])


# -----------------------------
# Metrics endpoints
# -----------------------------
@app.route('/api/metrics/npo/<int:npo_id>', methods=['GET'])
def npo_metrics(npo_id):
    # total donated items (exclude 'request' type)
    total_items = db.session.query(db.func.coalesce(db.func.sum(DonationItem.item_quantity), 0)) \
        .join(DonationRecord, DonationRecord.donation_id == DonationItem.donation_id) \
        .filter(DonationRecord.donation_type != 'request').scalar() or 0

    total_pickups = Pickup.query.count() or 0

    feedbacks = FeedbackReview.query.filter_by(npo_id=npo_id).all()
    avg_rating = None
    if feedbacks:
        ratings = [f.rating for f in feedbacks if f.rating is not None]
        if ratings:
            avg_rating = sum(ratings) / len(ratings)

    return jsonify({
        "npo_id": npo_id,
        "total_donations": int(total_items),
        "total_pickups": int(total_pickups),
        "average_feedback_rating": avg_rating
    })


@app.route('/api/donor/<int:donor_id>/metrics', methods=['GET'])
def get_donor_metrics(donor_id):
    total_donations = DonationRecord.query.filter_by(donor_store_id=donor_id).count()
    total_items = db.session.query(db.func.coalesce(db.func.sum(DonationItem.item_quantity), 0)) \
        .join(DonationRecord, DonationRecord.donation_id == DonationItem.donation_id) \
        .filter(DonationRecord.donor_store_id == donor_id).scalar() or 0
    total_value = db.session.query(db.func.coalesce(db.func.sum(DonationItem.item_value * DonationItem.item_quantity), 0.0)) \
        .join(DonationRecord, DonationRecord.donation_id == DonationItem.donation_id) \
        .filter(DonationRecord.donor_store_id == donor_id).scalar() or 0.0

    recent_donations = DonationRecord.query.filter_by(donor_store_id=donor_id).order_by(DonationRecord.donation_date.desc()).limit(5).all()
    recent_list = [{"donation_id": d.donation_id, "amount": d.donation_amount, "type": d.donation_type, "date": d.donation_date.isoformat()} for d in recent_donations]

    return jsonify({
        "total_donations": total_donations,
        "total_items": int(total_items),
        "total_value": float(total_value),
        "recent_donations": recent_list
    })


# -----------------------------
# Distribution centers
# -----------------------------
@app.route('/api/centers', methods=['POST'])
def create_center():
    data = request.get_json() or {}
    name = data.get("center_name")
    if not name:
        return json_error("center_name required", 400)
    c = DistributionCenter(center_name=name, address=data.get("address"), city=data.get("city"), state=data.get("state"), zip_code=data.get("zip_code"), country=data.get("country"), contact_person=data.get("contact_person"), contact_phone=data.get("contact_phone"))
    db.session.add(c)
    db.session.commit()
    return jsonify({"message": "Center created", "center_id": c.center_id}), 201


@app.route('/api/centers', methods=['GET'])
def get_centers():
    rows = DistributionCenter.query.order_by(DistributionCenter.created_at.desc()).all()
    return jsonify([{"center_id": r.center_id, "center_name": r.center_name, "address": r.address, "city": r.city, "state": r.state, "zip_code": r.zip_code, "country": r.country} for r in rows])


# -----------------------------
# Simple pages serving (frontend)
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/donor-dashboard")
def donor_dashboard_page():
    return render_template("donor-dashboard.html")


@app.route("/npo-dashboard")
def npo_dashboard_page():
    return render_template("npo-dashboard.html")


@app.route("/schedule-pickup")
def schedule_pickup_page():
    return render_template("schedule-pickup.html")


# -----------------------------
# Run
# -----------------------------
if __name__ == '__main__':
    with app.app_context():
        init_db(seed=True)
    app.run(debug=True)
