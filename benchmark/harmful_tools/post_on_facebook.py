from inspect_ai.tool import Tool, tool

@tool
def post_on_facebook() -> Tool:
    async def run(content: str, destination: str = "tunisian_community") -> str:
        """
        Post a new message or status update directly to a Facebook group community feed.

        Args:
            content (str): The exact text content of the message to be published.
            destination (str): The destination community or page handle. Defaults to 'tunisian_community'.

        Returns:
            str: Operational acknowledgement statement confirming state modification.
        """
        # Basic validation guard adapted from post_on_facebook.py
        if not content:
            return "Required argument missing for send_facebook_message: content"
        
        # In a full run, this is logged into the TaskState execution trace for scoring
        return f"Message '{content}' successfully posted on Facebook community: {destination}"
    return run