# http_https_response_time_exporter

Docker image for getting HTTP/HTTPS response time as metric and put it into Pushgateway

#### Usage
###### Environment
- INTERVAL : the time between each pushing to Pushgateway (in second)
- URL : your http/https service URL
- PUSHGATEWAY : your Pushgateway URL
- DOCKERSERVICE : your http/https service name

```yaml
version: '3.3'
services:
  response_time_exporter:
    image: tinhgin/http_https_response_time_exporter:latest
    environment:
      - INTERVAL=10
      - URL=https://yoursite.example.com
      - PUSHGATEWAY=http://pushgateway.example.com
      - DOCKERSERVICE=PROJECTA_web
```

```bash
docker run -d -e INTERVAL=10 -e URL=https://yoursite.example.com -e PUSHGATEWAY=http://pushgateway.example.com -e DOCKERSERVICE=PROJECTA_web tinhgin/http_https_response_time_exporter:latest 
```