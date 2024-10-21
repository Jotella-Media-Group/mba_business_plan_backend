from core.service import CoreService
from core.service import EmailService


class SERVICE_NAMES:
    CoreService = "core_service"


class ServiceLocator:
    service = {}

    core_service: CoreService

    def __init__(self):
        self._services = {}

    def register(self, name, service):
        self._services[name] = service

    def get(self, name):
        return self._services[name]

    def __getitem__(self, name):
        return self.get(name)

    def __getattr__(self, name):
        return self.get(name)


#  register services


service_locator = ServiceLocator()

email_service = EmailService()
service_locator.register(SERVICE_NAMES.CoreService, CoreService())
