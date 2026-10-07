<div align="center">

# 🗄️ SQL Server Project

**A hands-on training project focused on SQL Server: schema design, queries, and exercises.**

[![SQL Server](https://img.shields.io/badge/SQL%20Server-CC2927?style=flat&logo=microsoftsqlserver&logoColor=white)](#)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](#)
[![T-SQL](https://img.shields.io/badge/T--SQL-336791?style=flat&logo=microsoftsqlserver&logoColor=white)](#)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat)](#)

<br>

[![Stars](https://img.shields.io/github/stars/RufusTheDwarf/SQL_Server_project?style=flat&color=yellow)](https://github.com/RufusTheDwarf/SQL_Server_project/stargazers)
[![Forks](https://img.shields.io/github/forks/RufusTheDwarf/SQL_Server_project?style=flat&color=blue)](https://github.com/RufusTheDwarf/SQL_Server_project/forks)
[![Issues](https://img.shields.io/github/issues/RufusTheDwarf/SQL_Server_project?style=flat&color=red)](https://github.com/RufusTheDwarf/SQL_Server_project/issues)
[![Last Commit](https://img.shields.io/github/last-commit/RufusTheDwarf/SQL_Server_project?style=flat&color=orange)](https://github.com/RufusTheDwarf/SQL_Server_project/commits/main)

</div>

---

## 📖 Overview

**SQL Server Project** is a personal training repository dedicated to mastering **SQL Server** and **T-SQL**. It contains a collection of exercises, database schemas, and Python scripts designed to generate test data and automate database creation.

The project is a practical playground for exploring relational database concepts, from basic table creation to advanced querying and data manipulation. It is constantly evolving as new exercises and scenarios are added.

<br>

## ✨ Features

| Feature | Description |
|---|---|
| **Database Schema Design** | Complete T-SQL scripts to create databases, tables, constraints, and relationships. |
| **Python Data Generation** | Scripts that automatically generate realistic test data for the database. |
| **Query Exercises** | A set of SQL queries covering joins, subqueries, aggregations, and window functions. |
| **Investigation Scenario** | A fun "find the cheaters" exercise using SQL queries to solve a mystery. |
| **Open House Project** | A complete database project simulating a school open house event, including a local Flask interface for detecting suspicious players. |
| **Documentation** | Installation guides, admin manuals, and visitor manuals for the open house project. |

<br>

## 🗂️ Project Structure

```text
SQL_Server_project/
├── archive/
├── version-finale/
│   ├── 01-script-generation-bd/     # Database and data generation
│   └── portes-ouvertes/              # Local Flask open house interface
├── archive/
│   └── ...                           # Archived project files
│   ├── Y-141-Rafael_Melo-*.sql      # SQL scripts
│   ├── Y-141-Rafael_Melo-*.py       # Python generation scripts
│   └── *.docx                       # Reports and documentation
├── LICENSE
└── README.md
```

<br>

## 🚀 Getting Started

### Prerequisites

- **SQL Server** (Express, Developer, or Standard edition)
- **SQL Server Management Studio (SSMS)** or **Azure Data Studio**
- **Python 3.8+** with `pyodbc` or `pymssql` (for data generation scripts)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RufusTheDwarf/SQL_Server_project.git
   cd SQL_Server_project
   ```

2. **Create the database**
   - Open SSMS and connect to your SQL Server instance.
   - Run the SQL scripts located in the `archive/` folder to create the schema and tables.

3. **Generate test data (optional)**
   ```bash
   pip install pyodbc
   python archive/Y-141-Rafael_Melo-GenerationBd.py
   ```

4. **Run the queries**
   - Open the query files and execute them in SSMS to explore the data.

5. **Run the Open House interface**
   - Open `version-finale/portes-ouvertes/`
   - Install dependencies:
     `python -m pip install -r requirements.txt`
   - Start the interface:
     `python app.py`
   - Open `http://127.0.0.1:5000` in a browser.
   - Default SQL Server instance: `./SQLEXPRESS`
   - Database: `SQL_Server_Project`
   - ODBC driver: `ODBC Driver 17 for SQL Server`
   - The interface is read-only and uses parameterized SELECT queries.
   - Suspicion is calculated with a score based on the selected criteria.

<br>

## 🛠️ Technologies

| Category | Technology |
|---|---|
| **Database** | Microsoft SQL Server |
| **Query Language** | T-SQL |
| **Scripting** | Python 3 |
| **Tools** | SSMS, Azure Data Studio, Git |

<br>

## 📚 What You Will Find

- **DDL Scripts** : `CREATE DATABASE`, `CREATE TABLE`, `ALTER TABLE`, and constraint definitions.
- **DML Scripts** : `INSERT`, `UPDATE`, `DELETE`, and `MERGE` statements.
- **Query Exercises** : `SELECT` with joins, subqueries, `GROUP BY`, `HAVING`, and window functions.
- **Python Automation** : Scripts that connect to SQL Server and generate test data.
- **Scenarios** : Real-world inspired exercises like the "cheater investigation" and the "open house" database.

<br>

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a branch:
   ```bash
   git checkout -b feature/my-feature
   ```
3. Commit your changes:
   ```bash
   git add .
   git commit -m "Add my feature"
   ```
4. Push the branch:
   ```bash
   git push origin feature/my-feature
   ```
5. Open a Pull Request.

<br>

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

<div align="center">

### 👤 Author

**RufusTheDwarf**

[![GitHub](https://img.shields.io/badge/GitHub-RufusTheDwarf-181717?style=flat&logo=github&logoColor=white)](https://github.com/RufusTheDwarf)
[![Repository](https://img.shields.io/badge/Repo-SQL__Server__project-2ea44f?style=flat&logo=git&logoColor=white)](https://github.com/RufusTheDwarf/SQL_Server_project)

<br>

### 💖 Acknowledgements

- The **SQL Server community** for the endless documentation and resources.
- **Microsoft** for SQL Server and the free Developer edition.
- Everyone who shares SQL tips and tricks online.

<br>

### ⭐ Show Your Support

If this project helped you learn something new, consider giving it a star.

[![Star this repo](https://img.shields.io/badge/⭐_Star_this_repo-yellow?style=flat)](https://github.com/RufusTheDwarf/SQL_Server_project/stargazers)
[![Report an issue](https://img.shields.io/badge/🐛_Report_an_issue-red?style=flat)](https://github.com/RufusTheDwarf/SQL_Server_project/issues)
[![Fork this repo](https://img.shields.io/badge/🍴_Fork_this_repo-blue?style=flat)](https://github.com/RufusTheDwarf/SQL_Server_project/fork)

<br>

---

<sub>Made with ❤️ and a lot of SQL by **RufusTheDwarf** · Licensed under MIT · © 2026</sub>

<br>

*"In SQL we trust."* 🗄️

</div>
