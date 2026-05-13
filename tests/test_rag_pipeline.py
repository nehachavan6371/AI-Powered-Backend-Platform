"""RAG Pipeline Tests"""

import pytest
from rag.pipeline import RAGPipeline
from rag.output_validators import OutputValidator


def test_chunk_document():
    """Test document chunking"""
    pipeline = RAGPipeline()
    content = "This is a test document. " * 100
    chunks = pipeline.chunk_document(content)
    assert len(chunks) > 0


def test_preprocess_document():
    """Test document preprocessing"""
    pipeline = RAGPipeline()
    content = "  This  is   a   test  document.  "
    processed = pipeline.preprocess_document(content)
    assert "  " not in processed


def test_output_validation():
    """Test output validation"""
    validator = OutputValidator()
    output = "Valid response"
    validated = validator.validate(output)
    assert validated == output


def test_blocked_content_detection():
    """Test blocked content detection"""
    validator = OutputValidator()
    output = "This contains illegal content."
    validated = validator.validate(output)
    assert "cannot provide" in validated.lower()
