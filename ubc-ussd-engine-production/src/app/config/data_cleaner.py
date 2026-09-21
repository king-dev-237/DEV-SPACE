import re
from typing import Any, Optional


def clean_email(email: str) -> Optional[str]:
    """
    Validate and clean email addresses.

    Args:
        email: Email string to clean

    Returns:
        Cleaned email or None if invalid
    """
    if not isinstance(email, str):
        return None

    email = email.strip().lower()
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    return email if re.match(pattern, email) else None


def clean_phone_number(phone: str) -> Optional[str]:
    """
    Extract and validate phone numbers, removing non-digit characters.

    Args:
        phone: Phone number string to clean

    Returns:
        Cleaned phone number (digits only) or None if invalid
    """
    if not isinstance(phone, str):
        return None

    digits = re.sub(r'\D', '', phone)

    return digits if 10 <= len(digits) <= 15 else None


def prevent_sql_injection(value: str) -> str:
    """
    Sanitize input to prevent SQL injection by escaping dangerous characters.

    Args:
        value: String value to sanitize

    Returns:
        Sanitized string with escaped characters
    """
    if not isinstance(value, str):
        return str(value)

    dangerous_chars = {
        "'": "''",
        '"': '""',
        ";": "",
        "--": "",
        "/*": "",
        "*/": "",}

    sanitized = value
    for char, replacement in dangerous_chars.items():
        sanitized = sanitized.replace(char, replacement)

    return sanitized.strip()


def clean_username(username: str) -> Optional[str]:
    """
    Clean and validate usernames.
    Allows alphanumeric characters, underscores, and hyphens.

    Args:
        username: Username string to clean

    Returns:
        Cleaned username or None if invalid
    """
    if not isinstance(username, str):
        return None

    username = username.strip()
    pattern = r'^[a-zA-Z0-9_-]{3,32}$'

    return username if re.match(pattern, username) else None


def clean_url(url: str) -> Optional[str]:
    """
    Validate and clean URLs.

    Args:
        url: URL string to clean

    Returns:
        Cleaned URL or None if invalid
    """
    if not isinstance(url, str):
        return None

    url = url.strip()
    pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?$'

    return url if re.match(pattern, url) else None


def clean_text(text: str, remove_special: bool = False) -> str:
    """
    Clean text by removing extra whitespace and optionally special characters.

    Args:
        text: Text string to clean
        remove_special: If True, removes special characters

    Returns:
        Cleaned text
    """
    if not isinstance(text, str):
        return ""

    text = text.strip()
    text = re.sub(r'\s+', ' ', text)

    if remove_special:
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    return text


def clean_integer(value: Any) -> Optional[int]:
    """
    Convert and validate integer values.

    Args:
        value: Value to convert to integer

    Returns:
        Integer value or None if conversion fails
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def clean_float(value: Any) -> Optional[float]:
    """
    Convert and validate float values.

    Args:
        value: Value to convert to float

    Returns:
        Float value or None if conversion fails
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return None