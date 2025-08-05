# 🛒 SohamMart – Django E-Commerce Website

A fully functional e-commerce web application built with **Django**, designed for both users and sellers. Users can browse products, manage carts, place orders, and sellers can manage their inventory. Includes user authentication, admin panel, and checkout flow.

---

## 🔥 Features

### 👨‍💼 User Side
- Signup / Login / Logout
- Browse all products
- Add to Cart
- Increase / Decrease Quantity
- Remove from Cart / Empty Cart
- Checkout with address & phone
- Order tracking (My Orders)

### 🛍️ Seller Side
- Add New Product
- Edit Product Details
- Delete Products
- View All Orders (Admin Panel)

### 🛠️ Admin Panel
- Access all orders placed
- View users and products
- Modify database via Django admin

---

## 📂 Tech Stack

| Layer         | Tech                     |
|---------------|--------------------------|
| Backend       | Django (Python)          |
| Frontend      | HTML, CSS, Bootstrap     |
| Database      | SQLite                   |
| Auth          | Django Auth (Sessions)   |

---

## 📁 Folder Structure

ecommerce_site/
│
├── store/
│ ├── migrations/
│ ├── templates/store/
│ │ ├── index.html
│ │ ├── cart.html
│ │ ├── checkout.html
│ │ ├── login.html
│ │ ├── signup.html
│ │ ├── product_form.html
│ │ └── my_orders.html
│ ├── static/css/style.css
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ └── forms.py
│
├── ecommerce_site/
│ └── settings.py
│
├── db.sqlite3
└── manage.py

---