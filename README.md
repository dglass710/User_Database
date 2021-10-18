# User_Database
This is a python script which allows users to create accounts with associated passwords, login, change passwords, and remove accounts. It does not store plain text passwords but instead stores the output of recursively calling sha512 10,000 times on a password, using hash matching to confirm the users input matches the initial password.
