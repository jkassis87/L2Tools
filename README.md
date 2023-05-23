# ShellShorts
A web app for running common series's of ssh commands used for managing cPanel servers and providing the required output. Avoids the task of these repeatable tasks manually and retrieving them from the shell.

New web pages and commands can be added by updating the app/routes.py file.

NOTE: Tool runs on local host with the default Flask port. This shouldn't be exposed to the internet on ports 80/443 as that could leak the private key.
