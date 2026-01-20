# HTTPS and Secure Redirects Implementation Guide

## Overview
This document provides detailed information about the HTTPS and secure redirect configurations implemented in the LibraryProject Django application. These settings ensure secure communication between clients and the server, protecting user data from interception and tampering.

## Security Settings Configuration

All HTTPS-related settings are configured in `LibraryProject/settings.py`.

### 1. SECURE_SSL_REDIRECT

**Setting:**
```python
SECURE_SSL_REDIRECT = False  # Set to True in production with HTTPS configured
```

**Purpose:** Automatically redirects all HTTP requests to HTTPS.

**How it works:**
- When set to `True`, Django's SecurityMiddleware intercepts all HTTP requests
- Requests are redirected to the HTTPS equivalent URL
- Uses a 301 (permanent redirect) status code

**Production Configuration:**
```python
SECURE_SSL_REDIRECT = True
```

**Important Notes:**
- Only enable this after SSL/TLS certificates are properly configured
- Ensure your web server (Nginx, Apache) is configured to handle HTTPS
- Test in a staging environment before enabling in production
- Can cause redirect loops if not configured correctly with load balancers

**Testing:**
```bash
# Before enabling, test manually:
curl -I http://yourdomain.com
# Should return 301 redirect to https://yourdomain.com
```

### 2. HTTP Strict Transport Security (HSTS)

HSTS is a security mechanism that forces browsers to only interact with the server over HTTPS.

#### SECURE_HSTS_SECONDS

**Setting:**
```python
SECURE_HSTS_SECONDS = 31536000  # 1 year
```

**Purpose:** Specifies how long (in seconds) browsers should remember to only access the site via HTTPS.

**Configuration Options:**
- `0`: HSTS disabled (not recommended for production)
- `300`: 5 minutes (for initial testing)
- `86400`: 24 hours (for staging environments)
- `2592000`: 30 days (minimum recommended for production)
- `31536000`: 1 year (recommended for production)
- `63072000`: 2 years (maximum recommended)

**How it works:**
1. Server sends `Strict-Transport-Security` header with max-age value
2. Browser remembers this setting for the specified duration
3. All future requests automatically use HTTPS, even if user types http://
4. Protects against SSL stripping attacks

#### SECURE_HSTS_INCLUDE_SUBDOMAINS

**Setting:**
```python
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```

**Purpose:** Extends HSTS policy to all subdomains.

**Impact:**
- When enabled, HSTS applies to:
  - `example.com`
  - `www.example.com`
  - `api.example.com`
  - `*.example.com`

**Warning:**
- Only enable if ALL subdomains support HTTPS
- Cannot make exceptions for specific subdomains
- If any subdomain lacks HTTPS, it becomes inaccessible

**Testing Subdomains:**
```bash
# Test each subdomain before enabling
curl -I https://www.yourdomain.com
curl -I https://api.yourdomain.com
# All should return 200 OK with valid SSL certificate
```

#### SECURE_HSTS_PRELOAD

**Setting:**
```python
SECURE_HSTS_PRELOAD = True
```

**Purpose:** Allows the domain to be included in browsers' HSTS preload lists.

**How it works:**
1. Browsers maintain a hardcoded list of HSTS-enabled domains
2. Sites on the preload list are always accessed via HTTPS
3. Protection applies even on the very first visit (before HSTS header is received)

**Requirements for Preloading:**
- `SECURE_HSTS_SECONDS` must be at least 31536000 (1 year)
- `SECURE_HSTS_INCLUDE_SUBDOMAINS` must be `True`
- Valid SSL certificate must be configured
- Must submit domain to https://hstspreload.org/

**Preload Submission Process:**
1. Configure all HSTS settings correctly
2. Deploy to production with HTTPS
3. Visit https://hstspreload.org/
4. Enter your domain and check eligibility
5. Submit domain for inclusion
6. Wait for approval (can take weeks to months)

**Warning:**
- **Preload is difficult to undo** - removal can take 6+ months
- Ensure you're committed to HTTPS for the long term
- Test thoroughly before submitting

### 3. Secure Cookie Settings

#### CSRF_COOKIE_SECURE

**Setting:**
```python
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
```

**Purpose:** Ensures CSRF tokens are only transmitted over HTTPS.

**Production Configuration:**
```python
CSRF_COOKIE_SECURE = True
```

**Impact:**
- CSRF cookies will have the `Secure` flag set
- Cookies will not be sent over unencrypted HTTP connections
- Prevents CSRF token theft through man-in-the-middle attacks

#### SESSION_COOKIE_SECURE

**Setting:**
```python
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
```

**Purpose:** Ensures session cookies are only transmitted over HTTPS.

**Production Configuration:**
```python
SESSION_COOKIE_SECURE = True
```

**Impact:**
- Session cookies will have the `Secure` flag set
- Prevents session hijacking through unencrypted connections
- Users must access site via HTTPS to maintain sessions

### 4. Additional Secure Headers

These settings were configured in Task 2 but work together with HTTPS:

#### SECURE_BROWSER_XSS_FILTER
```python
SECURE_BROWSER_XSS_FILTER = True
```
Enables browser's XSS filter to detect and block XSS attacks.

#### SECURE_CONTENT_TYPE_NOSNIFF
```python
SECURE_CONTENT_TYPE_NOSNIFF = True
```
Prevents MIME-sniffing attacks by enforcing declared content types.

#### X_FRAME_OPTIONS
```python
X_FRAME_OPTIONS = 'DENY'
```
Prevents clickjacking by blocking the site from being embedded in frames.

## SSL/TLS Certificate Setup

### Development Environment

For local development and testing:

**Option 1: Using Django's runserver (HTTP only)**
```bash
python manage.py runserver
# Access via http://localhost:8000
# Keep secure settings disabled
```

**Option 2: Using mkcert for local HTTPS**
```bash
# Install mkcert
# On macOS:
brew install mkcert
# On Windows with Chocolatey:
choco install mkcert

# Create local certificate
mkcert -install
mkcert localhost 127.0.0.1 ::1

# Run with django-sslserver
pip install django-sslserver
python manage.py runsslserver --certificate localhost+2.pem --key localhost+2-key.pem
```

### Production Environment

**Using Let's Encrypt (Free SSL Certificates):**

1. **Install Certbot:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx
```

2. **Obtain Certificate:**
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

3. **Auto-renewal:**
```bash
sudo certbot renew --dry-run
# Add to crontab for automatic renewal
0 0 * * * certbot renew --quiet
```

### Web Server Configuration

#### Nginx Configuration

**Basic HTTPS Configuration:**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Certificate paths (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # HSTS Header (if not using Django setting)
    # add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # Django application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static files
    location /static/ {
        alias /path/to/your/staticfiles/;
    }
    
    # Media files
    location /media/ {
        alias /path/to/your/media/;
    }
}
```

#### Apache Configuration

**Basic HTTPS Configuration:**
```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # Redirect HTTP to HTTPS
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem
    
    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    
    # Django application
    WSGIDaemonProcess yourapp python-path=/path/to/project
    WSGIProcessGroup yourapp
    WSGIScriptAlias / /path/to/project/wsgi.py
    
    <Directory /path/to/project>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    
    # Static files
    Alias /static /path/to/staticfiles
    <Directory /path/to/staticfiles>
        Require all granted
    </Directory>
    
    # Media files
    Alias /media /path/to/media
    <Directory /path/to/media>
        Require all granted
    </Directory>
</VirtualHost>
```

## Production Deployment Checklist

### Pre-Deployment

- [ ] SSL/TLS certificates obtained and installed
- [ ] Web server (Nginx/Apache) configured for HTTPS
- [ ] Certificates tested and valid
- [ ] All subdomains have valid SSL certificates (if using SECURE_HSTS_INCLUDE_SUBDOMAINS)

### Django Settings Update

Update `settings.py` for production:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS Settings
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# HSTS Settings
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Post-Deployment Testing

1. **Test HTTP to HTTPS Redirect:**
```bash
curl -I http://yourdomain.com
# Should return 301 redirect to https://
```

2. **Verify HSTS Header:**
```bash
curl -I https://yourdomain.com | grep -i strict-transport
# Should show: Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

3. **Check SSL Certificate:**
```bash
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
# Should show valid certificate information
```

4. **Test Secure Cookies:**
```bash
curl -I https://yourdomain.com
# Check Set-Cookie headers include 'Secure' flag
```

5. **Browser Testing:**
- Visit http://yourdomain.com - should redirect to https://
- Verify padlock icon appears in browser
- Check certificate details in browser
- Test login and session persistence

6. **SSL Labs Test:**
Visit https://www.ssllabs.com/ssltest/ and test your domain for SSL configuration quality.

## Troubleshooting

### Issue: Redirect Loop

**Symptoms:** Browser shows "too many redirects" error

**Causes:**
- Load balancer or reverse proxy already handling HTTPS
- SECURE_SSL_REDIRECT enabled without proper HTTPS configuration

**Solutions:**
```python
# If behind a load balancer that handles SSL:
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Or disable SECURE_SSL_REDIRECT and handle redirects at web server level
SECURE_SSL_REDIRECT = False
```

### Issue: Mixed Content Warnings

**Symptoms:** Browser shows mixed content warnings, some resources don't load

**Causes:** 
- Some resources (images, scripts, CSS) loaded over HTTP instead of HTTPS

**Solutions:**
- Update all URLs in templates to use HTTPS or protocol-relative URLs
- Use Django's `{% static %}` template tag
- Check external resources (CDNs, APIs) support HTTPS

### Issue: HSTS Preventing Access

**Symptoms:** Cannot access site even after disabling HSTS

**Causes:**
- Browser has cached HSTS policy
- Certificate expired or invalid

**Solutions:**
1. Clear HSTS settings in browser:
   - Chrome: chrome://net-internals/#hsts → Delete domain
   - Firefox: Clear recent history → Cookies
2. Fix SSL certificate issues
3. Wait for HSTS max-age to expire

### Issue: Subdomains Not Accessible

**Symptoms:** Subdomains show SSL errors or are inaccessible

**Causes:**
- SECURE_HSTS_INCLUDE_SUBDOMAINS enabled but not all subdomains have SSL

**Solutions:**
- Obtain SSL certificates for all subdomains
- Use wildcard certificate: `*.yourdomain.com`
- Disable SECURE_HSTS_INCLUDE_SUBDOMAINS if needed

## Security Best Practices

1. **Always use HTTPS in production** - Never transmit sensitive data over HTTP
2. **Keep certificates up to date** - Set up automatic renewal
3. **Use strong SSL/TLS protocols** - Disable SSLv3, TLS 1.0, TLS 1.1
4. **Test before enforcing HSTS** - Start with short max-age values
5. **Monitor certificate expiration** - Set up alerts 30 days before expiration
6. **Use HTTP/2** - Improves performance with HTTPS
7. **Implement CSP** - Content Security Policy (already configured in Task 2)
8. **Regular security audits** - Use tools like SSL Labs, Mozilla Observatory

## Environment-Specific Configuration

### Using Environment Variables

**Recommended approach for managing settings across environments:**

```python
import os

# .env file or environment variables:
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', 'False') == 'True'
CSRF_COOKIE_SECURE = os.environ.get('DJANGO_CSRF_COOKIE_SECURE', 'False') == 'True'
SESSION_COOKIE_SECURE = os.environ.get('DJANGO_SESSION_COOKIE_SECURE', 'False') == 'True'
```

### Development Settings (local)
```bash
export DJANGO_DEBUG=True
export DJANGO_SECURE_SSL_REDIRECT=False
export DJANGO_CSRF_COOKIE_SECURE=False
export DJANGO_SESSION_COOKIE_SECURE=False
```

### Production Settings
```bash
export DJANGO_DEBUG=False
export DJANGO_SECURE_SSL_REDIRECT=True
export DJANGO_CSRF_COOKIE_SECURE=True
export DJANGO_SESSION_COOKIE_SECURE=True
```

## Additional Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [OWASP Transport Layer Protection](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)
- [HSTS Preload List](https://hstspreload.org/)
- [SSL Labs Server Test](https://www.ssllabs.com/ssltest/)

## Summary

This implementation provides:
- ✅ Automatic HTTP to HTTPS redirection (when enabled)
- ✅ HTTP Strict Transport Security (HSTS) with 1-year duration
- ✅ HSTS coverage for all subdomains
- ✅ HSTS preload support for maximum security
- ✅ Secure cookie transmission over HTTPS only
- ✅ Comprehensive documentation and deployment guidance
- ✅ Troubleshooting guides for common issues
- ✅ Environment-specific configuration recommendations

All settings are currently disabled for development but are documented and ready to enable in production with proper SSL/TLS configuration.
