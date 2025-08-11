#!/usr/bin/env python3
"""
Convenient script to run both test clients for UUDEX API testing.
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and show its output."""
    print(f"\n{'='*60}")
    print(f"🏃 {description}")
    print(f"Command: {' '.join(cmd)}")
    print('=' * 60)

    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run UUDEX API test clients")
    parser.add_argument("--cert",
                        "-c",
                        default="alice",
                        choices=["alice", "pnnl", "acme"],
                        help="Certificate to use/simulate (default: alice)")
    parser.add_argument("--direct-only",
                        action="store_true",
                        help="Only run direct FastAPI test client")
    parser.add_argument("--mtls-only", action="store_true", help="Only run mTLS client")
    parser.add_argument("--no-db",
                        action="store_true",
                        help="Skip database initialization in direct client")

    args = parser.parse_args()

    print("UUDEX API Test Suite")
    print("=" * 40)
    print(f"Certificate: {args.cert}")

    # Ensure we're in the right directory
    if not Path("test_direct_client.py").exists():
        print("❌ Please run this from the fastapi-web-server directory")
        sys.exit(1)

    success_count = 0
    total_tests = 0

    # Run direct FastAPI test client
    if not args.mtls_only:
        total_tests += 1
        cmd = [sys.executable, "test_direct_client.py", "--cert", args.cert]
        if args.no_db:
            cmd.append("--no-db")

        if run_command(cmd, "Running Direct FastAPI Test Client"):
            success_count += 1
            print("✅ Direct client test completed")
        else:
            print("❌ Direct client test failed")

    # Run mTLS client
    if not args.direct_only:
        total_tests += 1
        cmd = [sys.executable, "query_subjects.py", "--cert", args.cert]

        if run_command(cmd, "Running mTLS Certificate Client"):
            success_count += 1
            print("✅ mTLS client test completed")
        else:
            print("❌ mTLS client test failed")

    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Test Results: {success_count}/{total_tests} tests passed")

    if success_count == total_tests:
        print("🎉 All tests completed successfully!")
    else:
        print("⚠️  Some tests failed. Check the output above.")

        print("\n🔧 Troubleshooting Tips:")
        print("1. Ensure UUDEX server is running: docker-compose up -d")
        print("2. Generate certificates: cd infrastructure/caddy && ./generate-certs.sh")
        print("3. Check certificates are in infrastructure/caddy/certs/")
        print("4. Check database has endpoint data")
        print("5. Verify Caddy is configured properly")

    return success_count == total_tests


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
