# Run
- Run `aria2c xmlrpc` server (using `start_rpc_server.cmd` on windows)
- Run `backend/main.py` using python
- Run `frontend/` using `npm start`


<br /><br />


# Changing Host/Ports
### FLASK (PYTHON)

in anime-tracker-web/backend/conf.json
```json
{
    ...
    "python_server_host": "<New Host>",
    "python_server_port": "<New Port>"
}
```

in anime-tracker-web/frontend/src/config/config.js
```javascript
export const backendBaseURL = "<Your New (Python) Host:Port>"
````

<br />

### React App
in anime-tracker-web/frontend/package.json
```json
{
    ...
    "scripts": {
        "start": "PORT=<New Port> react-scripts start",
        "build": "react-scripts build",
        "test": "react-scripts test",
        "eject": "react-scripts eject"
    },
    ...
}
```

in anime-tracker-web/backend/conf.json
```json
{
    ...
    "react_server_url": "http://localhost:<New Port>",    
    ...
}
```