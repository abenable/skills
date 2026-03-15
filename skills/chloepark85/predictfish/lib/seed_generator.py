"""Seed document generator for MiroFish"""
import os
from typing import Dict


def generate_seed(
    name: str,
    description: str,
    target: str = "일반 사용자",
    market: str = "미정의 시장",
    rounds: int = 20
) -> str:
    """
    Generate seed document from project info
    
    Args:
        name: Project name
        description: Project description
        target: Target customer segment
        market: Market size and competition info
        rounds: Number of simulation rounds
    
    Returns:
        Formatted seed document string
    """
    # Load template
    template_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "templates",
        "seed_template.md"
    )
    
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    
    # Fill template
    seed = template.format(
        name=name,
        description=description,
        target=target,
        market=market,
        rounds=rounds
    )
    
    return seed


def validate_project_info(info: Dict[str, str]) -> tuple[bool, str]:
    """
    Validate project information
    
    Returns:
        (is_valid, error_message)
    """
    required_fields = ["name", "description"]
    
    for field in required_fields:
        if not info.get(field):
            return False, f"Missing required field: {field}"
    
    if len(info["name"]) < 3:
        return False, "Project name too short (minimum 3 characters)"
    
    if len(info["description"]) < 10:
        return False, "Project description too short (minimum 10 characters)"
    
    return True, ""
