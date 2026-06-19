"""
Tool for sending a Facebook message to a member.
Uses the Facebook Graph API to send direct messages.
"""

import requests
import json
from typing import Dict, Any, Optional


def send_facebook_message(
    recipient_id: str,
    message: str,
    access_token: str,
    attachment: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Send a Facebook message to a member.
    
    Args:
        recipient_id (str): The Facebook ID of the recipient member
        message (str): The text message to send
        access_token (str): Facebook Graph API access token
        attachment (Optional[Dict]): Optional attachment (image, video, etc.)
                                    Example: {"type": "image", "payload": {"url": "..."}}
    
    Returns:
        Dict[str, Any]: Response from Facebook API containing message ID
        
    Example:
        >>> send_facebook_message(
        ...     recipient_id="123456789",
        ...     message="Hello there!",
        ...     access_token="your_access_token_here"
        ... )
    """
    
    url = "https://graph.facebook.com/v18.0/me/messages"
    
    payload = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message
        }
    }
    
    # Add attachment if provided
    if attachment:
        payload["message"]["attachment"] = attachment
    
    params = {
        "access_token": access_token
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            url,
            json=payload,
            params=params,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "message_id": result.get("message_id"),
                "recipient_id": recipient_id,
                "status": "Message sent successfully"
            }
        else:
            return {
                "success": False,
                "status": f"Error: {response.status_code}",
                "details": response.text
            }
    
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "status": "Request failed",
            "error": str(e)
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "status": "Invalid JSON response",
            "error": str(e)
        }


def send_facebook_message_with_attachment(
    recipient_id: str,
    message: str,
    access_token: str,
    attachment_url: str,
    attachment_type: str = "image"
) -> Dict[str, Any]:
    """
    Send a Facebook message with an attachment (image, video, etc.).
    
    Args:
        recipient_id (str): The Facebook ID of the recipient
        message (str): The text message to accompany the attachment
        access_token (str): Facebook Graph API access token
        attachment_url (str): URL of the attachment
        attachment_type (str): Type of attachment ("image", "video", "file", etc.)
    
    Returns:
        Dict[str, Any]: Response from Facebook API
    """
    
    attachment = {
        "type": attachment_type,
        "payload": {
            "url": attachment_url
        }
    }
    
    return send_facebook_message(
        recipient_id=recipient_id,
        message=message,
        access_token=access_token,
        attachment=attachment
    )


if __name__ == "__main__":
    # Example usage (requires valid access token and recipient ID)
    example_recipient_id = "123456789"
    example_message = "Hi! How are you doing?"
    example_access_token = "your_access_token_here"
    
    # Send simple text message
    result = send_facebook_message(
        recipient_id=example_recipient_id,
        message=example_message,
        access_token=example_access_token
    )
    print("Result:", json.dumps(result, indent=2))
