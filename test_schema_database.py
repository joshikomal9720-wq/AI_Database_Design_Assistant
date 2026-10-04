from src.schema_generator import SchemaGenerator
from src.database_manager import DatabaseManager


# Generate the database schema
generator = SchemaGenerator()
schema = generator.generate_schema()

# Create the database
db = DatabaseManager("database.db")
db.execute_schema(schema)

# Display the tables
db.show_tables()

print("\nSchema-to-database test completed.")