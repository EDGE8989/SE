import re
from datetime import date

def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password):
    """Validate password strength."""
    if len(password) < 8:
        return False, 'Password must be at least 8 characters.'
    if not re.search(r'[A-Z]', password):
        return False, 'Password must contain at least one uppercase letter.'
    if not re.search(r'[0-9]', password):
        return False, 'Password must contain at least one number.'
    return True, ''

def validate_required(fields):
    """Check that all required fields are non-empty."""
    missing = [name for name, value in fields.items() if not value or not str(value).strip()]
    return missing

def validate_url(url):
    """Basic URL validation."""
    if not url:
        return True  # Optional URLs are fine
    pattern = r'^https?://[^\s]+$'
    return bool(re.match(pattern, url))

def validate_future_date(d):
    """Check that a date is not in the past."""
    if not d:
        return True
    if isinstance(d, str):
        try:
            d = date.fromisoformat(d)
        except ValueError:
            return False
    return d >= date.today()
