#!/usr/bin/env python3
"""
Simple runner script for the Data Entry System
This can be used for production deployment with gunicorn or similar WSGI servers
"""

from app import app

if __name__ == '__main__':
    # For development
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # For production (when imported by WSGI server)
    application = app