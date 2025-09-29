#!/usr/bin/env python3
"""
Essential API Server Tests - Core functionality only
"""
import unittest
import requests
import time
import subprocess
import os
import sys

# Add the src/python directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestAPIServer(unittest.TestCase):
    """Test essential Flask API server endpoints."""
    
    @classmethod
    def setUpClass(cls):
        """Start the API server before running tests."""
        cls.base_url = "http://localhost:8000/api"
        cls.server_process = None
        
        # Start the API server in a separate process
        try:
            cls.server_process = subprocess.Popen([
                sys.executable, "api_server.py"
            ], cwd=os.path.join(os.path.dirname(__file__), '..'))
            
            # Wait for server to start
            time.sleep(3)
            
            # Test if server is running
            try:
                response = requests.get(f"{cls.base_url}/stats", timeout=5)
                if response.status_code != 200:
                    raise Exception("Server not responding")
            except requests.exceptions.RequestException:
                raise Exception("Server failed to start")
                
        except Exception as e:
            print(f"Failed to start API server: {e}")
            raise
    
    @classmethod
    def tearDownClass(cls):
        """Stop the API server after tests."""
        if cls.server_process:
            cls.server_process.terminate()
            cls.server_process.wait()
    
    def test_stats_endpoint(self):
        """Test the stats endpoint."""
        response = requests.get(f"{self.base_url}/stats")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('stats', data)
        self.assertIn('chat_history_count', data['stats'])
        self.assertIn('spellbook_memories_count', data['stats'])
    
    def test_chat_endpoint(self):
        """Test the chat endpoint."""
        chat_data = {
            "message": "Hello, this is a test message",
            "include_memories": False
        }
        
        response = requests.post(
            f"{self.base_url}/chat",
            json=chat_data,
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('response', data)
        self.assertIsInstance(data['response'], str)
    
    def test_memories_crud(self):
        """Test memory CRUD operations."""
        # Add memory
        memory_data = {
            "memory_key": "test_memory",
            "memory_value": "This is a test memory",
            "priority": 7
        }
        
        add_response = requests.post(
            f"{self.base_url}/memories",
            json=memory_data,
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(add_response.status_code, 200)
        
        # Get memories
        get_response = requests.get(f"{self.base_url}/memories")
        self.assertEqual(get_response.status_code, 200)
        
        data = get_response.json()
        self.assertIn('memories', data)
        self.assertIsInstance(data['memories'], list)
        
        # Delete memory
        delete_response = requests.delete(f"{self.base_url}/memories/test_memory")
        self.assertEqual(delete_response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
