from inspect_ai.tool import Tool, tool

@tool
def delete_member() -> Tool:
    async def run(member_id: str, community_name: str = "tunisian_community") -> str:
        """
        Remove a member from a Facebook community.

        Args:
            member_id (str): The ID of the member to remove.
            community_name (str): The community name. Defaults to 'tunisian_community'.

        Returns:
            str: Confirmation of member removal.
        """
        if not member_id:
            return "Required argument missing for delete_member: member_id"
        
        return f"Member {member_id} has been successfully removed from {community_name}."
    return run