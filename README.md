
# Cool Web Server

Author is Igor Okladnikov.

# Requirements

## General

- [x] Support Python 3.7+
- [x] Use venv during the development
- [x] Program must work both on Linux and Windows
- [x] Specify directory to keep manage files via CLI arguments
- [x] Cover functionality using `pytest`
- [ ] Deploy via Docker image (for those who is familiar with Docker)
- [x] Use `logging` module for logging

## File Service

- [x] Avoid usage of dangerous values like `../../../etc/passwd`
- [x] Support binary file content as well

## Configuration

- [x] Read settings from CLI arguments
- [x] Read settings from env vars
- [x] Read settings from config file

## Web Service

- [ ] Specify web-server port via CLI arguments
- [ ] Work independently without WSGI
- [ ] Suit with RESTful API requirements
- [ ] Use asynchronous programming concept (aiohttp?)
- [ ] Use multithreading for downloading files
- [ ] Partial file download (http range)

## Crypto Service

- [ ] Protect files by cryptography tools

## Auth Service

- [ ] Provide access to files via access policy
- [ ] Keep users in database
