from services import config


class KeycloakConfig:
    def __init__(self):
        self.client_id = config.KEYCLOAK_CLIENT_ID
        self.client_secret = config.KEYCLOAK_CLIENT_SECRET
        self.realm = config.KEYCLOAK_REALM
        self.url = config.KEYCLOAK_URL

    @property
    def certs_url(self) -> str:
        return f"{self.realm_url}/protocol/openid-connect/certs"

    @property
    def realm_url(self) -> str:
        return f"{self.url}/realms/{self.realm}"

    @property
    def token_url(self) -> str:
        return f"{self.realm_url}/protocol/openid-connect/token"


keycloak_config = KeycloakConfig()
