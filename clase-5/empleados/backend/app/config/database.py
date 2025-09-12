import os
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mongodb")

# Cliente de MongoDB
client = None

def connect_to_mongo():
    """
    Establece la conexión con la base de datos MongoDB.
    """
    try:
        global client
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/userdb")

        logger.info("Intentando conectar a MongoDB...")
        client = MongoClient(mongo_uri)

        # Verificar la conexión
        client.admin.command('ping')

        logger.info("Conectado a MongoDB exitosamente")
        return client
    except ConnectionFailure as e:
        logger.error(f"Error al conectar a MongoDB: {str(e)}")
        raise

def\
        get_database():
    """
    Retorna la instancia de la base de datos.
    """
    if client is None:
        connect_to_mongo()

    db_name = os.getenv("MONGODB_DATABASE", "userdb")
    return client[db_name]

def get_collection(collection_name):
    """
    Retorna una colección específica de la base de datos.
    """
    db = get_database()
    return db[collection_name]

# Establecer la conexión al importar el módulo
connect_to_mongo()
