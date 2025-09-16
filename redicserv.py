#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python script that creates a Flask web server using Gunicorn
to redirect all requests to a URL provided as a command-line argument.

To use this script:

1. **Install required dependencies**:
```bash
pip install flask gunicorn
```

2. **Run with Flask development server** (for testing):
```bash
python redicserv "https://google.com"
```

3. **Run with Gunicorn** (for production):
```bash
gunicorn redic_serv:app -b 0.0.0.0:8000
```

When using Gunicorn, set the redirect URL via environment variable:
```bash
export REDIRECT_URL="https://google.com"
gunicorn redicserv:app -b 0.0.0.0:8000
```

## Key Features:

- **Command-line argument support** - Accepts URL as command-line argument.
- **Environment variable fallback** - Supports `REDIRECT_URL` environment
variable for Gunicorn compatibility.
- **Wildcard routing** - Catches all paths and redirects to target URL.
- **URL validation** - Automatically adds `https://` prefix if missing.
- **Production-ready** - Works with Gunicorn WSGI server.

## Advanced Configuration:

For production use, create a Gunicorn configuration file `gunicorn_conf.py`:
```python
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
timeout = 120
```

Run with config file:
```bash
gunicorn redicserv:app -c gunicorn_conf.py
```

The server will redirect all incoming requests (any path)
to the specified URL with HTTP 302 status code (temporary redirect).
For permanent redirects, change the code parameter to `301`
in the `redirect()` call.

```bash
export REDIRECT_URL="https://google.com"
gunicorn redicserv:app -b 0.0.0.0:8000
```
"""
import os
import sys
import argparse
from flask import Flask, redirect

__version__ = '0.1.0'
__author__ = "DOCTOR MOKIRA"


def create_app(redirect_url: str=None) -> Flask:
    """
    Factory function to create the Flask application.

    :param redirect_url: The URL string where we want to redict our navigator.
    :return: The instance of Flask server to perform the redirection.
    """
    app = Flask(__name__)

    # Get redirect URL from environment variable if not passed directly:
    target_url = redirect_url or os.environ.get('REDIRECT_URL')
    if not target_url:
        raise ValueError(
            "No redirect URL provided. Set `REDIRECT_URL` environment "
            "variable or pass as argument."
            )
    # Validate URL format
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        """Redirect all requests to the target URL."""
        return redirect(target_url, code=302)

    return app


def main() -> int:
    """Main function to start and run server of redirection."""
    parser = argparse.ArgumentParser(prog="REDIC SERV")
    parser.add_argument(
        "link", type=str,
        help=("Usage: ./redictserv \"<URL>\" or python redictserv \"<URL>\""
              "Example: python redirect_server.py \"https://google.com\"")
        )
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument(
        "--release", action="store_true",
        help="By default, it runs in debug mode."
        )
    args = parser.parse_args()
    # Get URL from command line argument:
    redirect_url = args.link

    # Set environment variable for Gunicorn compatibility:
    os.environ['REDIRECT_URL'] = redirect_url
    # Create app instance:
    app = create_app(redirect_url)
    # Run with Flask development server (for testing):
    app.run(host=args.host, port=args.port, debug=(not args.release))
    return 0


if __name__ == '__main__':
    code = main()
    sys.exit(code)
else:
    # Create app instance for Gunicorn:
    app = create_app()
