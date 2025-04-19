# Data Analytics

## 📊 Overview

**DataAnalytics** is a modular and interactive data analysis platform built with Python. It leverages **Streamlit** for the user interface, enabling users to perform data exploration, preprocessing, and machine learning tasks seamlessly. The platform is designed to be extensible, allowing for easy integration of new features and models.

This project was developed as a **class-wide assignment** for the **Object-Oriented Programming in Python** course during our **Master’s program**. It involved collaborative efforts from all students to design and build a robust analytical tool from scratch.


## 🚀 Getting Started
### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)


### Installation
1. Clone the repository:
```bash 
git clone https://github.com/rishitiwari08/DataAnalytics.git
cd DataAnalytics
```
2. Create a Virtual environment:
```bash 
python -m venv .venv
```
3. Activate the virtual environment:
    - On Unix or MacOS:
    ```bash
    source .venv/bin/activate
    ```
    - On Windows:
    ```bash
    .venv\Scripts\activate
    ``` 
4. Install the required dependencies:
```bash
pip install -r requirements.txt
```


### Running the Application
Start the Streamlit application:

```bash
streamlit run Home.py
```
The application will open in your default web browser, providing an interactive interface for data analysis.

## 📁 Project Structure
```arduino
DataAnalytics/
├── data/                   # Sample datasets for analysis
├── pages/                  # Additional Streamlit pages
├── src/                    # Core source code modules
├── tests/                  # Unit tests for the application
├── Presentations/          # Presentation materials and reports
├── Home.py                 # Main Streamlit application entry point
├── requirements.txt        # Python dependencies
└── README.md               # Project overview and instructions
```

- data/: Contains sample datasets used within the application.

- pages/: Houses additional Streamlit pages for modular functionality.
- src/: Includes core modules such as data processing, visualization, and machine learning algorithms.

- tests/: Contains unit tests to ensure code reliability.

- Presentations/: Stores presentation slides and related materials.

- Home.py: The main entry point for the Streamlit application.

- requirements.txt: Lists all Python dependencies required to run the project.

## 🧰 Features
- Interactive data visualization and exploration

- Data preprocessing tools

- Machine learning model training and evaluation

- Modular design for easy extension

- User-friendly interface with Streamlit
