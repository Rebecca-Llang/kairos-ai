#!/usr/bin/env python3
"""
Configuration tests for Kairos AI.
Tests YAML configuration and package.json scripts.
"""
import json

def test_yaml_config():
    """Test YAML file is valid."""
    print("📄 Testing YAML configuration...")
    try:
        import yaml
        with open('src/python/prompt.yaml', 'r') as f:
            data = yaml.safe_load(f)
        
        # Check it has required fields
        if 'persona' in data:
            print("✅ prompt.yaml - Valid YAML with persona")
            return True
        else:
            print("❌ prompt.yaml - Missing 'persona' field")
            return False
    except ImportError:
        print("⚠️  PyYAML not installed - skipping YAML test")
        return True
    except Exception as e:
        print(f"❌ YAML error: {e}")
        return False

def test_package_scripts():
    """Test that package.json has required scripts."""
    print("\n📋 Testing package scripts...")
    try:
        with open('package.json', 'r') as f:
            package = json.load(f)
        
        scripts = package.get('scripts', {})
        required_scripts = ['start', 'test', 'reset', 'debug']
        
        missing = []
        for script in required_scripts:
            if script in scripts:
                print(f"✅ {script} script exists")
            else:
                print(f"❌ {script} script missing")
                missing.append(script)
        
        if missing:
            print(f"❌ Missing scripts: {', '.join(missing)}")
            return False
        else:
            print("✅ All required scripts present")
            return True
            
    except Exception as e:
        print(f"❌ Package.json error: {e}")
        return False

def test_package_info():
    """Test that package.json has basic required fields."""
    print("\n📦 Testing package info...")
    try:
        with open('package.json', 'r') as f:
            package = json.load(f)
        
        required_fields = ['name', 'version', 'scripts']
        missing = []
        
        for field in required_fields:
            if field in package:
                print(f"✅ {field} field exists")
            else:
                print(f"❌ {field} field missing")
                missing.append(field)
        
        if missing:
            print(f"❌ Missing fields: {', '.join(missing)}")
            return False
        else:
            print("✅ All required fields present")
            return True
            
    except Exception as e:
        print(f"❌ Package.json error: {e}")
        return False

def run_tests():
    """Run all configuration tests."""
    tests = [
        test_yaml_config,
        test_package_scripts,
        test_package_info
    ]
    return sum(1 for test in tests if test())

if __name__ == "__main__":
    print("🧪 Configuration Tests")
    print("=" * 25)
    passed = run_tests()
    print(f"\n📊 {passed}/{len([test_yaml_config, test_package_scripts, test_package_info])} tests passed")
    exit(0 if passed == 3 else 1)
