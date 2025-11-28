# 🚀 python-logging-loki-v2

> Modern Python logging handler for Grafana Loki

[![PyPI version](https://img.shields.io/pypi/v/python-logging-loki-v2.svg)](https://pypi.org/project/python-logging-loki-v2/)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

Send Python logs directly to [Grafana Loki](https://grafana.com/loki) with minimal configuration.

---

## ✨ Features

- 📤 **Direct Integration** - Send logs straight to Loki
- 🔐 **Authentication Support** - Basic auth and custom headers
- 🏷️ **Custom Labels** - Flexible tagging system
- ⚡ **Async Support** - Non-blocking queue handler included
- 🔒 **SSL Verification** - Configurable SSL/TLS settings
- 🎯 **Multi-tenant** - Support for Loki multi-tenancy

---

## 📦 Installation

```bash
pip install python-logging-loki-v2
```

---

## 🎯 Quick Start

### Basic Usage

```python
import logging
import logging_loki

handler = logging_loki.LokiHandler(
    url="https://loki.example.com/loki/api/v1/push",
    tags={"app": "my-application"},
    auth=("username", "password"),
    version="2"
)

logger = logging.getLogger("my-app")
logger.addHandler(handler)
logger.info("Application started", extra={"tags": {"env": "production"}})
```

### Async/Non-blocking Mode

For high-throughput applications, use the queue handler to avoid blocking:

```python
import logging.handlers
import logging_loki
from multiprocessing import Queue

handler = logging_loki.LokiQueueHandler(
    Queue(-1),
    url="https://loki.example.com/loki/api/v1/push",
    tags={"app": "my-application"},
    version="2"
)

logger = logging.getLogger("my-app")
logger.addHandler(handler)
logger.info("Non-blocking log message")
```

---

## ⚙️ Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | `str` | *required* | Loki push endpoint URL |
| `tags` | `dict` | `{}` | Default labels for all logs |
| `auth` | `tuple` | `None` | Basic auth credentials `(username, password)` |
| `headers` | `dict` | `None` | Custom HTTP headers (e.g., for multi-tenancy) |
| `version` | `str` | `"1"` | Loki API version (`"0"`, `"1"`, or `"2"`) |
| `verify_ssl` | `bool` | `True` | Enable/disable SSL certificate verification |

---

## 🏷️ Labels

Logs are automatically labeled with:
- **severity** - Log level (INFO, ERROR, etc.)
- **logger** - Logger name
- **Custom tags** - From handler and `extra={"tags": {...}}`

```python
logger.error(
    "Database connection failed",
    extra={"tags": {"service": "api", "region": "us-east"}}
)
```

---

## 🔐 Multi-tenant Setup

```python
handler = logging_loki.LokiHandler(
    url="https://loki.example.com/loki/api/v1/push",
    headers={"X-Scope-OrgID": "tenant-1"},
    tags={"app": "my-app"}
)
```

---
Based on [python-logging-loki](https://github.com/GreyZmeem/python-logging-loki) by GreyZmeem.

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---
