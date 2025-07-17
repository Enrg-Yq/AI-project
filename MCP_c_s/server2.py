import mcp.types as types
from mcp.server.fastmcp import FastMCP
from mcp.shared._httpx_utils import create_mcp_http_client

async def fetch_website(url: str) -> list[types.ContentBlock]:
    headers = {
        "User-Agent": "MCP Simple Server"
    }
    async with create_mcp_http_client(headers=headers) as client:
        response = await client.get(url)
        response.raise_for_status()
        return [types.TextContent(type="text", text=response.text)]

def main(
    port: int = 8000,
    log_level: str = "INFO",
    json_response: bool = False,
) -> int:
    app = FastMCP(
        "mcp-website-fetcher",
        stateless_http=False,  # 状态http连接 （服务器记住客户端）
        json_response=json_response,
    )
    app.settings.port = port
    app.settings.log_level = log_level

    @app.tool()
    async def fetch(url: str) -> list[types.ContentBlock]:
        return await fetch_website(url)

    print(f"Starting MCP StreamableHttp server on port {port} ...")
    app.run(transport="streamable-http")
    return 0

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--log-level", type=str, default="INFO")
    parser.add_argument("--json-response", action="store_true")
    args = parser.parse_args()

    main(port=args.port, log_level=args.log_level, json_response=args.json_response)