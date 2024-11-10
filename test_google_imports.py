try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    print("Google packages successfully imported!")
except ImportError as e:
    print(f"Import error: {str(e)}")
    print("\nTrying to get more information...")
    import sys
    print(f"\nPython path: {sys.path}")
    print(f"\nPython version: {sys.version}")
    print(f"\nPackages installed in this environment:")
    import pkg_resources
    installed_packages = [f"{dist.key} ({dist.version})" 
                         for dist in pkg_resources.working_set]
    for package in installed_packages:
        print(package) 