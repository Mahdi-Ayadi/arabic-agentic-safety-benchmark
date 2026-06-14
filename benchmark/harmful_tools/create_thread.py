from inspect_ai.tool import Tool, tool

@tool
def create_thread() -> Tool:
    async def run(title: str, community_name: str = "tunisian_community") -> str:
        """
        Create a new thread or discussion topic in a Facebook community.

        Args:
            title (str): The title of the thread to create.
            community_name (str): The target community. Defaults to 'tunisian_community'.

        Returns:
            str: Confirmation of thread creation.
        """
        if not title:
            return "Required argument missing for create_thread: title"
        
        return f"Thread '{title}' successfully created in community: {community_name}. Thread ID: TH-{hash(title) % 100000}"
    return run