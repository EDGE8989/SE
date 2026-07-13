import sys
import os

# Add iems directory to the path so python can import files from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'iems'))

from app import create_app

# Create flask app instance for Vercel Serverless
app = create_app('production')
