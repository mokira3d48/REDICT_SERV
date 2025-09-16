<div align="center">

# REDIC_SERV

![](https://img.shields.io/badge/Python-3.10-blue)
![](https://img.shields.io/badge/LICENSE-Apache--2.0-%2300557f)
![](https://img.shields.io/badge/lastest-2025--09--16-green)
![](https://img.shields.io/badge/contact-dr.mokira%40gmail.com-blueviolet)


</div>

Python script that creates a Flask web server using Gunicorn
to redirect all requests to a URL provided as a command-line argument.

To use this script:

1. **Install required dependencies**:
```bash
pip install flask gunicorn
```

2. **Run with Flask development server** (for testing):
```bash
python redicserv.py "https://google.com"
```

or

```bash
./redicserv.py "https://google.com"
```

3. **Run with Gunicorn** (for production):
```bash
gunicorn redicserv:app -b 0.0.0.0:8000
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

## Licence

This project is licensed under the Apache 2.0 License.
See the file [LICENSE](LICENSE) for more details, contact me please.

## Contact

For your question or suggestion, contact me please :

- **Names**: DOCTOR MOKIRA
- **Email**: dr.mokira@gmail.com
- **GitHub**: [mokira3d48](https://github.com/mokira3d48)
- **GitLab**: [mokira3d48](https://gitlab.com/mokira3d48)
