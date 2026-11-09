from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def generate_response(self, prompt: str) -> dict:
        """
        Generate a response from an LLM.

        Expected output:
        {
            "response": str,
            "input_tokens": int,
            "output_tokens": int,
            "total_tokens": int,
            "latency": float,
            "model": str
        }
        """
        pass