import os
import sys
import re
import logging
import markdown
import bleach
import os
import sys
import re
import logging
import markdown
import bleach
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from bleach.sanitizer import ALLOWED_TAGS, ALLOWED_ATTRIBUTES
from urllib.parse import quote_plus
# Import Backend Modules
from gemini_handler import GeminiHandler
from ml_model import MLModelHandler
from utils import validate_image
from modules.models import db, User, Chat, ChatMessage, PatientRecord, Doctor

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('sqlalchemy.engine')

# Add project root and backend to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


# Load .env file
load_dotenv(dotenv_path='.env')

print("Environment variables:")
print(f"MYSQL_USER: {os.getenv('MYSQL_USER')}")
print(f"MYSQL_HOST: {os.getenv('MYSQL_HOST')}")
print(f"MYSQL_DATABASE: {os.getenv('MYSQL_DATABASE')}")
print(f"USE_MYSQL: {os.getenv('USE_MYSQL')}")

# Configure allowed HTML tags and attributes for sanitization
ALLOWED_TAGS_LIST = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'ul', 'ol', 'li', 'br']
ALLOWED_ATTRIBUTES_DICT = {'a': ['href', 'title']}

# Flask Configuration
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'templates'),
    static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'static')
)

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', '123456')  # Make sure this is set

# Database configuration
def get_database_url():
    """Get database URL with fallback to SQLite"""
    try:
        if os.getenv('USE_MYSQL', '').lower() == 'true':
            mysql_user = os.getenv('MYSQL_USER', 'root')
            mysql_password = os.getenv('MYSQL_PASSWORD', 'Born@2003')
            mysql_host = os.getenv('MYSQL_HOST', 'localhost')
            mysql_db = os.getenv('MYSQL_DATABASE', 'melanoma_db')
            # URL encode the password to handle special characters
            encoded_password = quote_plus(mysql_password)
            url = f'mysql+pymysql://{mysql_user}:{encoded_password}@{mysql_host}/{mysql_db}'
            print(f"Connecting to database: {url}")  # Debug line
            return url
        else:
            # Fallback to SQLite
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'melanoma.db')
            return 'sqlite:///{db_path}'
    except Exception as e:
        print(f"Error configuring database URL: {str(e)}")
        print("Falling back to SQLite")
        # db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'melanoma.db')
        return 'sqlite:///melanoma.db'  # Fallback to SQLite if there's any error

# Apply database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'super_secret_key')

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {str(e)}")

# Other configurations
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'static', 'uploads')
app.config['SESSION_TYPE'] = 'filesystem'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize AI Handlers
gemini_handler = GeminiHandler()
ml_model_handler = MLModelHandler()

# The rest of your route handlers and helper functions...
# Helper functions for chat and AI interaction
def format_ai_response(text: str) -> str:
    """Format AI response text with proper HTML and sanitization"""
    allowed_tags = [
        'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'strong', 'em', 'b', 'i', 'ul', 'ol', 'li',
        'br', 'span', 'div', 'a'
    ]
    allowed_attributes = {
        'a': ['href', 'title'],
        'img': ['src', 'alt', 'title'],
    }
    
    html = markdown.markdown(text, extensions=['extra'])
    clean_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True
    )
    return clean_html

def get_or_create_chat_session(user_id: int, category: str) -> Chat:
    """Get existing chat session or create new one"""
    today = datetime.utcnow().date()
    chat = Chat.query.filter(
        Chat.user_id == user_id,
        Chat.category == category,
        db.func.date(Chat.created_at) == today
    ).first()
    
    if not chat:
        chat = Chat(user_id=user_id, category=category)
        db.session.add(chat)
        db.session.commit()
    
    return chat

def create_chat_message(chat_id: int, content: str, is_ai: bool, message_type: str = 'chat') -> ChatMessage:
    """Create a new chat message"""
    message = ChatMessage(
        chat_id=chat_id,
        content=content,
        is_ai=is_ai,
        message_type=message_type
    )
    db.session.add(message)
    db.session.commit()
    return message

def format_medical_report(ai_response: str) -> tuple[str, bool]:
    """Format AI response into a structured medical report if it contains medical analysis"""
    if any(keyword in ai_response.lower() for keyword in ['diagnosis', 'analysis', 'symptoms', 'recommendation']):
        sections = {
            'Diagnosis': '',
            'Analysis': '',
            'Symptoms': '',
            'Recommendations': '',
            'Risk Level': ''
        }
        
        current_section = None
        for line in ai_response.split('\n'):
            for section in sections.keys():
                if section.lower() in line.lower():
                    current_section = section
                    continue
            if current_section and line.strip():
                sections[current_section] += line + '\n'
        
        report_html = '<div class="medical-report-content">'
        for section, content in sections.items():
            if content:
                report_html += f'''
                    <div class="medical-report-section">
                        <h5>{section}</h5>
                        <p>{content}</p>
                    </div>
                '''
        report_html += '</div>'
        return report_html, True
    return ai_response, False

def categorize_chat(query: str) -> str:
    """Categorize chat messages based on content"""
    categories = {
        'Diagnosis': r'diagnos|analys|examin',
        'Symptoms': r'symptom|feel|pain|notice',
        'Treatment': r'treat|medication|therapy|cure',
        'Prevention': r'prevent|protect|avoid',
        'General': r'.*'
    }
    
    for category, pattern in categories.items():
        if re.search(pattern, query.lower()):
            return category
    return 'General'

# Route handlers
@app.route('/')
def index():
    """Render Home Page
    
    Returns:
        rendered template for index.html
    """
    user_id = session.get('user_id', None)
    return render_template('index.html', user_id=user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login with database authentication"""
    if request.method == 'POST':
        username = request.form['username']
        print(f"Login attempt for username: {username}")  # Debug line
        password = request.form['password']


        user = User.query.filter_by(username=username).first()
        print(f"User found: {user is not None}")  # Debug line
        
        if user and user.check_password(password):
            print("Password check passed")  # Debug line
            session['user_id'] = user.id
            session['username'] = username
            session.permanent = True
            app.permanent_session_lifetime = timedelta(days=1)
            flash('Login successful!', 'success')
            print("Redirecting to dashboard...")  # Debug line
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials, try again.', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup with database storage"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email', '')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'warning')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered.', 'warning')
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    """User Dashboard"""
    print(f"Dashboard accessed. Session: {session}")  # Debug line
    if 'username' not in session:
        print("No username in session, redirecting to login")  # Debug line
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    print(f"Rendering dashboard for user: {session['username']}")  # Debug line
    return render_template('dashboard.html', username=session['username'])

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction with database storage"""
    if 'user_id' not in session:
        flash('Please log in to use this feature.', 'warning')
        return redirect(url_for('login'))
    
    if 'file' not in request.files:
        flash('No file uploaded.', 'warning')
        return redirect(url_for('dashboard'))
    
    file = request.files['file']
    if file.filename == '' or file.filename is None:
        flash('No selected file.', 'warning')
        return redirect(url_for('dashboard'))
    
    if not validate_image(file):
        flash('Invalid image file.', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        filename = secure_filename(str(file.filename))
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        melanoma_prob = ml_model_handler.predict(file_path)
        prompt = f"Patient has a melanoma probability of {melanoma_prob * 100:.2f}%. Provide a detailed medical consultation considering the risk level."
        consultation = gemini_handler.get_medical_consultation(prompt)
        formatted_consultation = format_ai_response(consultation)
        
        risk_level = "High" if melanoma_prob > 0.7 else "Moderate" if melanoma_prob > 0.3 else "Low"
        # Get default doctor (Dr. Jyothi K.S)
        default_doctor = Doctor.query.filter_by(name='Dr. Jyothi K.S').first()
        record = PatientRecord(
            user_id=session['user_id'],
            doctor_id=default_doctor.id if default_doctor else None,
            image_path=file_path,
            diagnosis_probability=melanoma_prob,
            risk_level=risk_level,
            consultation=formatted_consultation,
            status='reviewed'  # Since it's automatically reviewed by AI
        )
        db.session.add(record)
        db.session.commit()
        
        return render_template(
            'result.html',
            image_url=url_for('static', filename=f'uploads/{filename}'),
            confidence=f"{melanoma_prob * 100:.2f}%",
            risk_level=risk_level,
            consultation=formatted_consultation
        )
        
    except Exception as e:
        flash(f"Error: {str(e)}", 'danger')
        return redirect(url_for('dashboard'))

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    """AI-powered patient consultation chat with database storage"""
    if 'user_id' not in session:
        flash('Please log in to use the chat feature.', 'warning')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    chat_history = []
    categories = []
    
    # Get existing chat history
    chats = Chat.query.filter_by(user_id=user_id).order_by(Chat.created_at.desc()).all()
    for chat in chats:
        messages = ChatMessage.query.filter_by(chat_id=chat.id).order_by(ChatMessage.created_at.asc()).all()
        for msg in messages:
            chat_history.append({
                'user': msg.content if not msg.is_ai else None,
                'ai': msg.content if msg.is_ai else None,
                'type': msg.message_type,
                'timestamp': msg.created_at,
                'category': chat.category
            })
    
    if request.method == 'POST':
        user_query = request.form['query']
        category = categorize_chat(user_query)
        
        try:
            chat = get_or_create_chat_session(user_id, category)
            create_chat_message(chat.id, user_query, is_ai=False)
            
            ai_response = gemini_handler.get_medical_consultation(user_query)
            formatted_response = format_ai_response(ai_response)
            
            create_chat_message(
                chat.id,
                formatted_response,
                is_ai=True,
                message_type='report' if 'medical-report-content' in formatted_response else 'chat'
            )
            
            chats = Chat.query.filter_by(user_id=user_id).all()
            for chat in chats:
                messages = ChatMessage.query.filter_by(chat_id=chat.id).order_by(ChatMessage.created_at.desc()).all()
                for msg in messages:
                    chat_history.append({
                        'user': msg.content if not msg.is_ai else None,
                        'ai': msg.content if msg.is_ai else None,
                        'type': msg.message_type,
                        'timestamp': msg.created_at,
                        'category': chat.category
                    })
            
            chat_history.sort(key=lambda x: x['timestamp'], reverse=True)
            
            categories = db.session.query(
                Chat.category,
                db.func.count(ChatMessage.id).label('count')
            ).join(ChatMessage).group_by(Chat.category).all()
            
            categories = [{'name': cat, 'count': count} for cat, count in categories]
            
        except Exception as e:
            flash(f"Error: {str(e)}", 'danger')
    
    return render_template('chat.html',
                         chat_history=chat_history,
                         categories=categories)

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/consult')
def consult():
    return render_template('consult.html')

@app.route('/test-flash')
def test_flash():
    """Test route to demonstrate flash messages"""
    flash('This is a success message!', 'success')
    flash('This is a warning message!', 'warning')
    flash('This is an error message!', 'danger')
    flash('This is an info message!', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
