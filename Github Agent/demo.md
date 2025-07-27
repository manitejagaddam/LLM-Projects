
---

## 🌸 Project 1: Iris Flower Classification

### 📌 Problem Statement

Classify Iris flowers into one of three species:
- Setosa
- Versicolor
- Virginica

### 📂 Dataset

- **File**: `Iris.csv`
- **Source**: [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/iris)

### 🛠️ Techniques Used

- Data Preprocessing
- Label Encoding
- Model Training (Logistic Regression / Decision Tree / Random Forest)
- Train-Test Splitting
- Accuracy Score and Confusion Matrix

---

## 🏠 Project 2: House Price Prediction Web App

### 📌 Problem Statement

Predict the price of a house based on input features and serve the model through a web interface.

### 📂 Dataset

- **File**: `ParisHousing.xls`
- **Type**: Synthetic dataset containing housing attributes.

### ⚙️ Model & Deployment

- Model is built using regression techniques.
- Trained and serialized using `pickle` as `house_pred.pkl`.
- Deployed via a **Flask** app using `main.py`.

### 🌐 Web Interface

- HTML Template: `templates/index.html`
- Backend: Python + Flask
- Input: User form with housing features
- Output: Predicted price on screen

---

## 🚀 How to Run the Web App

### 🔧 Requirements

Install the following Python packages:

```bash
pip install flask pandas scikit-learn numpy
