from aiogram import types


def valid_email(text: str) -> str:
    if "@" not in text or "." not in text:
        raise ValueError("Invalid email")
    return text.lower()


# функция для переиспользования валидатора
# def valid_email_filter(message: types.Message) -> dict[str, str] | None:
#     try:
#         return {"email": valid_email(message.text)}
#     except ValueError:
#         return None

def valid_email_filter(message: types.Message) -> dict[str, str] | None:
    try:
        email = valid_email(message.text)
    except ValueError:
        return None

    return {"email": email}
