"""Output Validation and Guardrails"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class OutputValidator:
    """Validate and filter LLM outputs"""

    def __init__(self):
        """Initialize output validator"""
        self.blocked_keywords = [
            "illegal", "hack", "crack", "malware"
        ]
        self.min_confidence = 0.5

    def validate(self, output: str, confidence: Optional[float] = None) -> str:
        """Validate output"""
        # Check confidence
        if confidence and confidence < self.min_confidence:
            return "Unable to provide confident answer."
        
        # Check for blocked content
        if self._contains_blocked_content(output):
            return "I cannot provide that information."
        
        return output

    def _contains_blocked_content(self, text: str) -> bool:
        """Check if text contains blocked content"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.blocked_keywords)

    def sanitize_output(self, output: str) -> str:
        """Sanitize output"""
        # Remove potentially harmful content
        output = output.replace("<script>", "")
        output = output.replace("</script>", "")
        return output
