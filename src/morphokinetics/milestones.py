"""Embryo Morphokinetics Milestone & Timing Kinetics Calculator
Calculates time-lapse kinetic parameters (t2, t3, t4, t8, tSB, tB, cc2, s2)
conforming to international ESHRE & Vienna Consensus reproductive biology standards.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field

class MorphokineticTimings(BaseModel):
    t_pb: float = Field(..., description="Hours to polar body extrusion")
    t_2: float = Field(..., description="Hours to 2-cell cleavage")
    t_3: float = Field(..., description="Hours to 3-cell stage")
    t_4: float = Field(..., description="Hours to 4-cell stage")
    t_8: float = Field(..., description="Hours to 8-cell stage")
    t_sb: float = Field(..., description="Hours to start of blastulation")
    t_b: float = Field(..., description="Hours to full blastocyst")

class MorphokineticKineticsEvaluator:
    """Evaluates developmental cell division intervals based on standard time-lapse microscopy.
    Primary prognostic indicators:
    - cc2 = t3 - t2 (duration of second cell cycle, optimal: 5 - 12 hours)
    - s2  = t4 - t3 (synchrony of division from 2 to 4 cells, optimal: 0 - 0.75 hours)
    - t5 - t2 (cleavage to 5 cells)
    """
    
    @staticmethod
    def evaluate(timings: MorphokineticTimings) -> Dict[str, Any]:
        cc2 = timings.t_3 - timings.t_2
        s2 = timings.t_4 - timings.t_3
        blastulation_duration = timings.t_b - timings.t_sb
        
        # Clinical Prognostic Scoring (Meseguer / ESHRE Category)
        is_optimal_cc2 = 5.0 <= cc2 <= 12.0
        is_optimal_s2 = 0.0 <= s2 <= 1.0
        is_timely_blast = timings.t_b <= 116.0  # Full blastocyst before 116h post-ICSI
        
        score = 0
        if is_optimal_cc2: score += 35
        if is_optimal_s2: score += 35
        if is_timely_blast: score += 30
        
        if score >= 85:
            tier = "Tier A (High Implantation Potential)"
        elif score >= 65:
            tier = "Tier B (Moderate Implantation Potential)"
        else:
            tier = "Tier C (Suboptimal Morphokinetics - Secondary Priority)"
            
        return {
            "cell_cycle_2_duration_hours": round(cc2, 2),
            "synchrony_s2_hours": round(s2, 2),
            "blastulation_duration_hours": round(blastulation_duration, 2),
            "prognostic_score": score,
            "morphokinetic_tier": tier,
            "optimal_division_kinetics": is_optimal_cc2 and is_optimal_s2
        }
