from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import facade
from datetime import timedelta
from http import HTTPStatus

api = Namespace('auth', description='Authentication operations')

# Modèles pour la validation et la documentation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email address',
                         example='user@example.com'),
    'password': fields.String(required=True, description='User password',
                           example='********')
})

token_response = api.model('TokenResponse', {
    'access_token': fields.String(description='JWT access token'),
    'token_type': fields.String(description='Token type', example='bearer'),
    'expires_in': fields.Integer(description='Token expiration time in seconds')
})

error_response = api.model('ErrorResponse', {
    'error': fields.String(description='Error message'),
    'status_code': fields.Integer(description='HTTP status code')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Success', token_response)
    @api.response(401, 'Authentication failed', error_response)
    @api.response(422, 'Validation Error', error_response)
    def post(self):
        """Authenticate user and return a JWT token"""
        try:
            # Validation des données d'entrée
            if not api.payload:
                return {
                    'error': 'No input data provided',
                    'status_code': HTTPStatus.UNPROCESSABLE_ENTITY
                }, HTTPStatus.UNPROCESSABLE_ENTITY

            email = api.payload.get('email')
            password = api.payload.get('password')

            if not email or not password:
                return {
                    'error': 'Email and password are required',
                    'status_code': HTTPStatus.UNPROCESSABLE_ENTITY
                }, HTTPStatus.UNPROCESSABLE_ENTITY

            # Récupération de l'utilisateur
            user = facade.get_user_by_email(email)
            print(f"Utilisateur récupéré: {user}")
            # Vérification des credentials
            if not user or not user.verify_password(password):
                print(f"Mot de passe incorrect pour l'utilisateur {email}")
                return {
                    'error': 'Invalid credentials',
                    'status_code': HTTPStatus.UNAUTHORIZED
                }, HTTPStatus.UNAUTHORIZED
            print(email)
            print(password)
            # Création du token avec les claims
            token_expires = timedelta(hours=1)
            token_identity = {
                'id': str(user.id),
                'is_admin': user.is_admin
            }

            access_token = create_access_token(
                identity=token_identity,
                expires_delta=token_expires,
                additional_claims={'email': user.email}
            )

            # Retour de la réponse
            return {
                'access_token': access_token,
                'token_type': 'bearer',
                'expires_in': int(token_expires.total_seconds())
            }, HTTPStatus.OK

        except Exception as e:
            api.logger.error(f"Login error: {str(e)}")
            return {
                'error': 'An unexpected error occurred',
                'status_code': HTTPStatus.INTERNAL_SERVER_ERROR
            }, HTTPStatus.INTERNAL_SERVER_ERROR

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        # Récupérer l'identité de l'utilisateur à partir du token JWT
        current_user = get_jwt_identity()

        # Utiliser les informations de l'utilisateur, par exemple :
        user_id = current_user['id']
        is_admin = current_user['is_admin']

        # Retourner une réponse protégée
        return {'message': f'Hello, user {user_id}!'}, 200
