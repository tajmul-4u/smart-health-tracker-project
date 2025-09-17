# Smart Health Tracker

A comprehensive health monitoring and recommendation system with AI-powered insights.

## Features

- User authentication and profile management
- Health habit tracking
- AI-powered health recommendations
- Cloud synchronization
- Data analytics and progress tracking
- Cross-platform support (Desktop & API)

## Technology Stack

- **Frontend:** PyQt6 (Desktop GUI)
- **Backend:** FastAPI
- **Databases:** 
  - Local: SQLite
  - Cloud: PostgreSQL
- **AI/ML:** scikit-learn, numpy, pandas
- **Authentication:** JWT, bcrypt

## Project Structure

```
smart_health_tracker/
├── app/                    # Desktop application
│   ├── main.py            # Entry point
│   ├── ui/                # UI files
│   ├── controllers/       # GUI controllers
│   ├── models/           # Database models
│   ├── services/         # Business logic
│   ├── database/         # DB layer
│   └── utils/           # Helper functions
├── backend_api/          # FastAPI backend
├── tests/               # Unit & integration tests
└── docs/               # Documentation
```

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Development

Check PROJECT_SETUP.md for detailed development guidelines and procedures.

## Testing

```bash
pytest tests/
```

## License

[MIT License](LICENSE)
