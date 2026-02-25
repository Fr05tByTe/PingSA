class AppError(Exception):
    user_message = "Sorry, something went wrong."


class ValidationAppError(AppError):
    user_message = "That input looks invalid."
