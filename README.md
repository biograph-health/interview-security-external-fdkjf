Security Engineering Coding Interview
This repository contains a simple Flask application with several security vulnerabilities, including some from the OWASP Top Ten. Your task is to identify at least three vulnerabilities in the code and choose two of them to fix. For each vulnerability you identify, explain the risk it poses, and for the ones you fix, describe your remediation approach.
Setup

Clone the repository.
Install the requirements: pip install -r requirements.txt
Run the application: python app.py
Access the app at http://localhost:5000

Vulnerabilities
The application contains vulnerabilities such as:

SQL injection
Cross-site scripting (XSS)
Insecure direct object reference (IDOR)
Missing security headers

Task

Identify and fix three vulnerabilities in the code.
