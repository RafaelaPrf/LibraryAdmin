from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests
from utils.settings import get_api_base_url


@dataclass
class ApiResponse:
    success: bool
    message: str
    data: Optional[Any] = None


class APIClient:

    @staticmethod
    def _build_url(endpoint: str) -> str:
        base_url = get_api_base_url()
        return urljoin(base_url, endpoint.lstrip("/"))

    @staticmethod
    def test_connection(endpoint: str = "/genres") -> ApiResponse:
        try:
            url = APIClient._build_url(endpoint)
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return ApiResponse(success=True, message=f"✅ Connected successfully to {url}")
            else:
                return ApiResponse(success=False, message=f"❌ API responded with status {response.status_code}")
        except requests.exceptions.ConnectionError:
            return ApiResponse(success=False, message=f"❌ Could not connect to API at {APIClient._build_url(endpoint)}")
        except requests.exceptions.Timeout:
            return ApiResponse(success=False, message="❌ API request timed out")
        except Exception as e:
            return ApiResponse(success=False, message=f"❌ Error: {str(e)}")

    @staticmethod
    def put(endpoint: str, data: Dict[str, Any]) -> tuple[Optional[Any], Optional[str]]:
        try:
            url = APIClient._build_url(endpoint)
            response = requests.put(url, json=data, timeout=5)

            if response.status_code == 200:
                return response.json(), None

            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text

            return None, str(detail)

        except requests.exceptions.ConnectionError:
            return None, "Could not connect to the API."

        except requests.exceptions.Timeout:
            return None, "Request timed out."

        except Exception as e:
            return None, str(e)

    @staticmethod
    def delete(endpoint: str) -> tuple[bool, str]:
        try:
            url = APIClient._build_url(endpoint)
            response = requests.delete(url, timeout=5)

            if response.status_code == 204:
                return True, "Deleted successfully."

            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text

            return False, str(detail)

        except requests.exceptions.ConnectionError:
            return False, "Could not connect to the API."

        except requests.exceptions.Timeout:
            return False, "Request timed out."

        except Exception as e:
            return False, str(e)

    @staticmethod
    def get(endpoint: str) -> tuple[Optional[Any], Optional[str]]:
        try:
            url = APIClient._build_url(endpoint)
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                return response.json(), None
            else:
                return None, f"API returned {response.status_code}"

        except requests.exceptions.ConnectionError:
            return None, "Could not connect to the API."

        except requests.exceptions.Timeout:
            return None, "Request timed out."

        except Exception as e:
            return None, str(e)

    @staticmethod
    def post(endpoint: str, data: Dict[str, Any]) -> tuple[Optional[Any], Optional[str]]:
        try:
            url = APIClient._build_url(endpoint)
            response = requests.post(url, json=data, timeout=5)

            if response.status_code in (200, 201):
                return response.json(), None
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text

            return None, str(detail)

        except requests.exceptions.ConnectionError:
            return None, "Could not connect to the API."

        except requests.exceptions.Timeout:
            return None, "Request timed out."

        except Exception as e:
            return None, str(e)