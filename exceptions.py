class ImproperlyConfiguredApp(Exception):
    """XMLApp is somehow improperly configured"""
    pass

class NoProvider(Exception):
    """No Provider passed in query params"""
    def __str__(self) -> str:
        return "No Provider passed in query params"

class ProviderNotFound(Exception):
    def __init__(self, provider):
        self.provider = provider
        super().__init__(f"Provider '{provider}' not found in config.ini")
    
class InvalidDestination(Exception):
    def __init__(self, source_url):
        self.source_url = source_url
        super().__init__(f"Invalid Destination URL: {source_url}")

class CannotDownloadXML(Exception):
    def __init__(self, source_url):
        self.source_url = source_url
        super().__init__(f"Cannot download XML file from {source_url}")