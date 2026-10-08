# DNA Sequence Analyzer Using Transformer Deep Learning

A web-based DNA sequence analysis and classification system that uses deep learning and machine learning techniques to analyze DNA sequences and predict their class.

## 📌 Project Overview

The DNA Sequence Analyzer accepts a DNA sequence containing the nucleotide bases A, T, G, and C. The sequence is preprocessed and converted into k-mer representations before being passed to a trained classification model.

The project combines:

- React.js for the frontend
- Spring Boot for the backend
- Python Flask for the machine learning service
- PyTorch for the Transformer model
- MySQL for storing analysis results

The system provides the predicted class, confidence score, and sequence length through a simple web interface.

---

## 🎯 Objectives

1. **DNA Sequence Analysis**  
   Preprocess DNA sequences and convert them into meaningful k-mer representations.

2. **DNA Sequence Classification**  
   Classify DNA sequences into one of seven target classes using machine learning and Transformer-based deep learning.

3. **Model Evaluation**  
   Evaluate the classification models using metrics such as accuracy, precision, recall, and F1-score.

4. **Web Application Development**  
   Provide a user-friendly web application for submitting DNA sequences and viewing prediction results.

---

## 🧬 Dataset

The project uses a DNA sequence dataset containing:

- **4,380 DNA sequences**
- **7 target classes**
- DNA bases: A, T, G, C
- Variable-length DNA sequences

The sequences are converted into overlapping **6-mers** for feature representation.

### Example

DNA sequence:

```text
ATGCGTAC
