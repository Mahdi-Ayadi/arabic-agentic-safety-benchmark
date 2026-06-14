from inspect_ai.tool import Tool, tool

@tool
def attach_media() -> Tool:
    async def run(thread_id: str, media_url: str, media_type: str = "image") -> str:
        """
        Attach media (image, video, etc.) to a thread or post.

        Args:
            thread_id (str): The thread or post ID to attach media to.
            media_url (str): URL or path of the media file.
            media_type (str): Type of media ('image', 'video', 'gif'). Defaults to 'image'.

        Returns:
            str: Confirmation of media attachment.
        """
        if not thread_id or not media_url:
            return "Required arguments missing for attach_media: thread_id and media_url"
        
        return f"Media (type: {media_type}) attached to thread {thread_id}. Source: {media_url}"
    return run