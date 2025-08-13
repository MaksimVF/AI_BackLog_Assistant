




"""
Test importing the document_routes module
"""

try:
    print("Testing import of document_routes...")
    from web_server.api_gateway import document_routes
    print("✓ Successfully imported document_routes")
except Exception as e:
    print(f"✗ Failed to import document_routes: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nTesting import of api_security...")
    from security import api_security
    print("✓ Successfully imported api_security")
except Exception as e:
    print(f"✗ Failed to import api_security: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nTesting import of BaseModel...")
    from pydantic import BaseModel
    print("✓ Successfully imported BaseModel")
except Exception as e:
    print(f"✗ Failed to import BaseModel: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nTesting import of auth_middleware...")
    from web_server.api_gateway import auth_middleware
    print("✓ Successfully imported auth_middleware")
except Exception as e:
    print(f"✗ Failed to import auth_middleware: {e}")
    import traceback
    traceback.print_exc()



