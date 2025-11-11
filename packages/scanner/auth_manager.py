"""
Authentication Manager for Tavo Scanner

Handles API key and device token authentication for the scanner.
Supports device code flow for interactive authentication.
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
import asyncio
import webbrowser
import time
from dataclasses import dataclass

from ..python.src.tavo.device_auth import Device_AuthClient


@dataclass
class AuthCredentials:
    """Authentication credentials container."""
    api_key: Optional[str] = None
    device_token: Optional[str] = None
    user_info: Optional[Dict[str, Any]] = None


class AuthManager:
    """Manages authentication for Tavo Scanner."""

    def __init__(self, base_url: str = "https://api.tavo.ai", config_dir: Optional[Path] = None):
        """Initialize authentication manager.

        Args:
            base_url: Tavo API base URL
            config_dir: Directory to store credentials (default: ~/.tavoai)
        """
        self.base_url = base_url.rstrip('/')
        self.config_dir = config_dir or Path.home() / ".tavoai"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.credentials_file = self.config_dir / "credentials.json"
        self.device_auth = Device_AuthClient(base_url)

        # Load existing credentials
        self.credentials = self._load_credentials()

    def _load_credentials(self) -> AuthCredentials:
        """Load credentials from file."""
        if not self.credentials_file.exists():
            return AuthCredentials()

        try:
            with open(self.credentials_file, 'r') as f:
                data = json.load(f)
                return AuthCredentials(
                    api_key=data.get('api_key'),
                    device_token=data.get('device_token'),
                    user_info=data.get('user_info')
                )
        except (json.JSONDecodeError, IOError):
            return AuthCredentials()

    def _save_credentials(self) -> None:
        """Save credentials to file."""
        data = {
            'api_key': self.credentials.api_key,
            'device_token': self.credentials.device_token,
            'user_info': self.credentials.user_info
        }

        with open(self.credentials_file, 'w') as f:
            json.dump(data, f, indent=2)

    def get_credentials(self) -> AuthCredentials:
        """Get current authentication credentials."""
        return self.credentials

    def has_valid_credentials(self) -> bool:
        """Check if valid credentials are available."""
        return bool(self.credentials.api_key or self.credentials.device_token)

    def set_api_key(self, api_key: str) -> None:
        """Set API key for authentication.

        Args:
            api_key: The API key to use
        """
        self.credentials.api_key = api_key
        self.credentials.device_token = None  # Clear device token when setting API key
        self._save_credentials()

    def clear_credentials(self) -> None:
        """Clear all authentication credentials."""
        self.credentials = AuthCredentials()
        self._save_credentials()

    async def device_code_login(self, client_name: str = "Tavo Scanner") -> bool:
        """Perform device code authentication flow.

        Args:
            client_name: Name to display in the authorization prompt

        Returns:
            True if authentication successful, False otherwise
        """
        try:
            # Request device code
            response = await self.device_auth.post_code_cli(client_name)
            device_code = response.get('device_code')
            user_code = response.get('user_code')
            verification_url = response.get('verification_url')

            if not device_code or not user_code or not verification_url:
                print("Error: Invalid device code response")
                return False

            print("🔐 Authentication Required")
            print(f"Visit: {verification_url}")
            print(f"Enter code: {user_code}")
            print("\nOpening browser automatically...")

            # Open browser automatically
            try:
                webbrowser.open(verification_url)
            except Exception:
                print("Please open the URL manually in your browser.")

            print("\nWaiting for authorization...")

            # Poll for token
            max_attempts = 120  # 2 minutes with 1-second intervals
            for attempt in range(max_attempts):
                try:
                    # Check if code is approved
                    status_response = await self.device_auth.get_code_device_code_status(device_code)
                    if status_response.get('status') == 'approved':
                        # Get the token
                        token_response = await self.device_auth.post_token(device_code)
                        device_token = token_response.get('access_token')
                        user_info = token_response.get('user_info')

                        if device_token:
                            self.credentials.device_token = device_token
                            self.credentials.user_info = user_info
                            self.credentials.api_key = None  # Clear API key when using device token
                            self._save_credentials()

                            print("✅ Authentication successful!")
                            if user_info:
                                email = user_info.get('email', 'Unknown')
                                print(f"Logged in as: {email}")
                            return True

                except Exception:
                    # Token not ready yet, continue polling
                    pass

                # Wait before next poll
                await asyncio.sleep(1)

                # Show progress every 10 seconds
                if attempt % 10 == 0 and attempt > 0:
                    print(f"Still waiting... ({attempt}/{max_attempts})")

            print("❌ Authentication timed out. Please try again.")
            return False

        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False

    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests.

        Returns:
            Dictionary of headers to include in requests
        """
        headers = {}

        if self.credentials.api_key:
            headers['X-API-Key'] = self.credentials.api_key
        elif self.credentials.device_token:
            headers['Authorization'] = f'Bearer {self.credentials.device_token}'

        return headers

    def get_env_api_key(self) -> Optional[str]:
        """Get API key from environment variables."""
        return os.getenv('TAVO_API_KEY') or os.getenv('TAVOAI_API_KEY')

    def auto_authenticate(self) -> bool:
        """Automatically authenticate using available methods.

        Priority:
        1. Environment variable API key
        2. Stored API key
        3. Stored device token

        Returns:
            True if authentication credentials found, False otherwise
        """
        # Check environment variable first
        env_api_key = self.get_env_api_key()
        if env_api_key:
            self.set_api_key(env_api_key)
            return True

        # Check stored credentials
        if self.has_valid_credentials():
            return True

        return False

    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Get current user information."""
        return self.credentials.user_info

    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self.has_valid_credentials()


