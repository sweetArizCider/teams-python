from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.database import Database
from pymongo.collection import Collection
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class MongoDBService:
    def __init__(self):
        self.client = None
        self.database = None
        self._connect()

    def _connect(self):
        """Establish connection to MongoDB"""
        try:
            # Format the MongoDB URI with credentials
            uri = settings.mongodb_uri.replace("<db_username>", settings.mongodb_username).replace("<db_password>", settings.mongodb_password)

            self.client = MongoClient(
                uri,
                server_api=ServerApi('1')
            )

            # Test the connection
            self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB!")

            # Get the database
            self.database = self.client[settings.mongodb_database]

        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {str(e)}")
            raise e

    def get_database(self) -> Database:
        """Get the MongoDB database instance"""
        if self.database is None:
            self._connect()
        return self.database

    def get_players_collection(self) -> Collection:
        """Get the players collection"""
        return self.get_database()["players"]

    def get_teams_collection(self) -> Collection:
        """Get the teams collection"""
        return self.get_database()["teams"]

    def get_players_team_collection(self) -> Collection:
        """Get the players_team collection"""
        return self.get_database()["players_team"]

    def close_connection(self):
        """Close the MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

# Create a global instance
mongodb_service = MongoDBService()
