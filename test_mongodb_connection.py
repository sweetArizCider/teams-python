from classes.database.database import mongodb_service

# Test MongoDB connection
try:
    # Test connection
    players_collection = mongodb_service.get_players_collection()
    print("✓ Successfully connected to MongoDB!")
    print(f"✓ Database: {mongodb_service.db.name}")
    print(f"✓ Players collection: {players_collection.name}")

    # Test basic operations
    count = players_collection.count_documents({})
    print(f"✓ Current players in database: {count}")

except Exception as e:
    print(f"✗ Error connecting to MongoDB: {e}")
