# Data Entry System with Supabase

A modern, responsive web application for data entry built with Python Flask and Supabase database. Features a clean Bootstrap UI with full CRUD operations, form validation, and RESTful API endpoints.

## Features

- ✨ **Modern UI**: Clean, responsive design with Bootstrap 5 and custom CSS
- 🔐 **Supabase Integration**: Secure cloud database with real-time capabilities
- 📝 **Complete CRUD**: Create, Read, Update, Delete operations
- ✅ **Form Validation**: Client-side and server-side validation with WTForms
- 🔌 **RESTful API**: JSON API endpoints for programmatic access
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- 🎨 **Interactive Features**: Delete confirmations, character counters, copy-to-clipboard

## Demo

The application includes:
- **Home Page**: Display all data entries in a responsive table
- **Add Entry**: Form to create new data entries
- **Edit Entry**: Update existing entries with pre-populated forms
- **Delete**: Confirmation modal for safe deletion
- **API Endpoints**: RESTful API for integration with other systems

## Quick Start

### Prerequisites

- Python 3.8 or higher
- A Supabase account and project
- Git (for cloning the repository)

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd data-entry-system
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Supabase

1. Create a new project at [Supabase](https://supabase.com)
2. Go to Settings → API to get your project URL and anon key
3. In the SQL Editor, run the following SQL to create the table:

```sql
CREATE TABLE IF NOT EXISTS data_entries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    category VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Optional: Add some sample data
INSERT INTO data_entries (name, email, phone, category, description) VALUES
('John Doe', 'john@example.com', '+1-555-0123', 'business', 'Sample business contact'),
('Jane Smith', 'jane@example.com', '+1-555-0124', 'personal', 'Personal contact information');
```

### 5. Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your Supabase credentials:
```
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_KEY=your_supabase_anon_key_here
SECRET_KEY=your_secret_key_for_flask_sessions
```

### 6. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
data-entry-system/
├── app.py              # Main Flask application
├── config.py           # Configuration and Supabase client
├── models.py           # Data models and database operations
├── forms.py            # WTForms for form validation
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── .env               # Your environment variables (create this)
├── README.md          # This file
├── templates/         # HTML templates
│   ├── base.html      # Base template with navigation
│   ├── index.html     # Home page with entries list
│   ├── add_entry.html # Add new entry form
│   └── edit_entry.html # Edit entry form
└── static/           # Static assets
    ├── css/
    │   └── style.css  # Custom CSS styles
    └── js/
        └── main.js    # JavaScript enhancements
```

## Database Schema

The `data_entries` table includes:

| Column      | Type         | Description                    |
|-------------|--------------|--------------------------------|
| id          | SERIAL       | Primary key (auto-increment)  |
| name        | VARCHAR(255) | Full name (required)           |
| email       | VARCHAR(255) | Email address (optional)       |
| phone       | VARCHAR(50)  | Phone number (optional)        |
| category    | VARCHAR(100) | Entry category (optional)      |
| description | TEXT         | Additional notes (optional)    |
| created_at  | TIMESTAMP    | Created timestamp              |
| updated_at  | TIMESTAMP    | Last updated timestamp         |

## API Endpoints

The application provides RESTful API endpoints:

### GET /api/entries
Get all entries
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1-555-0123",
            "category": "business",
            "description": "Sample business contact",
            "created_at": "2024-01-01T10:00:00",
            "updated_at": "2024-01-01T10:00:00"
        }
    ]
}
```

### POST /api/entries
Create new entry
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-0123",
    "category": "business",
    "description": "Sample business contact"
}
```

### GET /api/entries/{id}
Get single entry by ID

### PUT /api/entries/{id}
Update entry by ID

### DELETE /api/entries/{id}
Delete entry by ID

## Customization

### Adding New Fields

1. **Update the database**: Add new columns to the `data_entries` table
2. **Update models.py**: Add the new fields to the CRUD operations
3. **Update forms.py**: Add form fields with validation
4. **Update templates**: Add the fields to the forms and display views

### Styling Customization

- Edit `static/css/style.css` to customize the appearance
- The CSS uses CSS custom properties (variables) for easy theme customization
- Bootstrap 5 classes can be modified in the templates

### Adding Authentication

To add user authentication:
1. Install Flask-Login: `pip install Flask-Login`
2. Set up Supabase Auth in your Supabase project
3. Add authentication routes and middleware
4. Update the database schema to include user associations

## Deployment

### Railway/Render/Heroku

1. Set environment variables in your deployment platform
2. Ensure `requirements.txt` is up to date
3. Deploy the repository

### Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions:
1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## Changelog

### v1.0.0
- Initial release
- Basic CRUD operations
- Bootstrap UI
- Supabase integration
- RESTful API
- Form validation
- Responsive design
