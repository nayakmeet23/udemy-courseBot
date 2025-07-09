#!/usr/bin/env python3
"""
Script to drop and recreate database tables
"""

from udemypy.database import database
from udemypy.database import script


def reset_database():
    """Drop and recreate all database tables"""
    print("[Database] Connecting to database...")
    db = database.connect()
    
    print("[Database] Dropping existing tables...")
    # Drop tables (in correct order due to foreign keys)
    drop_script = script.read_script(script.get_path("drop_tables.sql"))
    db.execute_script(drop_script, commit=True)
    print("[Database] Tables dropped successfully")
    
    print("[Database] Creating new tables...")
    # Create tables
    create_script = script.read_script(script.get_path("create_tables.sql"))
    db.execute_script(create_script, commit=True)
    print("[Database] Tables created successfully")
    
    print("[Database] Setting up default data...")
    # Setup default data (social media platforms)
    setup_script = script.read_script(script.get_path("setup_tables.sql"))
    db.execute_script(setup_script, commit=True)
    print("[Database] Default data inserted successfully")
    
    print("[Database] Database reset completed successfully!")
    db.close()


if __name__ == "__main__":
    reset_database() 