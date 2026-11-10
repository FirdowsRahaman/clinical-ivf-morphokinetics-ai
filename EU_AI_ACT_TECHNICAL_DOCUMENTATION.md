# EU AI Act Technical Documentation (Clinical Diagnostic System)

**Regulation Reference**: Regulation (EU) 2024/1689 (EU AI Act)  
**MDR Reference**: Medical Device Regulation (EU) 2017/745 (MDR Class IIa/IIb Software)  
**System**: Clinical IVF Embryo Assessment & Morphokinetics AI Platform  
**Classification**: High-Risk AI System (Article 6 & Annex III, Point 5 / Medical Device AI)  
**Target Market**: European Union (EEA) & International Reproductive Health Clinics  

---

## 1. System Overview & Intended Clinical Purpose
The Clinical IVF Morphokinetics platform provides computer-aided decision support to reproductive biologists and clinical embryologists. It processes time-lapse microscopy imaging of human embryos from fertilization through Day 5/6 blastocyst expansion to:
1. Segment biological morphological landmarks (Inner Cell Mass, Trophectoderm, Zona Pellucida).
2. Quantify developmental cleavage timings and cell cycle intervals ($t_2, t_3, t_4, cc_2, s_2$).
3. Generate standardized Gardner staging predictions to aid embryologists in non-invasive embryo transfer prioritization.

**Clinical Contraindication**: This system is strictly an auxiliary diagnostic decision support tool. Autonomous selection or disposal of human embryos without explicit, qualified human embryologist review is strictly prohibited.

---

## 2. Article 10: Data Governance & Biological Provenance
1. **De-Identification by Design**: In compliance with GDPR Article 9 (Special Category Health Data), all patient Protected Health Information (PHI) is permanently detached before image processing.
2. **Standardization**: Training datasets adhere to international ESHRE (European Society of Human Reproduction and Embryology) consensus guidelines.

---

## 3. Article 14: Human-in-the-Loop Clinical Oversight
1. **Embryologist Final Authority (Art. 14(4)(d))**: The AI system only produces recommendations. Final grading and transfer decisions require attending embryologist electronic signature.
2. **Explainability**: Outputs include segmentation overlays and developmental timing curves allowing clinical experts to verify the underlying rationale.

---

## 4. Article 15: Accuracy, Robustness & Cybersecurity
1. **Model Architecture**: Deep convolutional neural networks (Attention U-Net) validated for robustness against optical illumination variation and focal plane shifts.
2. **Cybersecurity**: Deployment within private sovereign VPCs with encrypted at-rest storage and zero telemetry leakage to third-party endpoints.
