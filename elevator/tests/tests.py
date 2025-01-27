import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from elevator.database.database import SQLALCHEMY_DATABASE_URL, get_db
from elevator.main import app

client = TestClient(app)

def test_database_connection():
    """
    Test database connection and basic functionality
    """
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    SessionLocal = sessionmaker(bind=engine)
    
    try:
        # Create a session
        session = SessionLocal()
        
        # Verify session is active
        assert session is not None, "Failed to create database session"
        
        # Ensure session can be closed
        session.close()
    
    except Exception as e:
        pytest.fail(f"Database connection failed: {str(e)}")

def test_get_db_context_manager():
    """
    Test the get_db context manager functionality
    """
    # Use the generator function
    db_generator = get_db()
    
    try:
        # Retrieve the database session
        db = next(db_generator)
        
        # Verify the session is not None
        assert db is not None, "Database session from get_db() is None"
        
        # Verify the session can perform basic operations
        # Note: This assumes you have models defined. Adjust as needed.
        # For example: result = db.query(SomeModel).first()
    
    except StopIteration:
        pytest.fail("get_db() generator did not yield a session")
    finally:
        # Ensure the session is closed
        try:
            next(db_generator)
        except StopIteration:
            pass  # This is expected behavior

def test_create_demand():
    """Test POST endpoint for creating an elevator demand"""

    response = client.post(
        "/demand", 
        json={"requestedFloor": 5, "isVacant": False}
    )

    assert response.status_code == 201

def test_invalid_demand():    

    response_basement = client.post(
        "/demand", 
        json={"requestedFloor": -3, "isVacant": False}
    )

    response_above = client.post(
        "/demand", 
        json={"requestedFloor": 23, "isVacant": True}
    )

    assert response_basement.status_code == 400
    assert response_above.status_code == 400

def test_request_demand():
    """Test GET endpoint for retrieving demand data"""
    
    response = client.get(
        "/demand"
    )

    assert response.status_code == 200
    assert "data" in response.json().keys()
    assert isinstance(response.json()["data"], list)
