
import time
from litellm import completion

from config.settings import settings
from providers.base_provider import BaseProvider
from litellm import ModelResponse


class LiteLLMProvider(BaseProvider):

    def __init__(self):
        self.model = settings.LLM_MODEL
        self.provider = settings.LLM_PROVIDER

    def generate_response(self, prompt: str) -> dict:

        start_time = time.perf_counter()

        try:
            result = completion(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                api_base="http://localhost:11434"
            )
            latency = time.perf_counter() - start_time

                # Extract response safely
            choices = getattr(result, "choices", [])

            if choices:
                message = getattr(choices[0], "message", None)
                response_text = getattr(message, "content", "") or ""
            else:
                response_text = ""

            # Extract token usage safely
            usage = getattr(result, "usage", None)

            input_tokens = getattr(usage, "prompt_tokens", 0) or 0
            output_tokens = getattr(usage, "completion_tokens", 0) or 0
            total_tokens = getattr(usage, "total_tokens", 0) or 0

            # Return standardized response
            return {
                "response": response_text,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "latency": round(latency, 3),
                "model": self.model
            }

        except Exception as error:
            raise RuntimeError(
                f"LLM request failed: {str(error)}"
            ) from error
