#!/usr/bin/env python3
"""
Test script for hallucination detection
"""
import sys
import os

sys.path.append("src/python")

from kairos_ai import KairosAI


def test_hallucination_detection():
    """Test the hallucination detection with sample responses."""

    # Initialize Kairos
    try:
        kairos = KairosAI()
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return

    # Test cases with different hallucination patterns
    test_cases = [
        {
            "name": "Basic 'You:' hallucination",
            "response": "🧚✨ Kairos: That's a great question!\n\nYou: Thanks for explaining that.",
        },
        {
            "name": "Old emoji hallucination",
            "response": "🧚✨ Kairos: I understand.\n\n👤 You: Can you help me?",
        },
        {
            "name": "New emoji hallucination",
            "response": "🧚✨ Kairos: Absolutely!\n\n✍️✨ You: That's helpful!",
        },
        {
            "name": "Multiple hallucinations",
            "response": "🧚✨ Kairos: Here's my answer.\n\nYou: I see.\nYou: Can you elaborate?\nYou: Thanks!",
        },
        {
            "name": "Clean response (no hallucination)",
            "response": "🧚✨ Kairos: This is a normal response without any fake user input.",
        },
    ]

    print("🧪 Testing Hallucination Detection")
    print("=" * 50)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['name']}")
        print(f"Input: {repr(test_case['response'])}")

        # Test the detection
        cleaned_response, hallucinations = kairos.detect_hallucinations(
            test_case["response"]
        )

        if hallucinations:
            print(f"🚨 DETECTED HALLUCINATIONS:")
            for hall in hallucinations:
                print(f"  - {hall}")
            print(f"✅ Cleaned response: {repr(cleaned_response)}")
        else:
            print("✅ No hallucinations detected")
            print(f"✅ Response unchanged: {repr(cleaned_response)}")

        print("-" * 30)

    print("\n🎉 Hallucination detection test complete!")


if __name__ == "__main__":
    test_hallucination_detection()
