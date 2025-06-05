# 🚀 Model-Context-Protocol-101

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/github/actions/workflow/status/itprodirect/Model-Context-Protocol-101/ci.yml)](https://github.com/itprodirect/Model-Context-Protocol-101/actions)
[![Dependencies](https://img.shields.io/badge/Dependencies-Updated-brightgreen.svg)](https://github.com/itprodirect/Model-Context-Protocol-101/blob/main/requirements.txt)

A step-by-step tutorial exploring the **Model Context Protocol (MCP)**. This repository serves as a structured learning guide for AI/ML practitioners, consultants, and developers interested in practical **MCP implementation**.

![Notebook demo](docs/img/notebook_screenshot.svg "Screenshot of notebook running a sales example")

---

## 📌 **Overview**
This repository covers:
✔️ Setting up a Python virtual environment for isolated development.  
✔️ Installing required dependencies using `pip install -r requirements.txt`.  
✔️ Understanding MCP concepts with practical code examples.  
✔️ Running Jupyter Notebooks for interactive experimentation.

---

## 🛠️ **Getting Started**
### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/itprodirect/Model-Context-Protocol-101.git
cd Model-Context-Protocol-101
```

### 2️⃣ **Create a Virtual Environment**
```bash
python -m venv venv
# On Mac/Linux
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

### 3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Run Jupyter Notebook**
```bash
jupyter notebook notebooks/Model-Context-Protocol-101.ipynb
```

### 5️⃣ **Run Tests**
```bash
pytest
```

---
## 🔑 Key Features

- 🚀 **MCP Server Setup**: Learn how to initialize and expand an MCP tool.
- 🔧 **Function Expansion**: Add custom tools and test them interactively.
- 📂 **CSV File Handling**: Automate CSV file reading and data extraction.
- 🎯 **Practical Exercises**: Hands-on coding exercises for better understanding.

---
## 🌟 Real-world Use Cases
Here are quick examples of how an independent insurance agent might apply MCP:
- **Automated Quotes** – load policy data from a CSV and generate quotes in seconds.
- **Lead Tracking** – triage new leads automatically using simple prompts.
- **Commission Insights** – compute profits and commissions with a single command.

![MCP flow](docs/img/architecture.svg "CSV data flowing through MCP tools to outputs")

---
## 📖 Usage Guide
This tutorial walks through how to:
✅ **Initialize the MCP Server**  
✅ **Test MCP tools locally**  
✅ **Expand MCP with custom functions**  
✅ **Read and process CSV files**  
✅ **Deploy and use MCP tools efficiently**  

---
## 📂 Project Structure
```
Model-Context-Protocol-101/
├── src/                # Python utilities
├── notebooks/          # Jupyter notebooks
├── data/               # Sample datasets
├── docs/img/           # Diagrams and screenshots
├── tests/              # Unit tests
├── README.md           # Documentation
├── requirements.txt    # Dependencies
├── LICENSE             # Project License
└── AGENTS.md           # Contribution guide
```

---
## 📚 Glossary
| Term    | Meaning                                |
| ------- | -------------------------------------- |
| **MCP** | Model Context Protocol, our tooling API |
| **Lead**| Potential client for an insurance policy|
| **Premium** | Amount a customer pays for coverage |

---
## 📝 License
This project is licensed under the **MIT License**.

---
## 🤝 Contributing
Contributions are welcome! Feel free to fork the repo, submit pull requests, or suggest improvements.

---
## 📬 Contact
For questions or collaborations, connect with me on **LinkedIn** or open an **Issue** in this repository.

---
🔥 *This README is designed for clarity, readability, and ease of navigation!* 🚀
