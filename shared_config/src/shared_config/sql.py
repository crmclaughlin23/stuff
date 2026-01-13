# config.py

# Import libraries
import os

# ---------------------------------------
# ENVIRONMENT CONFIGURATION
# ---------------------------------------
# Set default server environment
ENV = os.getenv('ENG', 'development').lower()

# ---------------------------------------
# SQL SERVER AND DATABASE NAMES
# ---------------------------------------
# SQL server environment names
DEV_SERVER = 'UT02SQLDEVAGL'
QUAL_SERVER = 'UT02SQLQUALAGL'
PROD_SERVER = 'UT02SQLPRODAGL'

# Central pyrometry server
PYRO_SERVER = 'c30-ywvdb81200.northgrum.com'

# Local server
LOCAL_SERVER = 'localhost'

# SQL database names
PYRO_DATABASE = 'Pyrometry'
LOCAL_DATABASE = 'Local_Database'

# ---------------------------------------
# ACTIVE SERVER BASED ON ENV
# ---------------------------------------
if ENV == 'development':
    ACTIVE_SERVER = DEV_SERVER
elif ENV == 'quality':
    ACTIVE_SERVER = QUAL_SERVER
elif ENV == 'production':
    ACTIVE_SERVER = PROD_SERVER
elif ENV == 'local':
    ACTIVE_SERVER = LOCAL_SERVER
else:
    raise ValueError(f'Invalid ENV setting: {ENV}')

# ---------------------------------------
# Environment dictionary
# ---------------------------------------
ENVIRONMENTS = {
    'development': DEV_SERVER,
    'quality': QUAL_SERVER,
    'production': PROD_SERVER,
    'local': LOCAL_SERVER
}