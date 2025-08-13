


"""
Test that the storage purchase endpoint can be imported correctly
"""

import sys
import os
import inspect

# Add the web_server directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'web_server')))

def test_endpoint_exists():
    """Test that the purchase_storage function exists and has the right signature"""

    try:
        # Import the document routes module
        from api_gateway.document_routes import purchase_storage

        print("✓ Successfully imported purchase_storage function")

        # Check that it's a function
        if not callable(purchase_storage):
            print("ERROR: purchase_storage is not callable")
            return False

        print("✓ purchase_storage is callable")

        # Get the function signature
        sig = inspect.signature(purchase_storage)
        params = list(sig.parameters.keys())

        expected_params = ['current_user', 'current_email', 'current_role']

        print(f"Function parameters: {params}")
        print(f"Expected parameters: {expected_params}")

        if params == expected_params:
            print("✓ Function has the correct parameters")
        else:
            print("ERROR: Function parameters don't match expected")
            return False

        return True

    except ImportError as e:
        print(f"ERROR: Failed to import purchase_storage: {str(e)}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error: {str(e)}")
        return False

def test_route_registration():
    """Test that the route is properly registered"""

    try:
        # Import the gateway blueprint
        from api_gateway.gateway import api_gateway_bp

        print("✓ Successfully imported api_gateway_bp")

        # Check if the route exists
        route_exists = False
        for rule in api_gateway_bp.url_map.iter_rules():
            if '/api/v1/storage/purchase' in str(rule):
                route_exists = True
                print(f"✓ Found route: {rule}")
                break

        if not route_exists:
            print("ERROR: Storage purchase route not found in blueprint")
            return False

        return True

    except ImportError as e:
        print(f"ERROR: Failed to import api_gateway_bp: {str(e)}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error checking route: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing storage purchase endpoint import...\n")

    test1 = test_endpoint_exists()
    print()
    test2 = test_route_registration()

    print(f"\nOverall test result: {'PASSED' if test1 and test2 else 'FAILED'}")


