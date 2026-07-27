# When someone "import app.models", all of the modules in __init__.py will be executed.
from app.models.user import User

__all__ = ["User"]