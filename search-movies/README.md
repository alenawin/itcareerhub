# 🎬 Film Search Console

A **console-based Python application** for searching movies by keyword, genre, and release year.  
Uses **MySQL** as the main movie database and **MongoDB** for logging and tracking search statistics.

---

## 🚀 Features

- Search movies by **keyword**
- Search by **genre** and **year range**
- View **popular** and **recent** search queries
- Automatically log all searches in **MongoDB**
- Nicely formatted **console output**

---

## 🧱 Project Structure
```
project/
│
├── main.py # Main program: menu and logic
├── formatter.py # Output formatting and table display
├── mysql_connector.py # MySQL database access (films, genres, years)
├── mongo_connector.py # MongoDB access (logs, analytics)
├── .env # Configuration file with credentials
└── README.md # Project description
```
