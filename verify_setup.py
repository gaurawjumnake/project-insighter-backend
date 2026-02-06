"""
Verification script to test database models and schemas.
Run this script to verify that all models and schemas are correctly set up.
"""

def test_imports():
    """Test that all models and schemas can be imported without errors."""
    print("Testing imports...")
    
    try:
        # Test model imports
        print("\n1. Testing model imports...")
        from backend.app.models import (
            Account, Circle, Project, Stakeholder, StakeholderConnection,
            AccountCircleCoverage, AISuggestion, ValueChainMetric, Opportunity
        )
        print("✓ All models imported successfully!")
        
        # Test schema imports
        print("\n2. Testing schema imports...")
        from backend.app.schemas import (
            AccountCreate, AccountResponse,
            CircleCreate, CircleResponse,
            ProjectCreate, ProjectResponse,
            StakeholderCreate, StakeholderResponse,
            StakeholderConnectionCreate, StakeholderConnectionResponse,
            AccountCircleCoverageCreate, AccountCircleCoverageResponse,
            AISuggestionCreate, AISuggestionResponse,
            ValueChainMetricCreate, ValueChainMetricResponse,
            OpportunityCreate, OpportunityResponse,
        )
        print("✓ All schemas imported successfully!")
        
        # Test database session
        print("\n3. Testing database session setup...")
        from backend.app.db import Base, get_db, engine
        print("✓ Database session setup imported successfully!")
        
        # Test config
        print("\n4. Testing configuration...")
        from backend.app.core.config import settings
        print(f"✓ Configuration loaded successfully!")
        print(f"  Database URL: {settings.DATABASE_URL[:50]}...")
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n✗ Error during import: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database_connection():
    """Test database connection."""
    print("\n\n5. Testing database connection...")
    try:
        from backend.app.db.session import test_connection
        test_connection()
        print("✓ Database connection test completed!")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("Note: Make sure your .env file has correct database credentials.")
        return False


def create_all_tables():
    """Create all database tables."""
    print("\n\n6. Creating database tables...")
    try:
        from backend.app.db.session import create_tables
        create_tables()
        print("✓ All tables created successfully!")
        return True
    except Exception as e:
        print(f"✗ Table creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("="*60)
    print("DATABASE SETUP VERIFICATION")
    print("="*60)
    
    # Run import tests
    imports_ok = test_imports()
    
    if imports_ok:
        # Test database connection
        connection_ok = test_database_connection()
        
        if connection_ok:
            # Ask user if they want to create tables
            print("\n" + "="*60)
            response = input("Do you want to create all tables in the database? (yes/no): ")
            if response.lower() in ['yes', 'y']:
                create_all_tables()
            else:
                print("Skipping table creation.")
    
    print("\n" + "="*60)
    print("VERIFICATION COMPLETE")
    print("="*60)
