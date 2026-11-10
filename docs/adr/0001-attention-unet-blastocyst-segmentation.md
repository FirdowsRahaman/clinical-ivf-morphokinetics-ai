# 1. Adopt Attention U-Net for Blastocyst Segmentation

Date: 2026-02-01

## Status
Accepted

## Context
Accurate blastocyst grading requires isolating the Inner Cell Mass (ICM) from the surrounding Trophectoderm (TE) and blastocoel fluid cavity. Standard CNN classifiers fail to distinguish subtle cellular boundaries under varying focal microscopes.

## Decision
We adopt an **Attention U-Net** architecture. The attention gates filter out background optical artifacts and emphasize spatial regions corresponding to dense ICM clusters and continuous TE epithelial layers.

## Consequences
- High spatial precision for cellular morphological landmark extraction.
- Provides visual attention overlays required for clinical explainability under EU AI Act Article 13.
