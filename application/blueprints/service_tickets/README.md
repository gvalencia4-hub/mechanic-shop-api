# My Mechanic Shop API

## Overview

This is a Flask REST API for managing a mechanic shop system. It supports customers, mechanics, service tickets, inventory, authentication, rate limiting, caching, and pagination.

## Features

- Customer CRUD
- Mechanic CRUD
- Service ticket CRUD
- Inventory CRUD
- Add and remove mechanics from tickets
- Add inventory parts to tickets
- Customer login with token authentication
- Protected route for customer tickets
- Rate limiting on login
- Caching on customer list route
- Pagination on customer list route
- Mechanics ranking by ticket count

## Tech Stack

- Flask
- SQLAlchemy
- Marshmallow
- Flask-Limiter
- Flask-Caching
- Python-JOSE
- SQLite

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-github-repo-url>
cd my-mechanic-shop
```
