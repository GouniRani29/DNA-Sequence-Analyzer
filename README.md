# 🧬 DNA Sequence Analyzer Using Transformer Deep Learning

A web-based DNA sequence analysis and classification system that uses **Transformer Deep Learning** to analyze DNA sequences and predict their target class.

---

## 📌 Overview

The **DNA Sequence Analyzer** allows users to enter a DNA sequence containing the nucleotide bases **A, T, G, and C**.

The system processes the sequence using **6-mer tokenization**, converts the tokens into embeddings, and uses a **Transformer-based classification model** to predict the sequence class.

The application combines a React frontend, Spring Boot backend, Python ML service, and MySQL database.

---

## 🎯 Objectives

- Analyze and preprocess DNA sequences.
- Convert DNA sequences into overlapping 6-mer tokens.
- Classify DNA sequences into seven target classes.
- Apply Transformer-based deep learning for sequence classification.
- Evaluate model performance using standard classification metrics.
- Provide a simple web interface for DNA sequence analysis.

---

## 🧬 Dataset

The dataset contains:

| Property | Details |
|---|---|
| Total sequences | 4,380 |
| Number of classes | 7 |
| Sequence type | DNA |
| DNA bases | A, T, G, C |
| Tokenization | Overlapping 6-mers |

### Example

For the DNA sequence:

```text
ATGCGTAC

---

## 🏗️ System Architecture

The system follows a three-layer architecture consisting of the React frontend, Spring Boot backend, and Python machine learning service.

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │  React Frontend │
                  │    (Vite)       │
                  └────────┬────────┘
                           │
                           │ REST API
                           ▼
                  ┌─────────────────┐
                  │ Spring Boot     │
                  │    Backend      │
                  └────────┬────────┘
                           │
                           │ REST API
                           ▼
                  ┌─────────────────┐
                  │  Flask ML       │
                  │    Service      │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ DNA Preprocessing│
                  │   & 6-mer       │
                  │  Tokenization   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   Transformer   │
                  │     Model       │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Classification  │
                  │     Head        │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Prediction +    │
                  │   Confidence    │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Spring Boot +   │
                  │     MySQL       │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ React Frontend  │
                  │ Display Result  │
                  └─────────────────┘
User enters DNA sequence
          ↓
React Frontend
          ↓
Spring Boot REST API
          ↓
Flask ML Service
          ↓
DNA Validation & Preprocessing
          ↓
6-mer Tokenization
          ↓
Token Embedding
          ↓
Positional Encoding
          ↓
Transformer Encoder
          ↓
Classification Head
          ↓
Softmax Probabilities
          ↓
Predicted Class
          ↓
Confidence Score
          ↓
Spring Boot
          ↓
MySQL
          ↓
React Frontend
          ↓
Display Result
