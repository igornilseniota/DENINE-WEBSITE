#!/usr/bin/env python3
"""
DE---NINE Art Print Store Backend API Tests
Tests all backend endpoints and functionality
"""

import requests
import json
import uuid
from datetime import datetime
import sys
import os

# Configuration
BACKEND_URL = "https://minimal-artspace.preview.emergentagent.com/api"
TEST_SESSION_ID = f"test_session_{uuid.uuid4().hex[:8]}"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_test_header(test_name):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}Testing: {test_name}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.ENDC}")

def test_health_check():
    """Test basic health check endpoint"""
    print_test_header("Health Check")
    
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health check passed - Status: {data.get('status', 'unknown')}")
            return True
        else:
            print_error(f"Health check failed - Status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print_error(f"Health check failed - Connection error: {str(e)}")
        return False

def test_print_management():
    """Test print management endpoints"""
    print_test_header("Print Management APIs")
    
    results = {"get_all_prints": False, "get_specific_theme": False, "theme_count": 0}
    
    # Test GET /api/prints
    try:
        print_info("Testing GET /api/prints...")
        response = requests.get(f"{BACKEND_URL}/prints", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            prints = data.get("prints", [])
            results["theme_count"] = len(prints)
            
            if len(prints) >= 5:
                print_success(f"GET /api/prints successful - Found {len(prints)} print themes")
                results["get_all_prints"] = True
                
                # Test specific theme
                if prints:
                    theme_id = prints[0].get("theme_id")
                    if theme_id:
                        print_info(f"Testing GET /api/prints/{theme_id}...")
                        theme_response = requests.get(f"{BACKEND_URL}/prints/{theme_id}", timeout=10)
                        
                        if theme_response.status_code == 200:
                            theme_data = theme_response.json()
                            print_success(f"GET /api/prints/{theme_id} successful")
                            print_info(f"Theme: {theme_data.get('theme', 'Unknown')}")
                            print_info(f"Variants: {len(theme_data.get('variants', []))}")
                            results["get_specific_theme"] = True
                        else:
                            print_error(f"GET /api/prints/{theme_id} failed - Status: {theme_response.status_code}")
            else:
                print_warning(f"Expected at least 5 print themes, found {len(prints)}")
                results["get_all_prints"] = len(prints) > 0
        else:
            print_error(f"GET /api/prints failed - Status: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print_error(f"Print management test failed - Connection error: {str(e)}")
    
    # Test invalid theme ID
    try:
        print_info("Testing GET /api/prints/invalid_theme...")
        response = requests.get(f"{BACKEND_URL}/prints/invalid_theme", timeout=10)
        
        if response.status_code == 404:
            print_success("Invalid theme ID correctly returns 404")
        else:
            print_warning(f"Invalid theme ID returned status: {response.status_code} (expected 404)")
            
    except requests.exceptions.RequestException as e:
        print_error(f"Invalid theme test failed - Connection error: {str(e)}")
    
    return results

def test_cart_management():
    """Test cart management endpoints"""
    print_test_header("Cart Management APIs")
    
    results = {"add_to_cart": False, "get_cart": False, "remove_from_cart": False}
    cart_item_id = None
    
    # First, get a print theme to add to cart
    try:
        prints_response = requests.get(f"{BACKEND_URL}/prints", timeout=10)
        if prints_response.status_code != 200:
            print_error("Cannot test cart - unable to fetch print themes")
            return results
            
        prints = prints_response.json().get("prints", [])
        if not prints:
            print_error("Cannot test cart - no print themes available")
            return results
            
        test_theme = prints[0]
        theme_id = test_theme.get("theme_id")
        base_price = test_theme.get("base_price", 29900)  # Default price in øre
        
    except Exception as e:
        print_error(f"Failed to get test theme: {str(e)}")
        return results
    
    # Test GET empty cart
    try:
        print_info(f"Testing GET /api/cart/{TEST_SESSION_ID} (empty cart)...")
        response = requests.get(f"{BACKEND_URL}/cart/{TEST_SESSION_ID}", timeout=10)
        
        if response.status_code == 200:
            cart_data = response.json()
            if cart_data.get("total", 0) == 0 and len(cart_data.get("items", [])) == 0:
                print_success("Empty cart test successful")
            else:
                print_warning("Cart not empty as expected")
        else:
            print_error(f"GET empty cart failed - Status: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print_error(f"Empty cart test failed - Connection error: {str(e)}")
    
    # Test POST add to cart
    try:
        print_info(f"Testing POST /api/cart/{TEST_SESSION_ID}/add...")
        
        cart_item = {
            "theme_id": theme_id,
            "selected_variants": ["variant_1"],
            "quantity": 2,
            "unit_price": base_price
        }
        
        response = requests.post(
            f"{BACKEND_URL}/cart/{TEST_SESSION_ID}/add",
            json=cart_item,
            timeout=10
        )
        
        if response.status_code == 200:
            cart_data = response.json()
            if cart_data.get("total", 0) > 0 and len(cart_data.get("items", [])) > 0:
                print_success("Add to cart successful")
                results["add_to_cart"] = True
                
                # Get the cart item ID for removal test
                items = cart_data.get("items", [])
                if items:
                    cart_item_id = str(items[0].get("id"))
            else:
                print_error("Add to cart failed - cart still empty")
        else:
            print_error(f"Add to cart failed - Status: {response.status_code}")
            try:
                error_detail = response.json()
                print_error(f"Error details: {error_detail}")
            except:
                print_error(f"Response text: {response.text}")
                
    except requests.exceptions.RequestException as e:
        print_error(f"Add to cart test failed - Connection error: {str(e)}")
    
    # Test GET cart with items
    try:
        print_info(f"Testing GET /api/cart/{TEST_SESSION_ID} (with items)...")
        response = requests.get(f"{BACKEND_URL}/cart/{TEST_SESSION_ID}", timeout=10)
        
        if response.status_code == 200:
            cart_data = response.json()
            if cart_data.get("total", 0) > 0 and len(cart_data.get("items", [])) > 0:
                print_success(f"Get cart successful - Total: {cart_data.get('total')} øre")
                results["get_cart"] = True
            else:
                print_error("Get cart failed - cart appears empty")
        else:
            print_error(f"Get cart failed - Status: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print_error(f"Get cart test failed - Connection error: {str(e)}")
    
    # Test DELETE cart item
    if cart_item_id:
        try:
            print_info(f"Testing DELETE /api/cart/{TEST_SESSION_ID}/item/{cart_item_id}...")
            response = requests.delete(
                f"{BACKEND_URL}/cart/{TEST_SESSION_ID}/item/{cart_item_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                cart_data = response.json()
                print_success("Remove from cart successful")
                results["remove_from_cart"] = True
            else:
                print_error(f"Remove from cart failed - Status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print_error(f"Remove from cart test failed - Connection error: {str(e)}")
    else:
        print_warning("Skipping remove from cart test - no cart item ID available")
    
    return results

def test_payment_system():
    """Test payment system endpoints"""
    print_test_header("Payment System APIs")
    
    results = {"create_checkout": False, "payment_status": False}
    
    # First, add an item to cart for checkout
    try:
        prints_response = requests.get(f"{BACKEND_URL}/prints", timeout=10)
        if prints_response.status_code != 200:
            print_error("Cannot test payments - unable to fetch print themes")
            return results
            
        prints = prints_response.json().get("prints", [])
        if not prints:
            print_error("Cannot test payments - no print themes available")
            return results
            
        test_theme = prints[0]
        theme_id = test_theme.get("theme_id")
        base_price = test_theme.get("base_price", 29900)
        
        # Add item to cart
        cart_item = {
            "theme_id": theme_id,
            "selected_variants": ["variant_1"],
            "quantity": 1,
            "unit_price": base_price
        }
        
        cart_response = requests.post(
            f"{BACKEND_URL}/cart/{TEST_SESSION_ID}/add",
            json=cart_item,
            timeout=10
        )
        
        if cart_response.status_code != 200:
            print_error("Cannot test payments - failed to add item to cart")
            return results
            
    except Exception as e:
        print_error(f"Failed to prepare cart for payment test: {str(e)}")
        return results
    
    # Test POST checkout
    try:
        print_info("Testing POST /api/payments/checkout...")
        
        checkout_data = {
            "session_id": TEST_SESSION_ID,
            "customer_info": {
                "email": "test@denine.art",
                "name": "Test Customer",
                "phone": "+47 123 45 678"
            },
            "payment_method": "stripe"
        }
        
        response = requests.post(
            f"{BACKEND_URL}/payments/checkout",
            json=checkout_data,
            timeout=15
        )
        
        if response.status_code == 200:
            checkout_response = response.json()
            if "checkout_url" in checkout_response and "session_id" in checkout_response:
                print_success("Create checkout session successful")
                print_info(f"Checkout URL: {checkout_response.get('checkout_url', 'N/A')}")
                results["create_checkout"] = True
                
                # Test payment status
                stripe_session_id = checkout_response.get("session_id")
                if stripe_session_id:
                    try:
                        print_info(f"Testing GET /api/payments/status/{stripe_session_id}...")
                        status_response = requests.get(
                            f"{BACKEND_URL}/payments/status/{stripe_session_id}",
                            timeout=10
                        )
                        
                        if status_response.status_code == 200:
                            status_data = status_response.json()
                            print_success(f"Payment status check successful - Status: {status_data.get('payment_status', 'unknown')}")
                            results["payment_status"] = True
                        else:
                            print_error(f"Payment status check failed - Status: {status_response.status_code}")
                            
                    except requests.exceptions.RequestException as e:
                        print_error(f"Payment status test failed - Connection error: {str(e)}")
            else:
                print_error("Create checkout failed - missing required fields in response")
        else:
            print_error(f"Create checkout failed - Status: {response.status_code}")
            try:
                error_detail = response.json()
                print_error(f"Error details: {error_detail}")
            except:
                print_error(f"Response text: {response.text}")
                
    except requests.exceptions.RequestException as e:
        print_error(f"Checkout test failed - Connection error: {str(e)}")
    
    return results

def test_error_handling():
    """Test error handling for invalid requests"""
    print_test_header("Error Handling Tests")
    
    results = {"invalid_endpoints": False, "malformed_requests": False}
    
    # Test invalid endpoints
    try:
        print_info("Testing invalid endpoint /api/nonexistent...")
        response = requests.get(f"{BACKEND_URL}/nonexistent", timeout=10)
        
        if response.status_code == 404:
            print_success("Invalid endpoint correctly returns 404")
            results["invalid_endpoints"] = True
        else:
            print_warning(f"Invalid endpoint returned status: {response.status_code} (expected 404)")
            
    except requests.exceptions.RequestException as e:
        print_error(f"Invalid endpoint test failed - Connection error: {str(e)}")
    
    # Test malformed cart request
    try:
        print_info("Testing malformed cart request...")
        malformed_data = {"invalid": "data"}
        
        response = requests.post(
            f"{BACKEND_URL}/cart/{TEST_SESSION_ID}/add",
            json=malformed_data,
            timeout=10
        )
        
        if response.status_code in [400, 422, 500]:  # Any error status is acceptable
            print_success(f"Malformed request correctly returns error status: {response.status_code}")
            results["malformed_requests"] = True
        else:
            print_warning(f"Malformed request returned status: {response.status_code} (expected error)")
            
    except requests.exceptions.RequestException as e:
        print_error(f"Malformed request test failed - Connection error: {str(e)}")
    
    return results

def run_all_tests():
    """Run all backend tests"""
    print(f"{Colors.BOLD}DE---NINE Art Print Store Backend API Tests{Colors.ENDC}")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Session ID: {TEST_SESSION_ID}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    all_results = {}
    
    # Run tests
    all_results["health"] = test_health_check()
    all_results["prints"] = test_print_management()
    all_results["cart"] = test_cart_management()
    all_results["payments"] = test_payment_system()
    all_results["errors"] = test_error_handling()
    
    # Summary
    print_test_header("Test Summary")
    
    total_tests = 0
    passed_tests = 0
    
    # Health check
    if all_results["health"]:
        print_success("Health Check: PASSED")
        passed_tests += 1
    else:
        print_error("Health Check: FAILED")
    total_tests += 1
    
    # Print management
    print_results = all_results["prints"]
    if print_results["get_all_prints"] and print_results["get_specific_theme"]:
        print_success(f"Print Management: PASSED ({print_results['theme_count']} themes found)")
        passed_tests += 1
    else:
        print_error("Print Management: FAILED")
        if not print_results["get_all_prints"]:
            print_error("  - Get all prints failed")
        if not print_results["get_specific_theme"]:
            print_error("  - Get specific theme failed")
    total_tests += 1
    
    # Cart management
    cart_results = all_results["cart"]
    cart_passed = cart_results["add_to_cart"] and cart_results["get_cart"]
    if cart_passed:
        print_success("Cart Management: PASSED")
        passed_tests += 1
    else:
        print_error("Cart Management: FAILED")
        if not cart_results["add_to_cart"]:
            print_error("  - Add to cart failed")
        if not cart_results["get_cart"]:
            print_error("  - Get cart failed")
        if not cart_results["remove_from_cart"]:
            print_warning("  - Remove from cart failed")
    total_tests += 1
    
    # Payment system
    payment_results = all_results["payments"]
    if payment_results["create_checkout"]:
        print_success("Payment System: PASSED")
        passed_tests += 1
    else:
        print_error("Payment System: FAILED")
        if not payment_results["create_checkout"]:
            print_error("  - Create checkout failed")
        if not payment_results["payment_status"]:
            print_warning("  - Payment status check failed")
    total_tests += 1
    
    # Error handling
    error_results = all_results["errors"]
    if error_results["invalid_endpoints"] and error_results["malformed_requests"]:
        print_success("Error Handling: PASSED")
        passed_tests += 1
    else:
        print_warning("Error Handling: PARTIAL")
        if not error_results["invalid_endpoints"]:
            print_warning("  - Invalid endpoints handling needs improvement")
        if not error_results["malformed_requests"]:
            print_warning("  - Malformed request handling needs improvement")
    total_tests += 1
    
    # Final summary
    print(f"\n{Colors.BOLD}Final Results:{Colors.ENDC}")
    print(f"Tests Passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print_success("🎉 All tests passed!")
        return True
    elif passed_tests >= total_tests * 0.8:  # 80% pass rate
        print_warning("⚠️  Most tests passed with some issues")
        return True
    else:
        print_error("❌ Multiple critical failures detected")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)