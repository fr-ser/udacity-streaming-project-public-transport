import time
from functools import wraps


def wait_until_or_crash(timeout=30, caught_exception=None):
    """
    A decorator to wait until a function suceeds and returns true in time.
    Otherwhise an error is raised.

    This should be used to wait for dependencies (e.g. check until a database is up)

    :param timeout: Maximum wait time in seconds (Does not interrupt blocking code!)
    :param caught_exception: Exception to catch (and retry)
    """
    def argumentless_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            result = None
            stored_exception = None
            end_time = time.time() + timeout
            while time.time() < end_time:
                try:
                    result = fn(*args, **kwargs)
                    stored_exception = None
                except Exception as e:
                    if caught_exception is None or not isinstance(e, caught_exception):
                        raise

                    stored_exception = e
                    time.sleep(0.3)
                    continue

                if result:
                    return
                else:
                    time.sleep(0.3)
                    continue

            if not result:
                if stored_exception:
                    raise stored_exception
                else:
                    raise Exception("Dependency not ready")

        return wrapper
    return argumentless_decorator
