class RoleManager:
    available_roles = ['admin','user','GOVTOff']

    def __init__(self):
        for role in self.available_roles:
            if getattr(self,role,None) is None:
                self.__setattr__(role, role)

role_manager = RoleManager()