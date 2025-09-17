from app.database.local_db import init_db
from app.models import user_model, habit_model, recommendation_model

def main():
    print("Creating database tables...")
    init_db()
    print("Database tables created successfully!")

if __name__ == "__main__":
    main()