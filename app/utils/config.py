import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'smart_health_tracker'),
}

# JWT Configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION = 3600  # 1 hour

# API Configuration
API_URL = os.getenv('API_URL', 'http://localhost:8000')

# AI Model Configuration
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/ai_models/')
