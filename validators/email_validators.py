from aiogram import types

from email_validator import validate_email, EmailNotValidError

# def valid_email(text: str) -> str:
#     if "@" not in text or "." not in text:
#         raise ValueError("Invalid email")
#     return text.lower()
#

# функция для переиспользования валидатора
# def valid_email_filter(message: types.Message) -> dict[str, str] | None:
#     try:
#         return {"email": valid_email(message.text)}
#     except ValueError:
#         return None

def valid_email_filter(message: types.Message) -> dict[str, str] | None:
    try:
        email = validate_email(message.text)
    except EmailNotValidError:
        return None

    return {"email": email.normalized.lower()}
