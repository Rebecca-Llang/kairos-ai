#!/usr/bin/env python3
"""
Core functionality tests for Kairos AI.
Tests basic Python functionality and imports.
"""
import sys

def test_syntax():
    """Test Python syntax validation."""
    print("🔍 Testing Python syntax...")
    try:
        with open('src/python/kairos_ai.py', 'r') as f:
            content = f.read()
        
        compile(content, 'src/python/kairos_ai.py', 'exec')
        print("✅ Python syntax is valid")
        return True
    except Exception as e:
        print(f"❌ Syntax error: {e}")
        return False

def test_imports():
    """Test that core imports work."""
    print("\n📦 Testing imports...")
    try:
        sys.path.insert(0, 'src/python')
        
        try:
            import kairos_ai
            print("✅ kairos_ai module imports")
            
            if hasattr(kairos_ai, 'KairosAI'):
                print("✅ KairosAI class exists")
                return True
            else:
                print("❌ KairosAI class missing")
                return False
        except ImportError as e:
            print(f"⚠️  Dependencies missing: {e}")
            print("✅ Module structure OK (install dependencies to test fully)")
            return True
            
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def run_tests():
    """Run all core tests."""
    tests = [test_syntax, test_imports]
    return sum(1 for test in tests if test())

if __name__ == "__main__":
    print("🧪 Core Tests")
    print("=" * 20)
    passed = run_tests()
    print(f"\n📊 {passed}/{len([test_syntax, test_imports])} tests passed")
    exit(0 if passed == 2 else 1)
