# EPG Proxy Server 

## Development setup
To run the development server 
- Start Docker Compose with the command ```docker-compose up```
- To rebuild container ```docker-compose up --build```

## Notes
- There are two flask application config, one at `app.py` and the other at `mock_server.py` <br>
- The main application to be deployed is at `app.py`
- The server at `mock_server.py` is just a way to mock the provider source response.
- The whitlisted channels name/id should be written in the `whitelisted_channel.txt` file.
- The `Dockerfile` is the main dockerfile for this project and it is deployment-ready
- The `nginx.conf` is valid and `proxy_pass` address should be changed on main server to `http://localhost:8080` (EC2)

## Running on Rocky 8
- You need to first install all the packages specified in the `requirements.txt`
- Run the `start-on-rocky.sh` file
- first, make the script executable `chmod +x start-on-rocky.sh`
- Run the script `./start-on-rocky.sh`
- Visit `http://localhost:8080`

## Logging
- There are several log levels which can be configured
- Log levels includes `Debug`, `Info`, `Warning`, `Error`, `Extract`
- To set the log level, add the `log` query parameter
- For example, http://127.0.0.1:5000/?large&log=extract where `large` is the source and `extract` is the log level.

