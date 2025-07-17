import asyncio
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def main():
    # 替换为你的 MCP 服务器地址
    server_url = "http://localhost:8000/mcp"
    async with streamablehttp_client(server_url) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 列出可用工具
            tools = await session.list_tools()
            print("Tools:", tools)

            # 调用 fetch 工具
            result = await session.call_tool("fetch", {"url": "https://feeds.feedburner.com/ruanyifeng"})
            print("Fetch result:", result)

if __name__ =="__main__":
    asyncio.run(main())