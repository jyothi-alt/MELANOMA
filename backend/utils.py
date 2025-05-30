import re
from typing import List, Tuple
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

def validate_image(file) -> bool:
    """
    Validate uploaded image file
    
    Args:
        file (FileStorage): Uploaded file
    
    Returns:
        bool: True if file is valid, False otherwise
    """
    # Check if filename is not empty
    if not file.filename:
        return False
    
    # Check file extension
    filename = secure_filename(file.filename)
    if not filename:
        return False
    
    # Get file extension
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    # Validate extension
    if ext not in ALLOWED_EXTENSIONS:
        return False
    
    return True

def generate_unique_filename(filename):
    """
    Generate a unique filename to prevent overwriting
    
    Args:
        filename (str): Original filename
    
    Returns:
        str: Unique filename
    """
    import uuid
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    return unique_filename

def extract_sections(text: str) -> List[Tuple[str, str]]:
    """Extract sections from AI response text"""
    sections = []
    current_section = None
    current_content = []
    
    for line in text.splitlines():
        # Check if line starts with common section markers
        if re.match(r'^[*#]+\s+|^[A-Z][A-Za-z\s]+:', line):
            if current_section:
                sections.append((current_section, '\n'.join(current_content).strip()))
            current_section = re.sub(r'^[*#]+\s+|:', '', line).strip()
            current_content = []
        else:
            current_content.append(line)
    
    if current_section:
        sections.append((current_section, '\n'.join(current_content).strip()))
    
    return sections

def markdown_to_html(text: str) -> str:
    """Convert markdown-like syntax to HTML"""
    # Convert bullet points
    text = re.sub(r'^\*\s+(.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.*</li>\n*)+', r'<ul>\g<0></ul>', text, flags=re.MULTILINE)
    
    # Convert bold text
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Convert italics
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    
    # Convert headers
    text = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    
    # Convert paragraphs
    text = re.sub(r'\n\n(.+?)\n\n', r'<p>\1</p>', text, flags=re.MULTILINE)
    
    return text