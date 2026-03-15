"""MiroFish report parser"""
import re
from typing import Dict, List, Optional


def parse_report(report_data: Dict) -> Dict:
    """
    Parse MiroFish report and extract success prediction
    
    Args:
        report_data: Raw report from MiroFish API
    
    Returns:
        Parsed prediction data with:
        - success_score: 0-100
        - risk_factors: list of risks
        - improvements: list of suggestions
        - market_reaction: summary
    """
    data = report_data.get("data", report_data)
    content = data.get("markdown_content", data.get("content", ""))
    
    # Extract success probability (0-100)
    success_score = extract_success_score(content)
    
    # Extract risk factors
    risk_factors = extract_list_section(content, "리스크 요인", "개선 제안")
    
    # Extract improvement suggestions
    improvements = extract_list_section(content, "개선 제안", "시장 반응")
    
    # Extract market reaction summary
    market_reaction = extract_section(content, "잠재 고객 반응")
    
    return {
        "success_score": success_score,
        "risk_factors": risk_factors,
        "improvements": improvements,
        "market_reaction": market_reaction,
        "raw_content": content
    }


def extract_success_score(text: str) -> Optional[int]:
    """Extract success probability score from text"""
    # Look for patterns like "성공 확률: 75%" or "75%의 성공 가능성"
    patterns = [
        r"성공\s*확률[:\s]*(\d+)%",
        r"(\d+)%의?\s*성공",
        r"시장\s*진입\s*성공\s*확률[:\s]*(\d+)%"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            score = int(match.group(1))
            return min(max(score, 0), 100)  # Clamp to 0-100
    
    return None


def extract_list_section(text: str, start_marker: str, end_marker: Optional[str] = None) -> List[str]:
    """Extract bulleted/numbered list from a section"""
    # Find section
    start_idx = text.find(start_marker)
    if start_idx == -1:
        return []
    
    # Find end of section
    if end_marker:
        end_idx = text.find(end_marker, start_idx)
        section = text[start_idx:end_idx] if end_idx != -1 else text[start_idx:]
    else:
        section = text[start_idx:]
    
    # Extract list items (numbered or bulleted)
    items = []
    for line in section.split("\n"):
        line = line.strip()
        # Match "1. item" or "- item" or "* item"
        match = re.match(r"^(?:\d+\.|[-*])\s*(.+)$", line)
        if match:
            items.append(match.group(1).strip())
    
    return items


def extract_section(text: str, section_name: str) -> str:
    """Extract text content from a named section"""
    # Find section header
    pattern = rf"##?\s*{re.escape(section_name)}.*?\n(.+?)(?=\n##|\Z)"
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        content = match.group(1).strip()
        # Remove list markers for summary
        content = re.sub(r"^\s*(?:\d+\.|[-*])\s*", "", content, flags=re.MULTILINE)
        return content
    
    return ""


def format_prediction_result(parsed: Dict) -> str:
    """Format parsed prediction into readable text"""
    lines = []
    
    if parsed["success_score"] is not None:
        lines.append(f"🎯 **성공 예측 점수**: {parsed['success_score']}/100")
    
    if parsed["market_reaction"]:
        lines.append(f"\n📊 **시장 반응**")
        lines.append(parsed["market_reaction"])
    
    if parsed["risk_factors"]:
        lines.append(f"\n⚠️ **주요 리스크** ({len(parsed['risk_factors'])}개)")
        for i, risk in enumerate(parsed["risk_factors"], 1):
            lines.append(f"{i}. {risk}")
    
    if parsed["improvements"]:
        lines.append(f"\n💡 **개선 제안** ({len(parsed['improvements'])}개)")
        for i, improvement in enumerate(parsed["improvements"], 1):
            lines.append(f"{i}. {improvement}")
    
    return "\n".join(lines)
