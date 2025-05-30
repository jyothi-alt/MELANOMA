from app import app, db
from modules.models import User, Chat, ChatMessage, PatientRecord, Doctor

def init_database():
    with app.app_context():
        # Drop all tables first
        db.drop_all()
        
        # Create all tables fresh
        db.create_all()
        
        # Create a default doctor
        default_doctor = Doctor(
            name='Dr. Jyothi K.S',
            specialization='Dermatologist'
        )
        db.session.add(default_doctor)
        
        # Create a test user
        test_user = User(username='testuser', email='test@example.com')
        test_user.set_password('password123')
        db.session.add(test_user)
        
        try:
            db.session.commit()
            print("Database initialized successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing database: {str(e)}")

if __name__ == '__main__':
    init_database()
