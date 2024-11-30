INSTALLED_APPS = [
    ...,
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...,
]

# Configuración de CORS
CORS_ALLOW_ALL_ORIGINS = True  # Permite todas las solicitudes