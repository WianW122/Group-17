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

class Pickup(db.Model):
    __tablename__ = 'pickup_scheduling'
    pickup_id = db.Column(db.Integer, primary_key=True)
    donor_store_id = db.Column(db.Integer, db.ForeignKey('donor_store_profiles.donor_store_id'))
    scheduled_date = db.Column(db.DateTime, nullable=False)
    pickup_address = db.Column(db.Text)
    contact_person = db.Column(db.String(200))
    contact_phone = db.Column(db.String(50))
    status = db.Column(db.String(50), default='Scheduled')

class Inventory(db.Model):
    __tablename__ = 'inventory'
    inventory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    center_id = db.Column(db.Integer, db.ForeignKey('distribution_centers.center_id'))
    item_name = db.Column(db.String(200))
    quantity = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class FeedbackReview(db.Model):
    __tablename__ = 'feedback_reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    donor_store_id = db.Column(db.Integer, db.ForeignKey('donor_store_profiles.donor_store_id'))
    npo_id = db.Column(db.Integer, db.ForeignKey('npo_profiles.npo_id'))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text)
    review_date = db.Column(db.DateTime, default=datetime.utcnow)

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

# -----------------------------
# Database initialization
# -----------------------------
def init_db(seed=True):
    db.create_all()
    if seed:
        if not User.query.filter_by(email='admin@example.com').first():
            u1 = User(name='Admin User', email='admin@example.com', password_hash=generate_password_hash('admin123'), role='donor')
            db.session.add(u1)
            db.session.commit()

# -----------------------------
# User CRUD
# -----------------------------
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json or {}
    name, email, password, role = data.get('name'), data.get('email'), data.get('password'), data.get('role')
    if not (name and email and password and role):
        return jsonify({"error": "Missing required fields"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400
    user = User(name=name, email=email, password_hash=generate_password_hash(password), role=role)
    db.session.add(user)
    db.session.commit()
    # profile stub
    if role == 'donor':
        profi = DonorProfile(donor_store_id=user.user_id, first_name=name.split()[0], last_name=' '.join(name.split()[1:]) or '', email=email)
        db.session.add(profi)
    elif role == 'npo':
        profi = NPOProfile(npo_id=user.user_id, npo_name=name, email=email)
        db.session.add(profi)
    db.session.commit()
    return jsonify({"message":"Registered","user_id":user.user_id}),201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json or {}
    email, password = data.get('email'), data.get('password')
    if not (email and password):
        return jsonify({"error":"Missing credentials"}),400
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error":"Invalid credentials"}),401
    return jsonify({"message":"OK","user":{"user_id":user.user_id,"name":user.name,"email":user.email,"role":user.role}})

@app.route('/api/users/<int:uid>', methods=['GET'])
def get_user(uid):
    user = User.query.get(uid)
    if not user:
        return jsonify({"error":"User not found"}),404
    profile = None
    if user.role == 'donor': profile = DonorProfile.query.get(uid)
    elif user.role == 'npo': profile = NPOProfile.query.get(uid)
    return jsonify({"user_id":user.user_id,"name":user.name,"email":user.email,"role":user.role,
                    "profile": {c.name:getattr(profile,c.name) for c in profile.__table__.columns} if profile else {}})

@app.route('/api/users/<int:uid>', methods=['PUT'])
def update_user(uid):
    user = User.query.get(uid)
    if not user: return jsonify({"error":"User not found"}),404
    data = request.json or {}
    if "name" in data: user.name = data["name"]
    if "email" in data: user.email = data["email"]
    if "password" in data: user.password_hash = generate_password_hash(data["password"])
    db.session.commit()
    return jsonify({"message":"User updated","user_id":uid})

@app.route('/api/users/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    user = User.query.get(uid)
    if not user: return jsonify({"error":"User not found"}),404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message":"User deleted","user_id":uid})

# -----------------------------
# Donation CRUD
# -----------------------------
@app.route('/api/donations', methods=['POST'])
def create_donation():
    data = request.json or {}
    donor_store_id, donation_amount, donation_type, notes, items = data.get('donor_store_id'), data.get('donation_amount',0.0), data.get('donation_type'), data.get('notes'), data.get('items',[])
    if not donor_store_id: return jsonify({"error":"donor_store_id required"}),400
    max_id = db.session.query(db.func.max(DonationRecord.donation_id)).scalar() or 0
    dr = DonationRecord(donation_id=max_id+1, donor_store_id=donor_store_id, donation_amount=donation_amount, donation_type=donation_type, notes=notes)
    db.session.add(dr)
    db.session.commit()
    for it in items:
        max_item = db.session.query(db.func.max(DonationItem.item_id)).scalar() or 0
        di = DonationItem(item_id=max_item+1, donation_id=dr.donation_id, item_name=it.get('item_name'), item_description=it.get('item_description'), item_quantity=it.get('item_quantity',0), item_value=it.get('item_value'))
        db.session.add(di)
    db.session.commit()
    return jsonify({"message":"Donation created","donation_id":dr.donation_id}),201

@app.route('/api/donations', methods=['GET'])
def list_donations():
    donor_id = request.args.get('donor_store_id')
    recs = DonationRecord.query.filter_by(donor_store_id=donor_id).all() if donor_id else DonationRecord.query.all()
    out=[]
    for r in recs:
        items = DonationItem.query.filter_by(donation_id=r.donation_id).all()
        out.append({"donation_id":r.donation_id,"donor_store_id":r.donor_store_id,"donation_amount":r.donation_amount,"donation_type":r.donation_type,"notes":r.notes,
                    "items":[{"item_id":i.item_id,"item_name":i.item_name,"qty":i.item_quantity,"value":i.item_value} for i in items]})
    return jsonify(out)

@app.route('/api/donations/<int:did>', methods=['PUT'])
def update_donation(did):
    donation = DonationRecord.query.get(did)
    if not donation: return jsonify({"error":"Donation not found"}),404
    data = request.json or {}
    if "donation_amount" in data: donation.donation_amount = data["donation_amount"]
    if "donation_type" in data: donation.donation_type = data["donation_type"]
    if "notes" in data: donation.notes = data["notes"]
    db.session.commit()
    return jsonify({"message":"Donation updated","donation_id":did})

@app.route('/api/donations/<int:did>', methods=['DELETE'])
def delete_donation(did):
    donation = DonationRecord.query.get(did)
    if not donation: return jsonify({"error":"Donation not found"}),404
    DonationItem.query.filter_by(donation_id=did).delete()
    db.session.delete(donation)
    db.session.commit()
    return jsonify({"message":"Donation deleted","donation_id":did})

# -----------------------------
# Pickup CRUD
# -----------------------------
@app.route('/api/pickups', methods=['POST'])
def schedule_pickup():
    data = request.json or {}
    donor_store_id, scheduled_date, pickup_address, contact_person, contact_phone = data.get('donor_store_id'), data.get('scheduled_date'), data.get('pickup_address'), data.get('contact_person'), data.get('contact_phone')
    if not (donor_store_id and scheduled_date): return jsonify({"error":"donor_store_id and scheduled_date required"}),400
    max_id = db.session.query(db.func.max(Pickup.pickup_id)).scalar() or 0
    p = Pickup(pickup_id=max_id+1, donor_store_id=donor_store_id, scheduled_date=datetime.fromisoformat(scheduled_date), pickup_address=pickup_address, contact_person=contact_person, contact_phone=contact_phone, status='Scheduled')
    db.session.add(p)
    db.session.commit()
    return jsonify({"message":"Pickup scheduled","pickup_id":p.pickup_id}),201

@app.route('/api/pickups', methods=['GET'])
def get_pickups():
    donor_store_id = request.args.get('donor_store_id')
    pickups = Pickup.query.filter_by(donor_store_id=donor_store_id).all() if donor_store_id else Pickup.query.all()
    return jsonify([{"pickup_id":p.pickup_id,"donor_store_id":p.donor_store_id,"scheduled_date":p.scheduled_date.isoformat(),"pickup_address":p.pickup_address,"contact_person":p.contact_person,"contact_phone":p.contact_phone,"status":p.status} for p in pickups])

@app.route('/api/pickups/<int:pid>/status', methods=['PUT'])
def update_pickup_status(pid):
    p = Pickup.query.get(pid)
    if not p: return jsonify({"error":"pickup not found"}),404
    data = request.json or {}
    if "status" not in data: return jsonify({"error":"status required"}),400
    p.status = data["status"]
    db.session.commit()
    return jsonify({"message":"Updated","pickup_id":pid,"status":p.status})

@app.route('/api/pickups/<int:pid>', methods=['DELETE'])
def delete_pickup(pid):
    p = Pickup.query.get(pid)
    if not p: return jsonify({"error":"Pickup not found"}),404
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message":"Pickup deleted","pickup_id":pid})

# -----------------------------
# Inventory CRUD
# -----------------------------
@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    rows = Inventory.query.all()
    return jsonify([{"inventory_id":r.inventory_id,"center_id":r.center_id,"item_name":r.item_name,"quantity":r.quantity} for r in rows])

@app.route('/api/inventory', methods=['POST'])
def create_inventory():
    data = request.json or {}
    center_id, item_name, quantity = data.get("center_id"), data.get("item_name"), data.get("quantity",0)
    if not (center_id and item_name): return jsonify({"error":"center_id and item_name required"}),400
    max_id = db.session.query(db.func.max(Inventory.inventory_id)).scalar() or 0
    inv = Inventory(inventory_id=max_id+1, center_id=center_id, item_name=item_name, quantity=quantity)
    db.session.add(inv)
    db.session.commit()
    return jsonify({"message":"Inventory created","inventory_id":inv.inventory_id}),201

@app.route('/api/inventory/<int:iid>', methods=['PUT'])
def update_inventory(iid):
    inv = Inventory.query.get(iid)
    if not inv: return jsonify({"error":"Inventory not found"}),404
    data = request.json or {}
    if "item_name" in data: inv.item_name = data["item_name"]
    if "quantity" in data: inv.quantity = data["quantity"]
    db.session.commit()
    return jsonify({"message":"Inventory updated","inventory_id":iid})

@app.route('/api/inventory/<int:iid>', methods=['DELETE'])
def delete_inventory(iid):
    inv = Inventory.query.get(iid)
    if not inv: return jsonify({"error":"Inventory not found"}),404
    db.session.delete(inv)
    db.session.commit()
    return jsonify({"message":"Inventory deleted","inventory_id":iid})

# -----------------------------
# Feedback CRUD
# -----------------------------
@app.route('/api/feedback', methods=['POST'])
def create_feedback():
    data = request.json or {}
    donor_store_id, npo_id, rating, comments = data.get('donor_store_id'), data.get('npo_id'), data.get('rating'), data.get('comments','')
    if not (donor_store_id and npo_id and rating): return jsonify({"error":"donor_store_id, npo_id, and rating are required"}),400
    if rating < 1 or rating > 5: return jsonify({"error":"Rating must be between 1 and 5"}),400
    max_id = db.session.query(db.func.max(FeedbackReview.review_id)).scalar() or 0
    review = FeedbackReview(review_id=max_id+1, donor_store_id=donor_store_id, npo_id=npo_id, rating=rating, comments=comments)
    db.session.add(review)
    db.session.commit()
    return jsonify({"message":"Feedback submitted","review_id":review.review_id,"donor_store_id":donor_store_id,"npo_id":npo_id,"rating":rating,"comments":comments}),201

@app.route('/api/feedback', methods=['GET'])
def get_feedback():
    donor_id, npo_id = request.args.get("donor_store_id"), request.args.get("npo_id")
    query = FeedbackReview.query
    if donor_id: query = query.filter_by(donor_store_id=donor_id)
    if npo_id: query = query.filter_by(npo_id=npo_id)
    rows = query.all()
    return jsonify([{"review_id":r.review_id,"donor_store_id":r.donor_store_id,"npo_id":r.npo_id,"rating":r.rating,"comments":r.comments} for r in rows])

@app.route('/api/feedback/<int:fid>', methods=['PUT'])
def update_feedback(fid):
    r = FeedbackReview.query.get(fid)
    if not r: return jsonify({"error":"Feedback not found"}),404
    data = request.json or {}
    if "rating" in data: r.rating = data["rating"]
    if "comments" in data: r.comments = data["comments"]
    db.session.commit()
    return jsonify({"message":"Feedback updated","review_id":fid})

@app.route('/api/feedback/<int:fid>', methods=['DELETE'])
def delete_feedback(fid):
    r = FeedbackReview.query.get(fid)
    if not r: return jsonify({"error":"Feedback not found"}),404
    db.session.delete(r)
    db.session.commit()
    return jsonify({"message":"Feedback deleted","review_id":fid})

# -----------------------------
# Distribution Centers CRUD
# -----------------------------
@app.route('/api/centers', methods=['POST'])
def create_center():
    data = request.json or {}
    name = data.get("center_name")
    if not name: return jsonify({"error":"center_name required"}),400
    max_id = db.session.query(db.func.max(DistributionCenter.center_id)).scalar() or 0
    c = DistributionCenter(center_id=max_id+1, center_name=name,address=data.get("address"),city=data.get("city"),state=data.get("state"),zip_code=data.get("zip_code"),country=data.get("country"),contact_person=data.get("contact_person"),contact_phone=data.get("contact_phone"))
    db.session.add(c)
    db.session.commit()
    return jsonify({"message":"Center created","center_id":c.center_id}),201

@app.route('/api/centers', methods=['GET'])
def get_centers():
    rows = DistributionCenter.query.all()
    return jsonify([{"center_id":r.center_id,"center_name":r.center_name,"address":r.address,"city":r.city,"state":r.state,"zip_code":r.zip_code,"country":r.country} for r in rows])

@app.route('/api/centers/<int:cid>', methods=['PUT'])
def update_center(cid):
    c = DistributionCenter.query.get(cid)
    if not c: return jsonify({"error":"Center not found"}),404
    data = request.json or {}
    for f in ["center_name","address","city","state","zip_code","country","contact_person","contact_phone"]:
        if f in data: setattr(c,f,data[f])
    db.session.commit()
    return jsonify({"message":"Center updated","center_id":cid})

@app.route('/api/centers/<int:cid>', methods=['DELETE'])
def delete_center(cid):
    c = DistributionCenter.query.get(cid)
    if not c: return jsonify({"error":"Center not found"}),404
    db.session.delete(c)
    db.session.commit()
    return jsonify({"message":"Center deleted","center_id":cid})

from flask import render_template

# Serve homepage
@app.route("/")
def home():
    return render_template("index.html")

# Serve login page
@app.route("/login")
def login_page():
    return render_template("login.html")

# Serve registration page
@app.route("/register")
def register_page():
    return render_template("register.html")

# Donor dashboard
@app.route("/donor-dashboard")
def donor_dashboard_page():
    return render_template("donor-dashboard.html")

# NPO dashboard
@app.route("/npo-dashboard")
def npo_dashboard_page():
    return render_template("npo-dashboard.html")

# Schedule pickup page
@app.route("/schedule-pickup")
def schedule_pickup_page():
    return render_template("schedule-pickup.html")

# -----------------------------
# Additional API Endpoints
# -----------------------------

@app.route('/api/test', methods=['GET'])
def api_test():
    """Simple test endpoint to check if the API is working"""
    return jsonify({"status":"ok","message":"API is reachable"}), 200


@app.route('/api/metrics/npo/<int:npo_id>', methods=['GET'])
def npo_metrics(npo_id):
    """Return some basic metrics for the NPO dashboard"""
    # Total donations received
    total_donations = db.session.query(DonationRecord).join(DonationItem).filter(DonationItem.donation_id==DonationRecord.donation_id).count()
    
    # Total pickups scheduled for this NPO (if you link pickups to NPOs)
    total_pickups = Pickup.query.count()  # adjust if pickups link to NPO

    # Average feedback rating
    feedbacks = FeedbackReview.query.filter_by(npo_id=npo_id).all()
    avg_rating = sum([f.rating for f in feedbacks])/len(feedbacks) if feedbacks else None

    return jsonify({
        "npo_id": npo_id,
        "total_donations": total_donations,
        "total_pickups": total_pickups,
        "average_feedback_rating": avg_rating
    })


@app.route('/api/deliveries/<int:npo_id>', methods=['GET'])
def get_deliveries(npo_id):
    """
    Fetch all deliveries (distributed items) related to a specific NPO.
    """
    deliveries = (
        db.session.query(
            DistributionCenter.center_id.label("delivery_id"),
            Inventory.item_name.label("item_name"),
            Inventory.quantity.label("quantity"),
            db.literal_column("'Delivered'").label("status"),
            DistributionCenter.created_at.label("delivery_date")
        )
        .join(Inventory, Inventory.center_id == DistributionCenter.center_id)
        .all()
    )

    results = [
        {
            "delivery_id": d.delivery_id,
            "item_name": d.item_name,
            "quantity": d.quantity,
            "status": d.status,
            "delivery_date": d.delivery_date.isoformat() if d.delivery_date else None
        }
        for d in deliveries
    ]

    return jsonify(results), 200


# -----------------------------
# App run
# -----------------------------
if __name__ == '__main__':
    with app.app_context():
        init_db(seed=True)
    app.run(debug=True)
