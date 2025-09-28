#!/usr/bin/env python3
"""
Main test runner for Kairos AI.
Runs all test suites and provides a summary.
"""
import sys
import os

# Add tests directory to path
sys.path.insert(0, os.path.dirname(__file__))

def run_test_suite(suite_name, test_module):
    """Run a test suite and return results."""
    print(f"\n🧪 {suite_name}")
    print("=" * (len(suite_name) + 4))
    
    try:
        # Import and run the test module
        result = test_module.run_tests()
        total_tests = len([attr for attr in dir(test_module) if attr.startswith('test_')])
        
        print(f"\n📊 {result}/{total_tests} tests passed")
        return result, total_tests
    except Exception as e:
        print(f"❌ Error running {suite_name}: {e}")
        return 0, 1

def main():
    """Run all test suites."""
    print("🧪 Kairos AI - Complete Test Suite")
    print("=" * 40)
    
    # Import test modules
    try:
        import test_core
        import test_data
        import test_config
    except ImportError as e:
        print(f"❌ Failed to import test modules: {e}")
        return 1
    
    # Run all test suites
    suites = [
        ("Core Tests", test_core),
        ("Data Tests", test_data),
        ("Configuration Tests", test_config)
    ]
    
    total_passed = 0
    total_tests = 0
    
    for suite_name, test_module in suites:
        passed, total = run_test_suite(suite_name, test_module)
        total_passed += passed
        total_tests += total
    
    # Final summary
    print("\n" + "=" * 40)
    print(f"📊 OVERALL: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed - check output above")
        return 1

if __name__ == "__main__":
    exit(main())
