# httPython

#### Description
Web-application emulating client-server relationships via Python modules HTTPServer and BaseHTTPRequestHandler.

#### Startup
To run the server use `python3 path/server.py portnumber` command. `protnumber` has 8001 as a default value, so to run server on 8001 port you can just enter `python3 path/server.py`.

#### About
Application has 5 pages: ___charge___, ___error___, ___form___, ___logIn___ and ___logOut___. ___logIn___ and ___logOut___ are responsible for authorisation processes, ___charge___ prints success message in case user was authorised, otherwise warning message will be shown. From ___form___ you can go to this pages by clicking the corresponding buttons.

In this version ___charge___, ___logIn___ and ___logOut___ pages exist only on server with 8002 port, while ___form___ page is running on 8001'th. Apart from the fact application uses 2 servers now to reach it's full potential, some features were added to improve compatibility with different browsers and operational systems.

#### What's new
When user clicks `Log In`/`Log Out` button, instead of seeing new page pop-up window appears, notifying about current authorization status. Also, when user entered ___form___ page, clients machine automatically sends request to charge some money (amount shown in input field).
