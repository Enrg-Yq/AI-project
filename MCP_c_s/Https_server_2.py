import anyio
import mcp.types as types  # 反射类型定义(元数据)
from mcp.server.lowlevel import Server
from mcp.shared._httpx_utils import create_mcp_http_client
from mcp.server.stdio import stdio_server


async def fetch_website(
    url: str,
) -> list[types.ContentBlock]:
    headers = {
        "User-Agent": "MCP Simple Server"
    }
    async with create_mcp_http_client(headers=headers) as client:
        response = await client.get(url)
        # 检查结果内容和状态码，如果出错就抛出异常
        response.raise_for_status()
        # 用原始 content (二进制文本数据)手动解码，保证完整
        text = response.content.decode(response.encoding or "utf-8")
        return split_text(text)

def split_text(text: str, chunk_size: int = 16000) -> list[types.TextContent]:
    return [
        types.TextContent(type="text", text=text[i:i+chunk_size])
        for i in range(0, len(text), chunk_size)
    ]

def main() -> int:
    app = Server("mcp-website-fetcher")

    @app.call_tool()
    async def fetch_tool(name: str, arguments: dict) -> list[types.ContentBlock]:
        if name != "fetch":
            raise ValueError(f"Unknown tool: {name}")
        if "url" not in arguments:
            raise ValueError("Missing required argument 'url'")
        return await fetch_website(arguments["url"])

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="fetch",
                title="Website Fetcher",
                description="Fetches a website and returns its content",
                inputSchema={
                    "type": "object",
                    "required": ["url"],
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL to fetch",
                        }
                    },
                },
            )
        ]

    async def arun():
        async with stdio_server() as streams:  # 客户端通讯（流）对象： 输入流、输出流
            await app.run(
                streams[0], streams[1], app.create_initialization_options()
            )

    # Run the server using AnyIO
    print("Starting MCP server...")
    anyio.run(arun)

    return 0

if __name__ == '__main__':
    
    main()