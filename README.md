# Run
- Run `aria2c xmlrpc` server (using `start_rpc_server.cmd` on windows)
- Run `docker-compose up` in `docker-compose.yml` directory


<br />

# Changing Host/Ports
It's now from docker-compose.yml

# Other notes
```yml
extra_hosts:
    - "host.docker.internal:host-gateway"
```
I have two containers that use Aria2, So, I run it on localhost and access it from the containers using `http://host.docker.internal:6800/rpc` as in `backend/conf.json`. If you want to dockerize Aria2 as well, you wont need that part. Just make sure to change `backend/conf.json-aria2_xmlrpc_server_url` accordingly.