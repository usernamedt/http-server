Daniil Zakhlystov

**Python web server.**

Usage: python main.py


By default, listening on localhost:8080 

By default, static files should be placed at wwwroot folder

Default settings can be overriden by placing custom config.json in root folder


**Default options**
```javascript
{
  "port": 8080,
  "host": "",
  "threads_count": 15,
  "log_file": "log.txt",
  "max_req_time": 10,
  "queue_size": 5,
  "default_headers": {
    "Server": "PythonHTTPServer/0.1b"
  },
  "www_dir": "wwwroot",
  "log_file": "log.txt",
  "proxy_pass_mode": true,
  "proxy_pass_port": 80,
  "proxy_pass_host": "",
  "file_cache_size": 10,
  "file_cache_errors": true,
  "error_page_loc": "general_error.html"
}
```