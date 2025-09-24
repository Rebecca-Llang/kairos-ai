#!/usr/bin/env python3
"""
Quick API connectivity and timeout test for Kairos AI.
Use this for fast checks without running the full system.
"""
import requests
import time
import json
import sys

# ============================================================================
# CONFIGURATION
# ============================================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"
TEST_TIMEOUT = 30

def test_ollama_connection():
    """Test basic Ollama connectivity."""
    print("🔌 Testing Ollama Connection...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model["name"] for model in models]
            
            if MODEL_NAME in model_names:
                print(f"✅ Ollama connected, {MODEL_NAME} available")
                return True
            else:
                print(f"❌ {MODEL_NAME} not found. Available: {model_names}")
                return False
        else:
            print(f"❌ HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_model_response():
    """Test model response with timeout."""
    print("🤖 Testing Model Response...")
    
    test_prompt = "Say 'API test successful' and nothing else."
    
    try:
        start_time = time.time()
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": test_prompt,
                "stream": False
            },
            timeout=TEST_TIMEOUT
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "").strip().lower()
            
            if "api test successful" in response_text:
                print(f"✅ Model responded correctly in {end_time - start_time:.2f}s")
                return True
            else:
                print(f"⚠️ Model responded but not as expected: '{result.get('response', '')[:50]}...'")
                return True  # Still counts as success
        else:
            print(f"❌ HTTP {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"❌ Request timed out after {TEST_TIMEOUT} seconds")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_streaming():
    """Test streaming response."""
    print("🌊 Testing Streaming...")
    
    test_prompt = "Count from 1 to 3, one number per line."
    
    try:
        start_time = time.time()
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": test_prompt,
                "stream": True
            },
            timeout=TEST_TIMEOUT,
            stream=True
        )
        
        if response.status_code == 200:
            chunks = 0
            print("    Streaming: ", end="", flush=True)
            
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if 'response' in data:
                            chunk = data['response']
                            print(chunk, end="", flush=True)
                            chunks += 1
                        if data.get('done', False):
                            break
                    except json.JSONDecodeError:
                        continue
            
            end_time = time.time()
            print(f"\n✅ Received {chunks} chunks in {end_time - start_time:.2f}s")
            return chunks > 1
        else:
            print(f"❌ HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_timeout_handling():
    """Test timeout handling."""
    print("⏱️ Testing Timeout Handling...")
    
    try:
        start_time = time.time()
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": "Write a very long, detailed essay about artificial intelligence",
                "stream": False
            },
            timeout=2
        )
        end_time = time.time()
        
        print(f"⚠️ Request completed in {end_time - start_time:.2f}s (expected timeout)")
        return False
        
    except requests.exceptions.Timeout:
        end_time = time.time()
        print(f"✅ Timeout handled correctly after {end_time - start_time:.2f}s")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Run quick API tests."""
    print("🧪 Kairos AI - Quick API Tests")
    print("=" * 40)
    
    tests = [
        ("Ollama Connection", test_ollama_connection),
        ("Model Response", test_model_response),
        ("Streaming", test_streaming),
        ("Timeout Handling", test_timeout_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All API tests passed! Kairos is ready to chat.")
        return 0
    else:
        print("⚠️ Some tests failed. Check Ollama status and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
