# S-Box Tester (Analisis Kriptografi S-Box)

**Deskripsi Proyek:** Ini adalah aplikasi web yang dirancang untuk menganalisis dan menghitung berbagai properti kriptografi dari Substitution Boxes (S-boxes). S-box adalah komponen penting dalam banyak algoritma enkripsi simetris seperti AES, DES, dll. Aplikasi ini memungkinkan pengguna untuk memuat S-box bawaan atau memasukkan S-box kustom, kemudian menghitung berbagai metrik kriptografi penting untuk mengevaluasi kekuatan dan kualitas kriptografi dari S-box tersebut.

A web application for computing cryptographic properties of S-boxes. This tool allows you to analyze predefined S-boxes or custom ones by calculating various cryptographic metrics.

## Features

- Load predefined S-boxes (S-box2, S-box3) from JSON files
- Input custom S-boxes manually
- Compute comprehensive cryptographic metrics:
  - Nonlinearity (NL)
  - Strict Avalanche Criterion (SAC)
  - Bit Independence Criterion - Nonlinearity (BIC-NL)
  - Bit Independence Criterion - SAC (BIC-SAC)
  - Linear Approximation Probability (LAP)
  - Differential Approximation Probability (DAP)
  - Differential Uniformity (DU)
  - Algebraic Degree (AD)
  - Transparency Order (TO)
  - Correlation Immunity (CI)

## Installation

1. Clone or create the project directory
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask application:
   ```bash
   python backend/app.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`

3. Choose an S-box to analyze:
   - Select a predefined S-box from the dropdown and click "Load S-box"
   - Or manually enter a custom S-box with 256 comma-separated values between 0-255

4. Click "Compute Metrics" to see the cryptographic analysis

## Project Structure

```
sbox-tester/
├── backend/
│   ├── app.py              # Flask application
│   ├── sbox_metrics/       # Metric calculation modules
│   │     ├── nl.py         # Nonlinearity
│   │     ├── sac.py        # Strict Avalanche Criterion
│   │     ├── bic.py        # Bit Independence Criterion
│   │     ├── lap.py        # Linear Approximation Probability
│   │     ├── dap.py        # Differential Approximation Probability
│   │     ├── du.py         # Differential Uniformity
│   │     ├── ad.py         # Algebraic Degree
│   │     ├── to_metric.py  # Transparency Order
│   │     ├── ci.py         # Correlation Immunity
│   │     └── utils.py      # Utility functions
│   └── sboxes/             # Predefined S-boxes in JSON
│         ├── sbox2.json
│         └── sbox3.json
├── frontend/
│   ├── index.html          # Main HTML page with HTMX
│   └── static/
│       └── style.css       # Custom styles
├── requirements.txt        # Python dependencies
└── README.md             # This file
```

## Requirements

- Python 3.7+
- Flask
- NumPy

## Metrics Explained

- **Nonlinearity (NL)**: Measures how far the S-box is from linear functions
- **Strict Avalanche Criterion (SAC)**: Measures output bit changes when input bits are flipped
- **Bit Independence Criterion (BIC)**: Measures independence of output bits
- **Linear Approximation Probability (LAP)**: Measures linear biases in the S-box
- **Differential Approximation Probability (DAP)**: Measures differential biases
- **Differential Uniformity (DU)**: Measures differential resistance
- **Algebraic Degree (AD)**: Degree of the algebraic normal form
- **Transparency Order (TO)**: Measures resistance to side-channel attacks
- **Correlation Immunity (CI)**: Measures independence from input subsets

## License

This project is available for educational and research purposes.