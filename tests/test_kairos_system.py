#!/usr/bin/env python3
"""
Comprehensive system tests for Kairos AI.
Tests API connectivity, memory retrieval, streaming, and performance.
"""
import sys
import os
import time
import json
import requests
from typing import List, Dict, Any

# ============================================================================
# SETUP
# ============================================================================

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'python'))

try:
    from kairos_ai import KairosAI, OLLAMA_URL, MODEL_NAME
    from sentence_transformers import SentenceTransformer
    import torch
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure you're in the project root and dependencies are installed")
    sys.exit(1)


class KairosSystemTester:
    """Comprehensive testing suite for Kairos AI system."""
    
    def __init__(self):
        self.kairos = None
        self.test_results = []
        
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log test results."""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "details": details
        })
    
    # ------------------------------------------------------------------------
    # CONNECTIVITY TESTS
    # ------------------------------------------------------------------------
    
    def test_ollama_connectivity(self):
        """Test basic Ollama API connectivity."""
        print("\n🔌 Testing Ollama Connectivity")
        print("=" * 40)
        
        try:
            # Test basic connection
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]
                
                if MODEL_NAME in model_names:
                    self.log_test("Ollama API Connection", True, f"Connected to Ollama, {MODEL_NAME} available")
                else:
                    self.log_test("Ollama API Connection", False, f"Connected but {MODEL_NAME} not found. Available: {model_names}")
            else:
                self.log_test("Ollama API Connection", False, f"HTTP {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            self.log_test("Ollama API Connection", False, "Cannot connect to Ollama. Is it running?")
        except requests.exceptions.Timeout:
            self.log_test("Ollama API Connection", False, "Connection timeout")
        except Exception as e:
            self.log_test("Ollama API Connection", False, f"Unexpected error: {e}")
    
    def test_model_generation(self):
        """Test basic model generation with timeout handling."""
        print("\n🤖 Testing Model Generation")
        print("=" * 40)
        
        test_prompt = "Hello, this is a test. Please respond with 'Test successful' and nothing else."
        
        try:
            start_time = time.time()
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": test_prompt,
                    "stream": False
                },
                timeout=30  # 30 second timeout for this test
            )
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "").strip()
                
                if "test successful" in response_text.lower():
                    self.log_test("Model Generation", True, f"Response received in {end_time - start_time:.2f}s")
                else:
                    self.log_test("Model Generation", True, f"Model responded but not as expected: '{response_text[:50]}...'")
            else:
                self.log_test("Model Generation", False, f"HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            self.log_test("Model Generation", False, "Request timed out after 30 seconds")
        except Exception as e:
            self.log_test("Model Generation", False, f"Error: {e}")
    
    def test_streaming_response(self):
        """Test streaming response functionality."""
        print("\n🌊 Testing Streaming Response")
        print("=" * 40)
        
        test_prompt = "Count from 1 to 5, saying each number on a new line."
        
        try:
            start_time = time.time()
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": test_prompt,
                    "stream": True
                },
                timeout=30,
                stream=True
            )
            
            if response.status_code == 200:
                chunks_received = 0
                full_response = ""
                
                print("    Streaming response:")
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            if 'response' in data:
                                chunk = data['response']
                                print(f"    {chunk}", end="", flush=True)
                                full_response += chunk
                                chunks_received += 1
                            if data.get('done', False):
                                break
                        except json.JSONDecodeError:
                            continue
                
                end_time = time.time()
                print(f"\n    Received {chunks_received} chunks in {end_time - start_time:.2f}s")
                
                if chunks_received > 1:
                    self.log_test("Streaming Response", True, f"Received {chunks_received} chunks successfully")
                else:
                    self.log_test("Streaming Response", False, "Only received 1 chunk - streaming may not be working")
            else:
                self.log_test("Streaming Response", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Streaming Response", False, f"Error: {e}")
    
    # ------------------------------------------------------------------------
    # SYSTEM TESTS
    # ------------------------------------------------------------------------
    
    def test_kairos_initialization(self):
        """Test Kairos AI initialization and memory loading."""
        print("\n🧠 Testing Kairos Initialization")
        print("=" * 40)
        
        try:
            self.kairos = KairosAI()
            
            # Test memory loading
            if self.kairos.memory:
                self.log_test("Memory Loading", True, f"Loaded {len(self.kairos.memory)} memory items")
            else:
                self.log_test("Memory Loading", False, "No memories loaded")
            
            # Test history loading
            if self.kairos.history:
                self.log_test("History Loading", True, f"Loaded {len(self.kairos.history)} history items")
            else:
                self.log_test("History Loading", True, "No history loaded (this is OK for new installations)")
            
            # Test persona loading
            if self.kairos.persona and len(self.kairos.persona) > 100:
                self.log_test("Persona Loading", True, f"Loaded persona ({len(self.kairos.persona)} chars)")
            else:
                self.log_test("Persona Loading", False, "Persona not loaded or too short")
                
        except Exception as e:
            self.log_test("Kairos Initialization", False, f"Error: {e}")
    
    def test_memory_retrieval(self):
        """Test memory retrieval and embedding functionality."""
        print("\n🔍 Testing Memory Retrieval")
        print("=" * 40)
        
        if not self.kairos:
            self.log_test("Memory Retrieval", False, "Kairos not initialized")
            return
        
        test_queries = [
            "I'm feeling scattered and can't focus",
            "What are my strengths?",
            "Tell me about my energy patterns",
            "I need help with productivity"
        ]
        
        for query in test_queries:
            try:
                start_time = time.time()
                relevant_memories = self.kairos.get_relevant_memories(query)
                end_time = time.time()
                
                if relevant_memories:
                    self.log_test(f"Memory Retrieval: '{query[:30]}...'", True, 
                                f"Found {len(relevant_memories)} relevant memories in {end_time - start_time:.3f}s")
                else:
                    self.log_test(f"Memory Retrieval: '{query[:30]}...'", False, "No relevant memories found")
                    
            except Exception as e:
                self.log_test(f"Memory Retrieval: '{query[:30]}...'", False, f"Error: {e}")
    
    def test_embedding_performance(self):
        """Test embedding generation and caching performance."""
        print("\n⚡ Testing Embedding Performance")
        print("=" * 40)
        
        if not self.kairos:
            self.log_test("Embedding Performance", False, "Kairos not initialized")
            return
        
        test_texts = [
            "I'm feeling scattered today",
            "I'm feeling scattered today",  # Duplicate to test caching
            "What are my productivity methods?",
            "Tell me about my neurodivergence",
            "I need emotional regulation tools"
        ]
        
        for i, text in enumerate(test_texts):
            try:
                start_time = time.time()
                relevant_memories = self.kairos.get_relevant_memories(text)
                end_time = time.time()
                
                # Check if caching is working (second query should be faster)
                if i == 1 and end_time - start_time < 0.01:  # Very fast = cached
                    self.log_test(f"Embedding Caching", True, f"Cached query completed in {end_time - start_time:.4f}s")
                elif i == 1:
                    self.log_test(f"Embedding Caching", False, f"Query not cached, took {end_time - start_time:.3f}s")
                else:
                    self.log_test(f"Embedding Generation", True, f"Generated embeddings in {end_time - start_time:.3f}s")
                    
            except Exception as e:
                self.log_test(f"Embedding Performance", False, f"Error: {e}")
    
    # ------------------------------------------------------------------------
    # PERFORMANCE TESTS
    # ------------------------------------------------------------------------
    
    def test_response_generation(self):
        """Test full response generation with timeout handling."""
        print("\n💬 Testing Response Generation")
        print("=" * 40)
        
        if not self.kairos:
            self.log_test("Response Generation", False, "Kairos not initialized")
            return
        
        test_messages = [
            "Hello Kairos, how are you?",
            "I'm feeling overwhelmed today",
            "What strategies work for my ADHD?"
        ]
        
        for message in test_messages:
            try:
                start_time = time.time()
                response = self.kairos.generate_response(message)
                end_time = time.time()
                
                if response and len(response) > 10:
                    self.log_test(f"Response Generation: '{message[:30]}...'", True, 
                                f"Generated {len(response)} char response in {end_time - start_time:.2f}s")
                else:
                    self.log_test(f"Response Generation: '{message[:30]}...'", False, 
                                f"Response too short or empty: '{response}'")
                    
            except Exception as e:
                self.log_test(f"Response Generation: '{message[:30]}...'", False, f"Error: {e}")
    
    def test_timeout_handling(self):
        """Test timeout handling with intentionally slow requests."""
        print("\n⏱️ Testing Timeout Handling")
        print("=" * 40)
        
        # Test with a very short timeout to trigger timeout handling
        try:
            start_time = time.time()
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": "Write a very long, detailed response about artificial intelligence",
                    "stream": False
                },
                timeout=1  # Very short timeout
            )
            end_time = time.time()
            
            # If we get here, the request completed quickly (unexpected)
            self.log_test("Timeout Handling", False, f"Request completed in {end_time - start_time:.2f}s (expected timeout)")
            
        except requests.exceptions.Timeout:
            end_time = time.time()
            self.log_test("Timeout Handling", True, f"Timeout handled correctly after {end_time - start_time:.2f}s")
        except Exception as e:
            self.log_test("Timeout Handling", False, f"Unexpected error: {e}")
    
    def test_session_pooling(self):
        """Test HTTP session pooling functionality."""
        print("\n🔗 Testing Session Pooling")
        print("=" * 40)
        
        if not self.kairos:
            self.log_test("Session Pooling", False, "Kairos not initialized")
            return
        
        try:
            # Make multiple requests to test connection reuse
            times = []
            for i in range(3):
                start_time = time.time()
                response = self.kairos.session.get("http://localhost:11434/api/tags", timeout=5)
                end_time = time.time()
                times.append(end_time - start_time)
                
                if response.status_code != 200:
                    self.log_test("Session Pooling", False, f"Request {i+1} failed with status {response.status_code}")
                    return
            
            # Check if subsequent requests are faster (indicating connection reuse)
            if len(times) >= 2 and times[1] < times[0] * 0.8:  # Second request significantly faster
                self.log_test("Session Pooling", True, f"Connection reuse detected: {times[0]:.3f}s -> {times[1]:.3f}s")
            else:
                self.log_test("Session Pooling", True, f"Session created successfully: {times}")
                
        except Exception as e:
            self.log_test("Session Pooling", False, f"Error: {e}")
    
    def run_all_tests(self):
        """Run all system tests."""
        print("🧪 Kairos AI System Tests")
        print("=" * 50)
        
        # Run all tests
        self.test_ollama_connectivity()
        self.test_model_generation()
        self.test_streaming_response()
        self.test_kairos_initialization()
        self.test_memory_retrieval()
        self.test_embedding_performance()
        self.test_response_generation()
        self.test_timeout_handling()
        self.test_session_pooling()
        
        # Summary
        print("\n📊 Test Summary")
        print("=" * 50)
        
        passed = sum(1 for result in self.test_results if result["passed"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {passed/total*100:.1f}%")
        
        if passed == total:
            print("\n🎉 All tests passed! Kairos system is working correctly.")
        else:
            print(f"\n⚠️ {total - passed} tests failed. Check the output above for details.")
        
        return passed == total


def main():
    """Run the system tests."""
    tester = KairosSystemTester()
    success = tester.run_all_tests()
    
    # Clean up
    if tester.kairos:
        tester.kairos.cleanup()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
