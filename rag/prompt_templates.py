"""Prompt Templates for LLM"""

from typing import Optional


class PromptTemplates:
    """Collection of prompt templates"""

    @staticmethod
    def get_rag_prompt(context: str, query: str) -> str:
        """Get RAG prompt template"""
        return f"""You are a helpful assistant. Use the provided context to answer the question.

Context:
{context}

Question: {query}

Answer:"""

    @staticmethod
    def get_summarization_prompt(text: str) -> str:
        """Get summarization prompt"""
        return f"""Summarize the following text concisely:

{text}

Summary:"""

    @staticmethod
    def get_extraction_prompt(text: str, entities: str) -> str:
        """Get entity extraction prompt"""
        return f"""Extract the following entities from the text: {entities}

Text:
{text}

Extracted entities:"""
