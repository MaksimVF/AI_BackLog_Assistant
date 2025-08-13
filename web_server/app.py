



"""
Flask Web Server for AI Backlog Assistant with Group Authentication Model
"""

import os
import uuid
import datetime
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate

from argon2.exceptions import VerifyMismatchError
from authlib.integrations.flask_client import OAuth
from google_auth import get_google_credentials
from google_drive_connector import GoogleDriveConnector
from google_sheets_connector import GoogleSheetsConnector
from google_calendar_connector import GoogleCalendarConnector

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# OAuth Configuration
app.config['GITHUB_CLIENT_ID'] = os.getenv('GITHUB_CLIENT_ID')
app.config['GITHUB_CLIENT_SECRET'] = os.getenv('GITHUB_CLIENT_SECRET')
app.config['GITLAB_CLIENT_ID'] = os.getenv('GITLAB_CLIENT_ID')
app.config['GITLAB_CLIENT_SECRET'] = os.getenv('GITLAB_CLIENT_SECRET')
app.config['BITBUCKET_CLIENT_ID'] = os.getenv('BITBUCKET_CLIENT_ID')
app.config['BITBUCKET_CLIENT_SECRET'] = os.getenv('BITBUCKET_CLIENT_SECRET')
app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')
app.config['TELEGRAM_CLIENT_ID'] = os.getenv('TELEGRAM_CLIENT_ID')
app.config['TELEGRAM_CLIENT_SECRET'] = os.getenv('TELEGRAM_CLIENT_SECRET')

# Initialize OAuth
oauth = OAuth(app)

# Register OAuth providers
github = oauth.register(
    name='github',
    client_id=app.config['GITHUB_CLIENT_ID'],
    client_secret=app.config['GITHUB_CLIENT_SECRET'],
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

gitlab = oauth.register(
    name='gitlab',
    client_id=app.config['GITLAB_CLIENT_ID'],
    client_secret=app.config['GITLAB_CLIENT_SECRET'],
    authorize_url='https://gitlab.com/oauth/authorize',
    authorize_params=None,
    access_token_url='https://gitlab.com/oauth/token',
    access_token_params=None,
    api_base_url='https://gitlab.com/api/v4/',
    client_kwargs={'scope': 'read_user'},
)

bitbucket = oauth.register(
    name='bitbucket',
    client_id=app.config['BITBUCKET_CLIENT_ID'],
    client_secret=app.config['BITBUCKET_CLIENT_SECRET'],
    authorize_url='https://bitbucket.org/site/oauth2/authorize',
    authorize_params=None,
    access_token_url='https://bitbucket.org/site/oauth2/access_token',
    access_token_params=None,
    api_base_url='https://api.bitbucket.org/2.0/',
    client_kwargs={'scope': 'account'},
)

google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'},
)

telegram = oauth.register(
    name='telegram',
    client_id=app.config['TELEGRAM_CLIENT_ID'],
    client_secret=app.config['TELEGRAM_CLIENT_SECRET'],
    authorize_url='https://oauth.telegram.org/auth',
    authorize_params=None,
    access_token_url='https://oauth.telegram.org/token',
    access_token_params=None,
    api_base_url='https://api.telegram.org/',
    client_kwargs={'scope': 'profile'},
)

# Import extensions
from .extensions import db, migrate, login_manager, ph

# Initialize extensions with app
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = 'login'

# Register billing blueprint
from .billing_routes import billing_bp
app.register_blueprint(billing_bp)

# Register team management blueprint
from .team_routes import team_bp
app.register_blueprint(team_bp)

# Register team management test blueprint
from .team_routes_test import team_test_bp
app.register_blueprint(team_test_bp)

# Register API Gateway blueprint
from .api_gateway import api_gateway_bp
app.register_blueprint(api_gateway_bp)

# Register Admin blueprint
from .admin_routes import admin_bp
app.register_blueprint(admin_bp)

# Import application models
from .models import User, Organization, OrganizationMember, ActiveContext

# Load user for login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))

# Middleware for loading current organization context
@app.before_request
def load_current_organization():
    if current_user.is_authenticated:
        # Get the current organization ID from session or active context
        org_id = session.get('current_org_id')
        if not org_id:
            # Try to get from active context
            active_context = ActiveContext.query.filter_by(user_id=current_user.id).first()
            if active_context and active_context.current_organization_id:
                org_id = active_context.current_organization_id
                session['current_org_id'] = org_id

        if org_id:
            g.organization = Organization.query.get(org_id)
        else:
            g.organization = None
    else:
        g.organization = None

# Routes
@app.route('/')
@app.route('/index')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/project')
@login_required
def project():
    """Project page"""
    return render_template('project.html')

@app.route('/analytics')
@login_required
def analytics():
    """Analytics page"""
    return render_template('analytics.html')

@app.route('/settings')
@login_required
def settings():
    """Settings page"""
    # Check Google authentication status
    google_connected = bool(session.get('google_credentials'))

    # Get Google services status
    drive_status = 'Connected' if google_connected else 'Disconnected'
    sheets_status = 'Connected' if google_connected else 'Disconnected'
    calendar_status = 'Connected' if google_connected else 'Disconnected'

    return render_template('settings.html',
                         google_connected=google_connected,
                         drive_status=drive_status,
                         sheets_status=sheets_status,
                         calendar_status=calendar_status,
                         current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error='Username already exists')

        # Check if email exists
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return render_template('register.html', error='Email already exists')

        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    return redirect(url_for('index'))

# Organization Routes
@app.route('/org/create', methods=['GET', 'POST'])
@login_required
def create_organization():
    """Create a new organization"""
    if request.method == 'POST':
        name = request.form.get('name')

        # Create new organization
        new_org = Organization(name=name, created_by=current_user.id)

        # Add the creator as the owner
        db.session.add(new_org)
        db.session.commit()

        # Create organization membership for the creator
        membership = OrganizationMember(
            user_id=current_user.id,
            organization_id=new_org.id,
            role='owner'
        )
        db.session.add(membership)

        # Set as current organization
        active_context = ActiveContext.query.filter_by(user_id=current_user.id).first()
        if active_context:
            active_context.current_organization_id = new_org.id
        else:
            new_context = ActiveContext(
                user_id=current_user.id,
                current_organization_id=new_org.id
            )
            db.session.add(new_context)

        db.session.commit()

        # Update session
        session['current_org_id'] = new_org.id
        g.organization = new_org

        return redirect(url_for('index'))

    return render_template('create_org.html')

@app.route('/org/switch/<org_id>')
@login_required
def switch_organization(org_id):
    """Switch to a different organization context"""
    # Check if user is a member of the organization
    membership = OrganizationMember.query.filter_by(
        user_id=current_user.id,
        organization_id=org_id
    ).first()

    if not membership:
        return redirect(url_for('index'))  # Or show error

    # Update active context
    active_context = ActiveContext.query.filter_by(user_id=current_user.id).first()
    if active_context:
        active_context.current_organization_id = org_id
    else:
        new_context = ActiveContext(
            user_id=current_user.id,
            current_organization_id=org_id
        )
        db.session.add(new_context)

    db.session.commit()

    # Update session
    session['current_org_id'] = org_id
    g.organization = Organization.query.get(org_id)

    return redirect(url_for('index'))

@app.route('/org/<org_id>/invite', methods=['POST'])
@login_required
def invite_to_organization(org_id):
    """Invite a user to an organization"""
    # Check if current user has permission to invite
    membership = OrganizationMember.query.filter_by(
        user_id=current_user.id,
        organization_id=org_id
    ).first()

    if not membership or membership.role not in ['owner', 'admin']:
        return jsonify({'error': 'Permission denied'}), 403

    email = request.form.get('email')
    role = request.form.get('role', 'member')

    # Find user by email
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check if already a member
    existing_membership = OrganizationMember.query.filter_by(
        user_id=user.id,
        organization_id=org_id
    ).first()

    if existing_membership:
        return jsonify({'error': 'User already a member'}), 400

    # Add to organization
    new_membership = OrganizationMember(
        user_id=user.id,
        organization_id=org_id,
        role=role
    )
    db.session.add(new_membership)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': f'User {user.username} added to organization'
    })

@app.route('/org/<org_id>/remove/<user_id>', methods=['POST'])
@login_required
def remove_from_organization(org_id, user_id):
    """Remove a user from an organization"""
    # Check if current user has permission to remove
    membership = OrganizationMember.query.filter_by(
        user_id=current_user.id,
        organization_id=org_id
    ).first()

    if not membership or membership.role != 'owner':
        return jsonify({'error': 'Permission denied'}), 403

    # Cannot remove yourself if you're the owner
    if user_id == current_user.id:
        return jsonify({'error': 'Cannot remove yourself as owner'}), 400

    # Remove membership
    user_membership = OrganizationMember.query.filter_by(
        user_id=user_id,
        organization_id=org_id
    ).first()

    if user_membership:
        db.session.delete(user_membership)
        db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'User removed from organization'
    })

# User Profile Route
@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    # Get user's organizations
    organizations = Organization.query.join(
        OrganizationMember
    ).filter(
        OrganizationMember.user_id == current_user.id
    ).all()

    # Get current organization
    current_org = g.organization

    return render_template('profile.html',
                         user=current_user,
                         organizations=organizations,
                         current_org=current_org)

# API Endpoints
@app.route('/api/status')
def api_status():
    """System status API"""
    return jsonify({
        'status': 'online',
        'version': '1.0.0',
        'message': 'AI Backlog Assistant API is running'
    })

@app.route('/api/upload', methods=['POST'])
@login_required
def api_upload():
    """Document upload API"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save file (temporary implementation)
    file.save(f'uploads/{file.filename}')

    return jsonify({
        'status': 'success',
        'filename': file.filename,
        'message': 'File uploaded successfully'
    })

@app.route('/export_to_sheets')
@login_required
def export_to_sheets():
    """Export issues to Google Sheets"""
    credentials = get_google_credentials()
    if not credentials:
        return redirect(url_for('google_login'))

    # Mock issues data
    ISSUES = [
        {
            'id': 1,
            'title': 'Design pipeline architecture',
            'status': 'Done',
            'priority': 'High',
            'assignee': 'Alice',
            'created_at': '2023-01-01',
            'updated_at': '2023-01-10'
        },
        {
            'id': 2,
            'title': 'Implement base pipeline',
            'status': 'In Progress',
            'priority': 'High',
            'assignee': 'Bob',
            'created_at': '2023-01-02',
            'updated_at': '2023-01-05'
        },
        {
            'id': 3,
            'title': 'Create IMP agents',
            'status': 'Backlog',
            'priority': 'Medium',
            'assignee': 'Unassigned',
            'created_at': '2023-01-03',
            'updated_at': '2023-01-03'
        }
    ]

    # Export issues to Google Sheets
    sheets = GoogleSheetsConnector(credentials)
    spreadsheet = sheets.create_spreadsheet('Issue Export')

    if spreadsheet:
        # Prepare data
        headers = ['ID', 'Title', 'Status', 'Priority', 'Assignee', 'Created At', 'Updated At']
        data = [headers]
        for issue in ISSUES:
            data.append([
                issue['id'],
                issue['title'],
                issue['status'],
                issue['priority'],
                issue['assignee'],
                issue['created_at'],
                issue['updated_at']
            ])

        # Write data
        sheets.write_data(spreadsheet['spreadsheetId'], 'Issues', data)

        return redirect(spreadsheet['spreadsheetUrl'])
    else:
        return "Failed to create spreadsheet", 500

@app.route('/schedule_review/<int:issue_id>')
@login_required
def schedule_review(issue_id):
    """Schedule an issue review meeting"""
    credentials = get_google_credentials()
    if not credentials:
        return redirect(url_for('google_login'))

    # Mock issue data
    ISSUES = {
        1: {'id': 1, 'title': 'Design pipeline architecture'},
        2: {'id': 2, 'title': 'Implement base pipeline'},
        3: {'id': 3, 'title': 'Create IMP agents'}
    }

    issue = ISSUES.get(issue_id)
    if not issue:
        return "Issue not found", 404

    # Schedule a meeting
    calendar = GoogleCalendarConnector(credentials)
    start_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    end_time = start_time + datetime.timedelta(minutes=30)

    event = calendar.create_event(
        'primary',
        f"Issue Review: {issue['title']}",
        f"Review and discuss issue #{issue['id']}",
        start_time,
        end_time,
        ['team@example.com']
    )

    if event:
        return redirect(event['htmlLink'])
    else:
        return "Failed to create event", 500

# Create database tables
with app.app_context():
    db.create_all()

# OAuth Authentication Routes
@app.route('/auth/github')
def github_login():
    """GitHub login"""
    redirect_uri = url_for('github_auth', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/auth/github/callback')
def github_auth():
    """GitHub auth callback"""
    token = github.authorize_access_token()
    resp = github.get('user')
    user_data = resp.json()

    # Get email (GitHub requires separate API call)
    emails_resp = github.get('user/emails')
    emails = emails_resp.json()
    email = emails[0]['email'] if emails else f"{user_data['id']}@github.user"

    # Find or create user
    user = User.query.filter_by(github_id=str(user_data['id'])).first()
    if not user:
        user = User.query.filter_by(email=email).first()

    if not user:
        # Create new user
        user = User(
            username=user_data['login'],
            email=email,
            github_id=str(user_data['id'])
        )
        db.session.add(user)
        db.session.commit()
    else:
        # Update existing user
        user.github_id = str(user_data['id'])
        user.username = user_data['login']
        db.session.commit()

    login_user(user)
    return redirect(url_for('index'))

@app.route('/auth/gitlab')
def gitlab_login():
    """GitLab login"""
    redirect_uri = url_for('gitlab_auth', _external=True)
    return gitlab.authorize_redirect(redirect_uri)

@app.route('/auth/gitlab/callback')
def gitlab_auth():
    """GitLab auth callback"""
    token = gitlab.authorize_access_token()
    resp = gitlab.get('user')
    user_data = resp.json()

    email = user_data.get('email') or f"{user_data['id']}@gitlab.user"

    # Find or create user
    user = User.query.filter_by(gitlab_id=str(user_data['id'])).first()
    if not user:
        user = User.query.filter_by(email=email).first()

    if not user:
        # Create new user
        user = User(
            username=user_data['username'],
            email=email,
            gitlab_id=str(user_data['id'])
        )
        db.session.add(user)
        db.session.commit()
    else:
        # Update existing user
        user.gitlab_id = str(user_data['id'])
        user.username = user_data['username']
        db.session.commit()

    login_user(user)
    return redirect(url_for('index'))

@app.route('/auth/bitbucket')
def bitbucket_login():
    """Bitbucket login"""
    redirect_uri = url_for('bitbucket_auth', _external=True)
    return bitbucket.authorize_redirect(redirect_uri)

@app.route('/auth/bitbucket/callback')
def bitbucket_auth():
    """Bitbucket auth callback"""
    token = bitbucket.authorize_access_token()
    resp = bitbucket.get('user')
    user_data = resp.json()

    email = user_data.get('email') or f"{user_data['uuid']}@bitbucket.user"

    # Find or create user
    user = User.query.filter_by(bitbucket_id=user_data['uuid']).first()
    if not user:
        user = User.query.filter_by(email=email).first()

    if not user:
        # Create new user
        user = User(
            username=user_data['username'],
            email=email,
            bitbucket_id=user_data['uuid']
        )
        db.session.add(user)
        db.session.commit()
    else:
        # Update existing user
        user.bitbucket_id = user_data['uuid']
        user.username = user_data['username']
        db.session.commit()

    login_user(user)
    return redirect(url_for('index'))

@app.route('/auth/google')
def google_login():
    """Google login"""
    redirect_uri = url_for('google_auth', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/google/callback')
def google_auth():
    """Google auth callback"""
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_data = resp.json()

    email = user_data['email']

    # Find or create user
    user = User.query.filter_by(google_id=user_data['id']).first()
    if not user:
        user = User.query.filter_by(email=email).first()

    if not user:
        # Create new user
        user = User(
            username=user_data['name'].replace(' ', '_'),
            email=email,
            google_id=user_data['id']
        )
        db.session.add(user)
        db.session.commit()
    else:
        # Update existing user
        user.google_id = user_data['id']
        user.username = user_data['name'].replace(' ', '_')
        db.session.commit()

    login_user(user)
    return redirect(url_for('index'))

@app.route('/auth/telegram')
def telegram_login():
    """Telegram login"""
    redirect_uri = url_for('telegram_auth', _external=True)
    return telegram.authorize_redirect(redirect_uri)

@app.route('/auth/telegram/callback')
def telegram_auth():
    """Telegram auth callback"""
    token = telegram.authorize_access_token()
    resp = telegram.get('userinfo')
    user_data = resp.json()

    # Telegram user info structure
    telegram_id = str(user_data.get('id'))
    username = user_data.get('username') or f"telegram_{telegram_id}"
    email = user_data.get('email') or f"{telegram_id}@telegram.user"

    # Find or create user
    user = User.query.filter_by(telegram_id=telegram_id).first()
    if not user:
        user = User.query.filter_by(email=email).first()

    if not user:
        # Create new user
        user = User(
            username=username,
            email=email,
            telegram_id=telegram_id
        )
        db.session.add(user)
        db.session.commit()
    else:
        # Update existing user
        user.telegram_id = telegram_id
        user.username = username
        db.session.commit()

    login_user(user)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Create uploads directory
    os.makedirs('uploads', exist_ok=True)

    # Initialize background jobs
    from web_server.background_jobs import init_background_jobs
    init_background_jobs()

    app.run(debug=True, host='0.0.0.0', port=5000)




