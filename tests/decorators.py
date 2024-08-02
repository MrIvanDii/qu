# decorators.py
import logging
import sqlite3


def handle_db_errors(func):
    """
    Декоратор для обработки ошибок базы данных и других исключений.

    Args:
        func (callable): Функция, к которой применяется декоратор.

    Returns:
        callable: Обернутая функция с обработкой ошибок.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            logging.error(f"Database error in {func.__name__}: {e}")
        except Exception as e:
            logging.error(f"Exception in {func.__name__}: {e}")

    return wrapper
