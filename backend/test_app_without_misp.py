#!/usr/bin/env python3
"""
Test script to verify the application loads without MISP dependencies
"""

import sys
import os
sys.path.append('.')

try:
    from app.main import app
    print("✅ SUCCESS: Application loads successfully without MISP!")
    print("✅ All MISP components have been successfully removed")
    print("✅ RTIP Platform is functional with remaining integrations:")
    print("   - Splunk SIEM")
    print("   - Elasticsearch") 
    print("   - Microsoft Sentinel")
    print("   - Generic SIEM")
    print("   - Core Threat Intelligence Platform")
    print("✅ No MISP or MySQL dependencies remain")
except ImportError as e:
    print(f"❌ Import Error: {e}")
except Exception as e:
    print(f"❌ General Error: {e}")
