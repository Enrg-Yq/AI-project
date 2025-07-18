import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main():
    async with stdio_client(
        StdioServerParameters(command="python", args=["Https_server_deftools_4.py"])  # 指令方式启动独立进程，"java" args"-jar"可用不同的语言
    ) as (read, write):
        # 创建会话
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            # print(tools)
            # print([tool.name for tool in tools.tools])

            # Call the fetch tool
            result = await session.call_tool("fetch", {"url": "https://feeds.feedburner.com/ruanyifeng"})
            full_text = ""
            for block in result.content:
                if block.type == "text":
                    full_text += block.text
            # print(full_text)
            with open("result.html", "w", encoding='utf-8') as f:
                f.write(full_text)

            result = await session.call_tool("echo",{"content":"你好！"})
            print("tool call result:",result.content[0].text)

asyncio.run(main())