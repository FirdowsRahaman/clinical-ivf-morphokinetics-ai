"""
Gardner Blastocyst Grading & Viability Assessment System
Implements the standard Gardner & Schoolcraft clinical staging criteria:
- Expansion Grade (1 to 6)
- Inner Cell Mass (ICM) Quality (A, B, C)
- Trophectoderm (TE) Quality (A, B, C)
"""

from typing import Dict, Any, Tuple
from pydantic import BaseModel, Field

class BlastocystMorphology(BaseModel):
    expansion_grade: int = Field(..., ge=1, le=6, description="1: Early, 2: Blastocyst, 3: Full, 4: Expanded, 5: Hatching, 6: Hatched")
    icm_cell_count: int = Field(..., description="Estimated segmented cells in Inner Cell Mass")
    icm_compaction_ratio: float = Field(..., ge=0.0, le=1.0, description="Cohesiveness of ICM cells")
    te_cell_count: int = Field(..., description="Estimated segmented cells in Trophectoderm epithelium")
    te_continuity_ratio: float = Field(..., ge=0.0, le=1.0, description="Epithelial continuity around cavity")

class GardnerClassifier:
    """
    Evaluates blastocyst morphological features and outputs standard clinical Gardner grade.
    """
    @staticmethod
    def classify_icm(cell_count: int, compaction: float) -> str:
        if cell_count >= 25 and compaction >= 0.75:
            return "A"  # Many cells, tightly packed
        elif cell_count >= 12 and compaction >= 0.50:
            return "B"  # Several cells, loosely grouped
        else:
            return "C"  # Very few cells

    @staticmethod
    def classify_te(cell_count: int, continuity: float) -> str:
        if cell_count >= 30 and continuity >= 0.80:
            return "A"  # Many cells forming a cohesive epithelium
        elif cell_count >= 15 and continuity >= 0.60:
            return "B"  # Fewer cells forming a loose epithelium
        else:
            return "C"  # Very few large cells

    @classmethod
    def evaluate(cls, morphology: BlastocystMorphology) -> Dict[str, Any]:
        exp = morphology.expansion_grade
        icm = cls.classify_icm(morphology.icm_cell_count, morphology.icm_compaction_ratio)
        te = cls.classify_te(morphology.te_cell_count, morphology.te_continuity_ratio)
        gardner_grade = f"{exp}{icm}{te}"

        # Clinical Viability & Implantation Probability Estimation
        # Reference: ESHRE Vienna Consensus on embryo transfer prioritization
        base_prob = {
            "AA": 0.65, "AB": 0.55, "BA": 0.52, "BB": 0.42, 
            "AC": 0.32, "CA": 0.30, "BC": 0.25, "CB": 0.22, "CC": 0.12
        }.get(f"{icm}{te}", 0.20)

        # Expansion modifier (4, 5 typically best transfers)
        exp_mod = {1: -0.20, 2: -0.10, 3: 0.0, 4: 0.05, 5: 0.05, 6: 0.02}.get(exp, 0.0)
        viability_probability = max(0.05, min(0.80, base_prob + exp_mod))

        return {
            "gardner_grade": gardner_grade,
            "expansion_stage": exp,
            "icm_grade": icm,
            "trophectoderm_grade": te,
            "estimated_implantation_potential": round(viability_probability, 3),
            "transfer_priority": "High" if viability_probability >= 0.50 else ("Moderate" if viability_probability >= 0.30 else "Low")
        }
