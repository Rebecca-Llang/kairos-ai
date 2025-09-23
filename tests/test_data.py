#!/usr/bin/env python3
"""
Data validation tests for Kairos AI.
Tests file structure and data format validation.
"""
import os
import json

def test_file_existence():
    """Test that required files exist."""
    print("📁 Testing file existence...")
    files = [
        'src/python/kairos_ai.py',
        'src/python/prompt.yaml',
        'src/python/the-spellbook.json',
        'src/python/chat-history.json'
    ]
    
    all_exist = True
    for file_path in files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            all_exist = False
    
    return all_exist

def test_json_validity():
    """Test that JSON files are valid."""
    print("\n📄 Testing JSON validity...")
    json_files = [
        'src/python/the-spellbook.json',
        'src/python/chat-history.json'
    ]
    
    all_valid = True
    for file_path in json_files:
        try:
            with open(file_path, 'r') as f:
                json.load(f)
            print(f"✅ {file_path} - Valid JSON")
        except Exception as e:
            print(f"❌ {file_path} - Invalid JSON: {e}")
            all_valid = False
    
    return all_valid

def test_memory_structure():
    """Test memory file has correct structure."""
    print("\n🧠 Testing memory structure...")
    try:
        with open('src/python/the-spellbook.json', 'r') as f:
            memory = json.load(f)
        
        # Should be a list
        if isinstance(memory, list):
            print("✅ Memory file is a list")
            
            # If not empty, check structure
            if memory:
                first_memory = memory[0]
                if isinstance(first_memory, dict):
                    print("✅ Memory entries are dictionaries")
                    return True
                else:
                    print("❌ Memory entries should be dictionaries")
                    return False
            else:
                print("✅ Empty memory file (OK)")
                return True
        else:
            print("❌ Memory file should be a list")
            return False
            
    except Exception as e:
        print(f"❌ Memory structure error: {e}")
        return False

def test_chat_structure():
    """Test chat history has correct structure."""
    print("\n💬 Testing chat structure...")
    try:
        with open('src/python/chat-history.json', 'r') as f:
            history = json.load(f)
        
        # Should be a list
        if isinstance(history, list):
            print("✅ Chat history is a list")
            
            # If not empty, check structure
            if history:
                first_msg = history[0]
                if isinstance(first_msg, dict) and 'role' in first_msg and 'content' in first_msg:
                    print("✅ Chat messages have required fields")
                    return True
                else:
                    print("❌ Chat messages missing required fields")
                    return False
            else:
                print("✅ Empty chat history (OK)")
                return True
        else:
            print("❌ Chat history should be a list")
            return False
            
    except Exception as e:
        print(f"❌ Chat structure error: {e}")
        return False

def run_tests():
    """Run all data tests."""
    tests = [
        test_file_existence,
        test_json_validity,
        test_memory_structure,
        test_chat_structure
    ]
    return sum(1 for test in tests if test())

if __name__ == "__main__":
    print("🧪 Data Tests")
    print("=" * 20)
    passed = run_tests()
    print(f"\n📊 {passed}/{len([test_file_existence, test_json_validity, test_memory_structure, test_chat_structure])} tests passed")
    exit(0 if passed == 4 else 1)
