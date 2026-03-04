# Aubree Rose Valencia Shop

A simple **React + Firebase E-Commerce application** that allows users to browse products, create accounts, login, and manage a shopping cart. Products and users are stored in **Firebase Cloud Firestore**, and authentication is handled using **Firebase Authentication**.

---

## Project Overview

This project demonstrates how to integrate **Firebase services into a modern React application**. The application allows users to:

- Browse products stored in Firestore
- Create a user account
- Login securely
- Add items to a shopping cart
- View and manage cart items

Firebase handles both **authentication and backend database storage**, making the application scalable and easy to manage.

---

## Technologies Used

- React
- Vite
- Firebase Authentication
- Firebase Firestore
- React Router
- JavaScript (ES6)

---

## Features

### User Authentication

Users can create an account and login using **Firebase Authentication (Email & Password)**.

When a new user registers:

1. Firebase Authentication creates the user.
2. A matching document is automatically created in the **Firestore `users` collection**.

Example:

```
users
   userUID
      email
      createdAt
```

---

### Product Storage

Products are stored in **Firestore** inside the `products` collection.

Example:

```
products
   productID
      name
      price
      category
      image
```

These products are loaded dynamically into the React application.

---

### Shopping Cart

Users can:

- Add items to cart
- Adjust quantities
- View total price

Cart state is managed using **Redux / state management in Rea**
