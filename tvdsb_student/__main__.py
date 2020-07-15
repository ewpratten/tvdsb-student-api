import argparse
import getpass
import json

from .auth import getAuthInfo, AuthInfo

if __name__ == "__main__":
    
    # Create parser
    ap = argparse.ArgumentParser(description="Dumps all TVDSB Student info to STDOUT as JSON")

    # Auth
    ap.add_argument("--user", help="TVDSB account username", required=True)
    ap.add_argument("--passwd", help="TVDSB account password", required=False)

    # Parse arguments
    args = ap.parse_args()

    # Handle auth
    if not args.passwd:
        print("Student information is password protected")
        args.passwd = getpass.getpass("TVDSB Password: ")
    
    # Log in
    authInfo: AuthInfo = getAuthInfo(args.user, args.passwd)
    print(authInfo)