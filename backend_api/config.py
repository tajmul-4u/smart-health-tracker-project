from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),  # Changed to use root user by default
    'password': os.getenv('DB_PASSWORD', 'root123'),  # Your MySQL root password
    'database': os.getenv('DB_NAME', 'smart_health_tracker')
}

# JWT Settings
JWT_SECRET = os.getenv('JWT_SECRET', 'your-super-secret-key-change-this-in-production')
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30