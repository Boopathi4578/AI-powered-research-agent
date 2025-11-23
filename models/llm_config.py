"""LLM Model configuration for the research agent.

This module provides AWS Bedrock model configuration.
The Bedrock support uses `boto3` to call the Bedrock runtime API.
"""

import os
from typing import Optional
from dotenv import load_dotenv

try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
except Exception:
    boto3 = None

# Load environment variables
load_dotenv()


class BedrockModel:
    """Thin wrapper around AWS Bedrock runtime `invoke_model`.

    This wrapper provides a minimal `generate(prompt: str, **kwargs)`
    method that returns the raw text response. It uses the
    `bedrock-runtime` client when available (boto3 >=1.24+).
    """

    def __init__(self, model_id: str, region: Optional[str] = None, **client_kwargs):
        if boto3 is None:
            raise RuntimeError("boto3 is required for Bedrock support; install boto3")

        self.id = model_id
        # Create Bedrock runtime client
        self.region = region or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
        if self.region:
            client_kwargs.setdefault("region_name", self.region)

        # boto3 uses standard AWS auth chain (env, config file, role, etc.)
        try:
            self.client = boto3.client("bedrock-runtime", **client_kwargs)
        except Exception as e:
            raise RuntimeError(f"Failed to create Bedrock client: {e}")

    def generate(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.0, **kwargs) -> str:
        """Invoke the Bedrock model and return the text output.

        This implements a simple invoke using `input` -> text response
        flow. For more complex model types (structured inputs, multimodal)
        adapt this method.
        """
        # Construct payload for text input - many Bedrock models accept a simple 'input' key
        payload = {"input": prompt}

        try:
            response = self.client.invoke_model(modelId=self.id, contentType="application/json", body=bytes(str(payload), "utf-8"))
            # response may have a streaming/byte body depending on model/runtime
            body = response.get("body")
            if hasattr(body, "read"):
                raw = body.read()
            else:
                raw = body

            # Attempt to decode bytes
            if isinstance(raw, (bytes, bytearray)):
                try:
                    raw = raw.decode("utf-8")
                except Exception:
                    raw = str(raw)

            # Many runtimes return JSON or plain text; try to extract text
            text = str(raw)
            return text

        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f"Bedrock invocation error: {e}")


class LLMConfig:
    """Configuration for AWS Bedrock models used in the research agent."""

    @staticmethod
    def get_bedrock_model(
        model_id: str = None,
        region: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.0,
    ):
        """Create a BedrockModel wrapper.

        Args:
            model_id: Bedrock model identifier (reads from BEDROCK_MODEL_ID env var if not provided)
            region: AWS region to use (reads from AWS_REGION env var if not provided)
            max_tokens: Maximum tokens for generation
            temperature: Temperature for generation

        Returns:
            BedrockModel instance
        """
        model_id = model_id or os.getenv("BEDROCK_MODEL_ID")
        if not model_id:
            raise ValueError("BEDROCK_MODEL_ID not provided (env var or parameter)")
        return BedrockModel(model_id=model_id, region=region)

