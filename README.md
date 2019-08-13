# httPython

#### Description
Web-application emulating client-server relationships via Python modules HTTPServer and BaseHTTPRequestHandler.

#### Startup
To run the server use `python3 path/server.py portnumber` command. `portnumber` has 8001 as a default value, so this argument is optional.

#### About
Application has 5 pages: ___charge___, ___error___, ___form___, ___logIn___ and ___logOut___. ___logIn___ and ___logOut___ are responsible for authorisation processes, ___charge___ prints success message in case user was authorised, otherwise warning message will be shown. From ___form___ you can go to this pages by clicking the corresponding buttons.
