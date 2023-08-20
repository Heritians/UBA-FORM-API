from API.models import *

from typing import Any

class DBFieldManager:
    """
    This class is used to manage the fields of the forms.
    """
    forms = [FormData]
    def __init__(self):
        self.form_fields = {cls.__name__:cls.__annotations__.keys() for cls in self.forms}

    def get_form_fields(self, form_name: Any, exclude: list = None, include: list = None):
        """
        Get the fields of the form.

        Args:
            form_name (Any): name of the form
            exclude (list, optional): fields to exclude. Defaults to None.
            include (list, optional): fields to include. Defaults to None.
        """
        form_name = form_name.__name__ if isinstance(form_name, type) else form_name
        if exclude is not None and include is not None:
            raise AttributeError("Cannot use both exclude and include together.")
        
        if exclude is not None:
            return [field for field in self.form_fields[form_name] if field not in exclude]
        
        if include is not None:
            return [field for field in self.form_fields[form_name] if field in include]
        
        return self.form_fields[form_name]
    
field_manager = DBFieldManager()