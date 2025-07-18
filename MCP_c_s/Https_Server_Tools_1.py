import anyio
import mcp.types as types  # 反射类型定义(元数据)
from mcp.server.lowlevel import Server
from mcp.shared._httpx_utils import create_mcp_http_client
from mcp.server.stdio import stdio_server
import asyncio


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
if __name__ == "__main__":
    result = asyncio.run(fetch_website('http://finance.people.com.cn/n1/2025/0717/c1004-40524175.html'))
    full_text = ""
    for item in result:
        if  full_text == (item.text):
            full_text += item.text
    with open('result.html', 'w', encoding='utf-8') as file:
        file.write(full_text)
