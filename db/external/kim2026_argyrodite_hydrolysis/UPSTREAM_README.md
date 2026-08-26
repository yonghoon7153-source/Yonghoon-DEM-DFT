# Deciphering Surface Hydrolysis Mechanism in Argyrodite via Large-Scale Machine Learning Potential Simulations

This repository contains the datasets and analysis files associated with the paper  
**“Deciphering Surface Hydrolysis Mechanism in Argyrodite via Large-Scale Machine Learning Potential Simulations.”**

The repository consists of two main directories:

---

## 📁 1. `MD_results`

This directory contains molecular dynamics (MD) simulation results for each reaction environment:

- **1_LPSC-H2O**  
- **2_LPSC-H3O+OH+H2O**  
- **3_LPSnSC-H3O+OH+H2O**

Each subdirectory includes:

- The final MD snapshot images  
- The fine-tuned universal machine learning potential (**uMLP**) used for the simulations  

> Note: The uMLP files for `1_LPSC-H2O` and `2_LPSC-H3O+OH+H2O` are identical.

---

## 📁 2. `validation`

This directory contains validation data used to evaluate the fidelity of the fine-tuned ML potentials.

Subdirectories:

- **1_LPSC_H-O**  
- **2_LPSnSC_H-O**

Each includes the following files:

- **checkpoint_best.pth** — Fine-tuned uMLP checkpoint  
- **combined.xyz** — Reference structures for DFT single-point energy validation  
- **correlation.py** — Python script used to generate validation correlation plots  
- **fine-tuned.png** — Visualization of validation results  
- **MD_fidelity_DFTvsMLP.csv** — Comparison of MLP vs DFT energies sampled from MD trajectories for fidelity assessment  

---
