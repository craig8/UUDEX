from typing import Dict, Any, List, Union
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
from pathlib import Path
from datetime import datetime, timezone


class MockConfigRequest(BaseModel):
    path: str
    response: Union[
        Dict[str, Any], List[Dict[str, Any]]
    ]  # Allow both dict and list of dicts
    status_code: int = 200


class UUDEXMockServer:
    def __init__(self):
        self.app = FastAPI()
        self.responses = {}
        self.requests_history = []
        self.server_id = "mock-server-" + datetime.now(timezone.utc).strftime(
            "%Y%m%d-%H%M%S"
        )
        self.start_time = datetime.now(timezone.utc)

        @self.app.middleware("http")
        async def capture_request(request: Request, call_next):
            # Capture request before processing
            if not request.url.path.startswith("/mock/"):
                body = None
                if request.method in ["POST", "PUT", "PATCH"]:
                    body_bytes = await request.body()
                    try:
                        body = json.loads(body_bytes)
                    except:
                        pass
                    # Reset body for other handlers
                    request._body = body_bytes

                self.requests_history.append(
                    {"path": request.url.path, "method": request.method, "body": body}
                )

            response = await call_next(request)
            return response

        # Load mock data
        fixtures_path = (
            Path(__file__).parent.parent / "tests" / "fixtures" / "mock_data.json"
        )
        if fixtures_path.exists():
            with open(fixtures_path) as f:
                mock_data = json.load(f)
                # Pre-configure responses for standard endpoints
                self.responses = {
                    "api/v1/participants": {
                        "response": mock_data["participants"],
                        "status_code": 200,
                    },
                    "api/v1/subjects": {
                        "response": mock_data["subjects"],
                        "status_code": 200,
                    },
                    "api/v1/subscriptions": {
                        "response": mock_data["subscriptions"],
                        "status_code": 200,
                    },
                }
                # Store messages for lookup
                self.messages = mock_data.get("messages", [])

        # Try to load OpenAPI spec if available
        openapi_path = Path(__file__).parent.parent / "openapi.json"
        self.openapi_spec = None
        if openapi_path.exists():
            with open(openapi_path) as f:
                self.openapi_spec = json.load(f)

            # Override the OpenAPI schema if spec exists
            def custom_openapi():
                if self.app.openapi_schema:
                    return self.app.openapi_schema
                openapi_schema = self.openapi_spec
                self.app.openapi_schema = openapi_schema
                return self.app.openapi_schema

            self.app.openapi = custom_openapi

        self._setup_routes()

    def _setup_routes(self):
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "server": {
                    "id": self.server_id,
                    "uptime": str(datetime.now(timezone.utc) - self.start_time),
                    "fixtures_loaded": bool(self.responses),
                    "endpoints": {
                        "participants": len(
                            self.responses.get("api/v1/participants", {}).get(
                                "response", []
                            )
                        ),
                        "subjects": len(
                            self.responses.get("api/v1/subjects", {}).get(
                                "response", []
                            )
                        ),
                        "subscriptions": len(
                            self.responses.get("api/v1/subscriptions", {}).get(
                                "response", []
                            )
                        ),
                        "messages": len(self.messages),
                    },
                },
            }

        @self.app.post("/mock/reset")
        async def reset():
            """Reset the mock server state"""
            self.reset()
            return {"status": "reset"}

        @self.app.post("/mock/configure")
        async def configure_mock(config: MockConfigRequest):
            """Configure mock response for a specific path"""
            path = config.path.lstrip("/")
            self.responses[path] = {
                "response": config.response,
                "status_code": config.status_code,
            }
            return {"status": "configured"}

        @self.app.get("/mock/history")
        async def get_history():
            """Get request history"""
            return self.requests_history

        @self.app.post("/api/v1/subscriptions")
        async def create_subscription(request: Request):
            """Create a new subscription"""
            data = await request.json()
            # Add an ID if not provided
            if "id" not in data:
                data[
                    "id"
                ] = f"sub_{len(self.responses.get('api/v1/subscriptions', {}).get('response', []))}"
            # Add to existing subscriptions
            subs = self.responses.get("api/v1/subscriptions", {}).get("response", [])
            subs.append(data)
            self.responses["api/v1/subscriptions"] = {
                "response": subs,
                "status_code": 200,
            }
            return data

        @self.app.delete("/api/v1/subscriptions/{subscription_id}")
        async def delete_subscription(subscription_id: str):
            """Delete a subscription"""
            subs = self.responses.get("api/v1/subscriptions", {}).get("response", [])
            subs = [s for s in subs if s["id"] != subscription_id]
            self.responses["api/v1/subscriptions"] = {
                "response": subs,
                "status_code": 200,
            }
            return {"status": "deleted"}

        @self.app.post("/api/v1/subjects/{subject_id}/messages")
        async def publish_message(subject_id: str, request: Request):
            """Publish a message"""
            data = await request.json()
            message = {
                "message_id": f"msg_{len(self.messages)}",
                "subject_id": subject_id,
                "content": (
                    {"message": data["message"]}
                    if "message" in data  # Integration test format
                    else data["content"]  # Mock server test format
                ),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            if "metadata" in data:
                message["metadata"] = data["metadata"]
            self.messages.append(message)
            return message

        @self.app.get("/api/v1/subjects/{subject_id}/messages")
        async def get_messages(subject_id: str):
            """Get messages for a subject"""
            # Ensure path matches with or without api/v1 prefix
            parts = subject_id.split("/")
            clean_subject = parts[-1] if len(parts) > 1 else subject_id
            return [msg for msg in self.messages if msg["subject_id"] == clean_subject]

        @self.app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
        async def handle_request(path: str, request: Request):
            """Handle all API requests"""
            path = path.lstrip("/")
            # Try both with and without api/v1 prefix
            paths_to_try = [path]
            if path.startswith("api/v1/"):
                paths_to_try.append(path[7:])  # Remove api/v1/
            else:
                paths_to_try.append(f"api/v1/{path}")

            # Special handling for subscriptions and messages
            if request.method == "POST":
                if path.endswith("subscriptions"):
                    return await create_subscription(request)
                elif "messages" in path:
                    parts = path.split("/")
                    if len(parts) >= 4 and parts[-1] == "messages":
                        return await publish_message(parts[-2], request)

            # Handle GET messages
            if request.method == "GET" and "messages" in path:
                parts = path.split("/")
                if len(parts) >= 4 and parts[-1] == "messages":
                    return await get_messages(parts[-2])

            for try_path in paths_to_try:
                mock_response = self.responses.get(try_path)
                if mock_response:
                    return JSONResponse(
                        content=mock_response["response"],
                        status_code=mock_response["status_code"],
                    )

            # Try OpenAPI spec next
            spec_response = await self._generate_response_from_spec(path, request)
            if spec_response:
                return spec_response

            raise HTTPException(status_code=404, detail="Path not found")

    async def _generate_response_from_spec(self, path: str, request: Request):
        """Generate a response based on the OpenAPI specification if available"""
        if not self.openapi_spec:
            return None

        # Find matching path in OpenAPI spec
        for spec_path, path_item in self.openapi_spec["paths"].items():
            if self._paths_match(path, spec_path):
                method = request.method.lower()
                if method in path_item:
                    operation = path_item[method]
                    if "responses" in operation:
                        success_response = operation["responses"].get("200", {})
                        if "content" in success_response:
                            content = success_response["content"]
                            if "application/json" in content:
                                schema = content["application/json"]
                                if "example" in schema:
                                    return schema["example"]
        return None

    def _paths_match(self, request_path: str, spec_path: str):
        """Check if request path matches OpenAPI spec path pattern"""
        request_parts = request_path.strip("/").split("/")
        spec_parts = spec_path.strip("/").split("/")

        if len(request_parts) != len(spec_parts):
            return False

        for req_part, spec_part in zip(request_parts, spec_parts):
            if spec_part.startswith("{") and spec_part.endswith("}"):
                continue
            if req_part != spec_part:
                return False
        return True

    def reset(self):
        """Reset mock state"""
        # Clear all state
        self.responses = {}
        self.messages = []
        self.requests_history = []


app = UUDEXMockServer().app
