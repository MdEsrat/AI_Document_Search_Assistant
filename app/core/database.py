"""
MongoDB database connection and management
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class MongoDB:
    """MongoDB connection manager"""
    
    def __init__(self):
        self.client = None
        self.db = None
    
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
            self.db = self.client[settings.DATABASE_NAME]
            # Verify connection
            await self.client.admin.command('ping')
            logger.info(f"Connected to MongoDB: {settings.DATABASE_NAME}")
        except Exception as e:
            logger.warning(f"MongoDB connection failed: {e}. The application will continue without MongoDB.")
            # Don't raise - allow app to start without MongoDB
            self.client = None
            self.db = None
    
    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
    
    def get_collection(self, collection_name: str):
        """Get a collection from the database"""
        if self.db is None:
            logger.warning(f"MongoDB not connected. Cannot get collection: {collection_name}")
            return None
        return self.db[collection_name]


# Global MongoDB instance
mongodb = MongoDB()


async def get_database():
    """Dependency to get database instance"""
    return mongodb.db
