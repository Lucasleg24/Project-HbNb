from flask import Flask
from flask_restx import Api
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns

def create_app(config_class="config.DevelopmentConfig"):
    # Création de l'application Flask
    app = Flask(__name__)

    # Chargement de la configuration à partir de l'objet de configuration
    app.config.from_object(config_class)

    # Initialisation de l'API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API'
    )

    # Ajout des namespaces pour les différents modules
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")

    return app
