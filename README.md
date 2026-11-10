# Clinical IVF Morphokinetics & Reproductive AI Platform 🔬

<p align="left">
  <img src="https://img.shields.io/badge/Domain-Clinical%20IVF%20%26%20Embryology-06B6D4?style=flat-square" alt="Domain">
  <a href="EU_AI_ACT_TECHNICAL_DOCUMENTATION.md"><img src="https://img.shields.io/badge/EU%20AI%20Act-High--Risk%20(Class%20IIa/IIb)-10B981?style=flat-square" alt="EU AI Act"></a>
  <a href="docs/adr/"><img src="https://img.shields.io/badge/Architecture-ADRs-8B5CF6?style=flat-square" alt="ADRs"></a>
  <img src="https://img.shields.io/badge/Standards-Gardner%20Staging%20%7C%20ESHRE-EC4899?style=flat-square" alt="Standards">
  <img src="https://img.shields.io/badge/Privacy-GDPR%20Art.%209%20%7C%20HIPAA-F59E0B?style=flat-square" alt="Privacy">
</p>

A production-grade, clinical computer vision platform for non-invasive **blastocyst grading**, **embryo developmental morphokinetics**, and **implantation potential scoring** from time-lapse microscopy imaging. Architected as an **EU AI Act High-Risk Clinical Decision Support System** adhering to strict GDPR Article 9 health data privacy and international ESHRE consensus guidelines.

---

## 📑 Table of Contents
- [Clinical Background & Objectives](#-clinical-background--objectives)
- [System Architecture](#-system-architecture)
- [Key Capabilities](#-key-capabilities)
- [EU AI Act & Regulatory Governance](#-eu-ai-act--regulatory-governance)
- [Quick Start](#-quick-start)
- [Architecture Decision Records (ADRs)](#-architecture-decision-records)
- [License](#-license)

---

## 🔬 Clinical Background & Objectives

In In-Vitro Fertilization (IVF) cycles, selecting the embryo with the highest developmental competence for single embryo transfer (SET) is critical to achieving successful live births while avoiding multiple pregnancies.

Traditional manual grading under an optical microscope suffers from **high inter- and intra-observer subjectivity**. This platform automates the objective analysis of:
1. **Morphological Staging**: High-resolution segmentation of the **Inner Cell Mass (ICM)** (destined to form the fetus) and **Trophectoderm (TE)** (destined to form the placenta) according to the standard **Gardner Criteria** (Expansion 1–6, ICM A–C, TE A–C).
2. **Time-Lapse Morphokinetics**: Tracking cell cleavage milestones ($t_2, t_3, t_4, t_8, t_{SB}, t_B$) to evaluate cell cycle synchrony ($s_2$) and cell cycle duration ($cc_2$).
3. **Clinical Decision Support**: Synthesizing morphological and kinetic markers to generate an objective implantation viability score with human-in-the-loop oversight.

---

## 🏗️ System Architecture

```
Time-Lapse Ingestion (DICOM / TIFF)
         │
         ▼
[GDPR Art. 9 De-Identification Layer] (PHI Strip & Cryptographic Hash)
         │
         ▼
[Attention U-Net Segmentation Engine]
 ├── Zona Pellucida (ZP)
 ├── Inner Cell Mass (ICM)
 ├── Trophectoderm (TE)
 └── Blastocoel Cavity
         │
         ├───▶ [Morphokinetic Tracker] ──▶ ($cc_2 = t_3 - t_2$, $s_2 = t_4 - t_3$)
         │
         └───▶ [Gardner Staging Engine] ──▶ (Expansion, ICM Quality, TE Quality)
                     │
                     ▼
       [Clinical Viability Prognosis]
                     │
                     ▼
  [EU AI Act Art. 14 Human Oversight Gate]
```

---

## 🚀 Quick Start

1. **Clone & Setup**:
   ```bash
   git clone https://github.com/FirdowsRahaman/clinical-ivf-morphokinetics-ai.git
   cd clinical-ivf-morphokinetics-ai
   pip install -r requirements.txt
   ```

2. **Run End-to-End Diagnostic Pipeline Demo**:
   ```bash
   python demo/pipeline.py
   ```

---

## 🏛️ EU AI Act & Regulatory Governance
- Full technical documentation available in [**`EU_AI_ACT_TECHNICAL_DOCUMENTATION.md`**](EU_AI_ACT_TECHNICAL_DOCUMENTATION.md).
- Architectural decisions documented in [**`docs/adr/`**](docs/adr/).
- Strict compliance with Human Oversight (Article 14) and Clinical Cybersecurity (Article 15).

---

## 📄 License
This project is licensed under the MIT License.
