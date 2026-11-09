class RequestManager:

    @staticmethod
    def validate_prompt(prompt: str) -> str:
        """
        Clean and validate the user's prompt.
        """

        if not isinstance(prompt, str):
            raise TypeError("Prompt must be a string.")

        prompt = prompt.strip()

        if not prompt:
            raise ValueError("Prompt cannot be empty.")

        if len(prompt) > 20000:
            raise ValueError("Prompt is too long. Maximum is 20,000 characters.")

        return prompt