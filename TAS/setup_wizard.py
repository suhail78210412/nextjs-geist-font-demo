#!/usr/bin/env python3
"""
TAS Setup Wizard
Interactive setup for TAS AI Assistant
"""

import asyncio
import os
import sys
from pathlib import Path
from core.config_manager import ConfigManager
from core.consent_manager import ConsentManager

async def main():
    """Run setup wizard"""
    print("🤖 TAS Setup Wizard")
    print("==================")
    print("Welcome to TAS - Your AI Assistant")
    print()
    
    # Initialize config
    config = ConfigManager()
    await config.load()
    
    # Language selection
    print("Select language:")
    print("1. Hindi (हिंदी)")
    print("2. English")
    choice = input("Enter choice (1-2): ").strip()
    
    if choice == "1":
        config.set("language", "hindi")
    else:
        config.set("language", "english")
    
    # API Keys configuration
    print("\n🔑 API Configuration")
    print("Enter your API keys (leave empty to skip):")
    
    openai_key = input("OpenAI API Key: ").strip()
    if openai_key:
        config.set("api_keys.openai", openai_key)
    
    google_key = input("Google Cloud API Key: ").strip()
    if google_key:
        config.set("api_keys.google_cloud", google_key)
    
    cohere_key = input("Cohere API Key: ").strip()
    if cohere_key:
        config.set("api_keys.cohere", cohere_key)
    
    groq_key = input("Groq API Key: ").strip()
    if groq_key:
        config.set("api_keys.groq", groq_key)
    
    # Privacy and consent
    consent_manager = ConsentManager(config)
    
    print("\n🔒 Privacy Settings")
    camera_consent = input("Enable camera for face recognition? (yes/no): ").strip().lower()
    if camera_consent == "yes":
        consent_manager.request_camera_consent()
    
    data_consent = input("Allow data collection for memory? (yes/no): ").strip().lower()
    if data_consent == "yes":
        consent_manager.request_data_collection_consent()
    
    # Memory retention
    print("\n🧠 Memory Settings")
    print("How long should TAS remember your data?")
    print("1. 1 month (default)")
    print("2. 1 year")
    print("3. Forever")
    
    memory_choice = input("Enter choice (1-3): ").strip()
    if memory_choice == "2":
        config.set("memory_retention_days", 365)
    elif memory_choice == "3":
        config.set("memory_retention_days", 9999)
    
    # Save configuration
    await config.save()
    
    print("\n✅ Setup Complete!")
    print("TAS is now configured and ready to use.")
    print("\nTo start TAS, run:")
    print("python main.py")

if __name__ == "__main__":
    asyncio.run(main())
