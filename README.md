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




