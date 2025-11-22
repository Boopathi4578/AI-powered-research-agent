"""
LLM Model configuration for the research agent.
Supports OpenAI and Anthropic models via Agno framework.
"""

import os
from typing import Optional
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMConfig:
    """Configuration for LLM models used in the research agent."""
    
    @staticmethod
    def get_openai_model(
        model_name: str = "gpt-4o-mini",
        temperature: float = 0.3,
        max_tokens: int = 4000
    ):
        """
        Get an OpenAI model instance.
        
        Args:
            model_name: Name of the OpenAI model
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            
        Returns:
            Configured OpenAI model instance
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        return OpenAIChat(
            id=model_name,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    @staticmethod
    def get_anthropic_model(
        model_name: str = "claude-3-5-sonnet-20241022",
        temperature: float = 0.3,
        max_tokens: int = 4000
    ):
        """
        Get an Anthropic Claude model instance.
        
        Args:
            model_name: Name of the Claude model
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
            
        Returns:
            Configured Claude model instance
        """
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        return Claude(
            id=model_name,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    @staticmethod
    def get_default_model(provider: str = "openai"):
        """
        Get the default model based on provider.
        
        Args:
            provider: Either 'openai' or 'anthropic'
            
        Returns:
            Configured model instance
        """
        if provider.lower() == "openai":
            return LLMConfig.get_openai_model()
        elif provider.lower() == "anthropic":
            return LLMConfig.get_anthropic_model()
        else:
            raise ValueError(f"Unsupported provider: {provider}")

