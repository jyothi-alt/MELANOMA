# 🩺 AI Melanoma Detection System

A comprehensive Flask web application that uses artificial intelligence to detect and analyze skin lesions for potential melanoma. This system combines deep learning image classification with AI-powered medical consultation to provide users with preliminary skin cancer screening capabilities.

![Flask](https://img.shields.io/badge/Flask-2.3.2-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13+-orange)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Features

### 🔬 **AI-Powered Skin Lesion Analysis**
- **Deep Learning Classification**: Uses a trained TensorFlow model to analyze skin lesion images
- **Multi-class Detection**: Identifies 9 different types of skin conditions:
  - Melanoma
  - Basal Cell Carcinoma
  - Squamous Cell Carcinoma
  - Actinic Keratosis
  - Seborrheic Keratosis
  - Nevus (Moles)
  - Dermatofibroma
  - Pigmented Benign Keratosis
  - Vascular Lesions
- **Confidence Scoring**: Provides probability assessments for each prediction
- **Risk Level Assessment**: Categorizes findings into risk levels

### 🤖 **AI Medical Consultation**
- **Interactive Chat Interface**: Real-time conversation with AI medical assistant
- **Contextual Responses**: AI provides relevant medical information based on uploaded images
- **Chat History**: Persistent conversation history for each user
- **Medical Disclaimers**: Appropriate warnings about the limitations of AI diagnosis

### 👥 **User Management**
- **Secure Authentication**: User registration and login system
- **Session Management**: Persistent user sessions
- **Patient Records**: Store and track analysis history
- **Dashboard**: Personal user dashboard with quick access to features

### 💾 **Data Management**
- **MySQL Database**: Robust data storage for users, chats, and medical records
- **Image Upload**: Secure file handling with validation
- **Record Keeping**: Complete audit trail of all analyses

### 🎨 **Modern Web Interface**
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Flash Messages**: Real-time user feedback with styled notifications
- **Professional UI**: Clean, medical-grade interface design
- **Interactive Elements**: Drag-and-drop file uploads and live image previews

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.11 or higher
- MySQL 8.0 or higher
- pip package manager
- Git (for cloning the repository)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd "research capstone"
```

### 2. Environment Setup

Create a virtual environment (recommended):

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=melanoma_db
USE_MYSQL=True

# Flask Configuration
FLASK_SECRET_KEY=your_secret_key_here
FLASK_DEBUG=True

# AI Configuration
GEMINI_API_KEY=your_gemini_api_key
```

### 5. Database Setup

**Create MySQL Database:**
```sql
CREATE DATABASE melanoma_db;
```

**Initialize Database Tables:**
```bash
cd backend
python init_db.py
```

This will create all necessary tables and add a default test user:
- **Username**: `testuser`
- **Password**: `password123`
<!-- - **Default Doctor**: `Dr. Jyothi K.S` -->

### 6. Verify ML Model

Ensure the trained model file exists at:
```
models/melanoma_model.h5
```

### 7. Run the Application

```bash
cd backend
python app.py
```

The application will start on `http://127.0.0.1:5000`

## 📱 Usage Guide

### **1. Registration & Login**
- Navigate to `/signup` to create a new account
- Use `/login` to access existing accounts
- Test with credentials: `testuser` / `password123`

### **2. Image Analysis**
1. Go to the homepage (`/`)
2. Click "Upload Skin Image" or drag and drop an image
3. Supported formats: JPG, JPEG, PNG
4. Click "Analyze Skin Lesion"
5. View detailed results including:
   - Prediction confidence
   - Risk level assessment
   - AI medical consultation
   - Image analysis summary

### **3. AI Chat Consultation**
1. Access via "AI Medical Consultation" button
2. Ask questions about skin conditions
3. Get contextual medical information
4. View chat history and categories

### **4. Dashboard**
- Access personal dashboard at `/dashboard`
- View analysis history
- Quick access to upload and chat features

## 🏗️ Project Structure

```
research-capstone/
├── backend/                    # Flask application backend
│   ├── app.py                 # Main Flask application
│   ├── gemini_handler.py      # AI chat integration
│   ├── ml_model.py           # ML model handling
│   ├── utils.py              # Utility functions
│   ├── init_db.py            # Database initialization
│   └── modules/
│       └── models.py         # Database models
├── frontend/                   # Web interface
│   ├── templates/            # Jinja2 HTML templates
│   │   ├── base.html         # Base template
│   │   ├── index.html        # Homepage
│   │   ├── login.html        # Login page
│   │   ├── result.html       # Analysis results
│   │   ├── chat.html         # AI chat interface
│   │   └── ...
│   └── static/               # CSS, JS, images
│       ├── css/
│       ├── js/
│       └── uploads/          # User uploaded images
├── models/                     # ML model files
│   └── melanoma_model.h5     # Trained TensorFlow model
├── data/                      # Training/test datasets
│   ├── Train/                # Training images
│   └── Test/                 # Test images
├── requirements.txt           # Python dependencies
├── setup.py                  # Package setup
└── README.md                 # This file
```

## 🧪 Testing

### Test Routes
- `/test-flash` - Test flash message functionality
- All routes include proper error handling and user feedback

### Test Data
Sample images are provided in the `data/Test/` directory organized by condition type.

## 🔧 Configuration

### Database Configuration
Edit the `.env` file to configure your MySQL connection:
```env
MYSQL_HOST=localhost
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=melanoma_db
```

### Flask Configuration
- Debug mode: Set `FLASK_DEBUG=True` for development
- Secret key: Use a strong, unique secret key for production
- Session configuration is handled automatically

### AI Integration
- Gemini API: Add your Google Gemini API key to `.env`
- Model path: Ensure the ML model is accessible at `models/melanoma_model.h5`

## 🔒 Security Features

- **Input Validation**: All user inputs are validated and sanitized
- **File Upload Security**: Secure filename handling and file type validation
- **SQL Injection Protection**: SQLAlchemy ORM provides protection
- **Session Security**: Secure session management with proper configuration
- **Password Security**: User passwords are properly hashed

## 📊 Database Schema

### Tables
- **users**: User authentication and profile data
- **doctors**: Medical professional information
- **patient_records**: Analysis results and medical history
- **chats**: Chat session management
- **chat_messages**: Individual chat messages

## 🚨 Important Disclaimers

⚠️ **Medical Disclaimer**: This application is for educational and screening purposes only. It is NOT a substitute for professional medical diagnosis or treatment. Always consult with qualified healthcare professionals for accurate medical advice.

⚠️ **AI Limitations**: The AI model provides probability assessments based on image analysis. Results should not be considered definitive medical diagnoses.

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error:**
- Verify MySQL is running
- Check connection credentials in `.env`
- Ensure database `melanoma_db` exists

**Model Loading Error:**
- Verify `melanoma_model.h5` exists in `models/` directory
- Check TensorFlow installation
- Ensure compatible model format

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version compatibility (3.11+)

**Flash Messages Not Appearing:**
- Clear browser cache
- Check browser console for JavaScript errors
- Verify template extends `base.html`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Research Capstone Team** - Initial development

## 🙏 Acknowledgments

- TensorFlow team for the deep learning framework
- Flask community for the web framework
- Medical professionals who provided domain expertise
- Open source contributors and the Python community

---

**⚡ Quick Start**: After installation, run `python backend/app.py` and visit `http://127.0.0.1:5000` to get started!
