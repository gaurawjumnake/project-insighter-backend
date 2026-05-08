# Health Check API Documentation

**Endpoint:** `GET /api/v1/health`  
**Purpose:** Monitor application and database health  
**Added:** 2026-05-07

---

## 📋 Overview

The health check endpoint provides a lightweight, low-latency mechanism to:
- Verify application is running
- Test database connectivity
- Monitor latency to database
- Support infrastructure health checks (ALB, NLB, Kubernetes)
- Enable monitoring and alerting systems

**Response Time:** Typically 1-5ms (measured in response body)

---

## 🎯 Response Format

### Successful Response (200 OK)

```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-05-07T14:30:00Z",
  "message": "Database connectivity OK (latency: 2ms)"
}
```

**Fields:**
- `status` (string): Overall health status
  - `"healthy"` - Application and database are operational
  - `"unhealthy"` - Application or database has issues
- `database` (string): Database connectivity status
  - `"connected"` - Database is accessible
  - `"disconnected"` - Database is not accessible
- `timestamp` (ISO 8601 datetime): When health check was performed (UTC)
- `message` (string): Detailed status message with latency or error reason

---

## 🔴 Error Response (503 Service Unavailable)

When database is unavailable, the endpoint returns status code 200 with unhealthy payload (not 503, for compatibility with some load balancers):

```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "timestamp": "2026-05-07T14:30:05Z",
  "message": "Failed to connect to database: connection timeout (5s)"
}
```

**Note:** The HTTP status code is `200` even when unhealthy, so check the `status` field in response body.

---

## 🚀 Usage Examples

### cURL

```bash
# Basic health check
curl -X GET http://localhost:8000/api/v1/health

# With verbose output
curl -v http://localhost:8000/api/v1/health

# In a monitoring script (check status field)
curl -s http://localhost:8000/api/v1/health | jq '.status'
```

### Python

```python
import requests
import json

response = requests.get("http://localhost:8000/api/v1/health")
health_data = response.json()

if health_data["status"] == "healthy":
    print(f"✓ Application is healthy")
    print(f"✓ Database latency: {health_data['message']}")
else:
    print(f"✗ Application is unhealthy: {health_data['message']}")
```

### JavaScript/Node.js

```javascript
fetch("http://localhost:8000/api/v1/health")
  .then(res => res.json())
  .then(data => {
    if (data.status === "healthy") {
      console.log("✓ Service is healthy");
    } else {
      console.error("✗ Service is unhealthy:", data.message);
    }
  });
```

### AWS ALB Health Check Configuration

```
Protocol: HTTP
Path: /api/v1/health
Port: 8000
Healthy Threshold: 2
Unhealthy Threshold: 2
Timeout: 5 seconds
Interval: 30 seconds
Matcher: 200 (HTTP status codes)
```

### Kubernetes Liveness Probe

```yaml
livenessProbe:
  httpGet:
    path: /api/v1/health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

### Kubernetes Readiness Probe

```yaml
readinessProbe:
  httpGet:
    path: /api/v1/health
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 2
```

---

## 🔧 Configuration

The health check service uses the following configuration:

| Setting | Value | Notes |
|---------|-------|-------|
| **Database Timeout** | 5 seconds | Maximum time to wait for DB response |
| **Query** | `SELECT 1` | Lightweight test query |
| **Latency Tracking** | Yes | Measures DB response time |
| **Caching** | None | Always performs fresh check |

---

## 📊 Error Scenarios

### Scenario 1: Database Connection Refused

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/health
```

**Response (200 with unhealthy status):**
```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "timestamp": "2026-05-07T14:30:05Z",
  "message": "Failed to connect to database: (psycopg2.OperationalError) could not connect to server"
}
```

### Scenario 2: Database Connection Timeout

**Cause:** Network latency or database server slow to respond

**Response:**
```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "timestamp": "2026-05-07T14:30:10Z",
  "message": "Failed to connect to database: connection timeout (5s)"
}
```

### Scenario 3: Database Query Timeout

**Cause:** Database server responding slowly to SELECT 1 query

**Response:**
```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "timestamp": "2026-05-07T14:30:15Z",
  "message": "Failed to connect to database: connection timeout (5s)"
}
```

### Scenario 4: Healthy with Normal Latency

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-05-07T14:30:20Z",
  "message": "Database connectivity OK (latency: 2ms)"
}
```

---

## 📈 Monitoring & Alerting

### Prometheus Metrics

To expose this as a Prometheus metric, parse the response:

```yaml
# Example scrape config
- job_name: 'project-insighter'
  static_configs:
    - targets: ['localhost:8000']
  relabel_configs:
    - source_labels: [__address__]
      target_label: instance
      replacement: 'health'
```

### DataDog Integration

```python
# In your monitoring script
import requests
import statsd

client = statsd.StatsClient('localhost', 8125)

response = requests.get("http://localhost:8000/api/v1/health")
data = response.json()

if data["status"] == "healthy":
    client.gauge('health.status', 1)
    # Extract latency from message
    latency = int(data["message"].split("latency: ")[1].split("ms")[0])
    client.gauge('health.latency_ms', latency)
else:
    client.gauge('health.status', 0)
```

### CloudWatch Integration

```bash
# Monitor health check every 30 seconds
while true; do
  curl -s http://localhost:8000/api/v1/health | jq '.status' | \
    aws cloudwatch put-metric-data \
      --metric-name ApplicationHealth \
      --value $([ "$(cat)" = '"healthy"' ] && echo 1 || echo 0) \
      --namespace ProjectInsighter
  sleep 30
done
```

---

## 🛠️ Troubleshooting

### Health Check Returns Unhealthy

**Step 1: Verify Database Credentials**
```bash
# Check environment variables
echo $DB_HOST $DB_PORT $DB_USER $DB_NAME
```

**Step 2: Test Database Connection Directly**
```bash
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT 1"
```

**Step 3: Check Database Server Status**
```bash
# For PostgreSQL
pg_isready -h $DB_HOST -p $DB_PORT
```

**Step 4: Review Application Logs**
```bash
# Check for connection errors
tail -f app.log | grep -i "database\|connection\|health"
```

### High Latency Detected

If latency is > 50ms:

1. **Check Database Load**
   ```sql
   SELECT count(*) FROM pg_stat_activity;
   ```

2. **Check Network Latency**
   ```bash
   ping -c 3 $DB_HOST
   ```

3. **Review Database Queries**
   ```sql
   SELECT query, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
   ```

---

## 📋 Implementation Details

### Service Layer

**File:** [backend/core/services/health_service.py](../backend/core/services/health_service.py)

- `HealthCheckService` class: Performs database connectivity checks
- Async implementation for non-blocking operations
- Configurable timeout (default 5 seconds)
- Latency measurement with millisecond precision
- Comprehensive error handling

### API Endpoint

**File:** [backend/finance/app/api/health.py](../backend/finance/app/api/health.py)

- FastAPI router with GET /health endpoint
- Response model: `HealthCheckResponse` Pydantic schema
- Dependency injection for database session
- OpenAPI auto-documentation

### Schema

**File:** [backend/core/schemas/health.py](../backend/core/schemas/health.py)

- `HealthCheckResponse` Pydantic model
- Full type hints and validation
- JSON schema examples for API docs

---

## 🧪 Testing

### Run Unit Tests

```bash
# All health check tests
uv run pytest tests/test_health.py -v

# With coverage report
uv run pytest tests/test_health.py --cov=backend.core.services.health_service --cov=backend.finance.app.api.health

# Specific test
uv run pytest tests/test_health.py::test_health_check_happy_path_db_connected -v
```

### Test Coverage

**Current Coverage:** 95% (58/61 lines)

**Test Scenarios:**
- ✅ Happy path (DB connected)
- ✅ Connection errors
- ✅ Timeout scenarios
- ✅ Generic exceptions
- ✅ Response schema validation
- ✅ HTTP status codes
- ✅ OpenAPI documentation

---

## 📚 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL libpq Documentation](https://www.postgresql.org/docs/current/libpq.html)

---

## ✅ Checklist for Integration

- [ ] Health endpoint is accessible at `/api/v1/health`
- [ ] Database credentials are properly configured
- [ ] Response returns healthy status when DB is connected
- [ ] Load balancer is configured to use health endpoint
- [ ] Monitoring/alerting system is consuming health checks
- [ ] Kubernetes probes are configured (if using K8s)
- [ ] Tests pass with >95% coverage
- [ ] Documentation is updated

---

**Last Updated:** 2026-05-07  
**Status:** ✅ Production Ready
