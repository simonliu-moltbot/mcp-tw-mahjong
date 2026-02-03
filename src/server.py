
import asyncio
import sys
import os

# Add the current directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
import mcp.types as types

try:
    from logic import calculate_tai
except ImportError:
    print("Error importing logic.py", file=sys.stderr)
    def calculate_tai(*args, **kwargs):
        return {"error": "Internal logic import failed"}

server = Server("mcp-tw-mahjong")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available mahjong tools."""
    return [
        types.Tool(
            name="calculate_tai",
            description="依據中華麻將競技協會標準計算台灣 16 張麻將台數",
            inputSchema={
                "type": "object",
                "properties": {
                    "melds": {
                        "type": "array",
                        "items": {"type": "array", "items": {"type": "string"}},
                        "description": "5 組面子 (順子或刻子)，每組 3 張。例如 [['1m','2m','3m'], ['中','中','中']]"
                    },
                    "eye": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "1 組將 (對子)，共 2 張。例如 ['發', '發']"
                    },
                    "hu_tile": {
                        "type": "string",
                        "description": "胡的那張牌。例如 '1m'"
                    },
                    "is_self_drawn": {
                        "type": "boolean",
                        "description": "是否為自摸"
                    },
                    "is_concealed": {
                        "type": "boolean",
                        "description": "是否為門清",
                        "default": False
                    },
                    "wait_type": {
                        "type": "string",
                        "enum": ["normal", "edge"],
                        "description": "聽牌類型。normal: 一般, edge: 邊張/嵌張/單吊 (+1)",
                        "default": "normal"
                    },
                    "wind_round": {
                        "type": "string",
                        "enum": ["東", "南", "西", "北"],
                        "description": "目前圈風"
                    },
                    "wind_seat": {
                        "type": "string",
                        "enum": ["東", "南", "西", "北"],
                        "description": "胡家門風"
                    },
                    "is_dealer": {
                        "type": "boolean",
                        "description": "胡家是否為莊家"
                    },
                    "dealer_count": {
                        "type": "integer",
                        "description": "連莊次數 (0 為當莊第一次，1 為連一，以此類推)",
                        "default": 0
                    },
                    "flower_tiles": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "胡家擁有的花牌列表 (f1-f8)。"
                    },
                    "is_robbing_kong": {
                        "type": "boolean",
                        "description": "是否為搶槓 (+1)",
                        "default": False
                    },
                    "is_last_tile": {
                        "type": "boolean",
                        "description": "是否為海底撈月 (+1)",
                        "default": False
                    }
                },
                "required": ["melds", "eye", "hu_tile", "is_self_drawn", "wind_round", "wind_seat", "is_dealer"]
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""
    if name == "calculate_tai":
        if not arguments:
            return [types.TextContent(type="text", text="Missing arguments")]

        try:
            result = calculate_tai(
                melds=arguments.get("melds"),
                eye=arguments.get("eye"),
                hu_tile=arguments.get("hu_tile"),
                is_self_drawn=arguments.get("is_self_drawn"),
                is_concealed=arguments.get("is_concealed", False),
                wait_type=arguments.get("wait_type", "normal"),
                is_dealer=arguments.get("is_dealer"),
                dealer_count=arguments.get("dealer_count", 0),
                wind_round=arguments.get("wind_round"),
                wind_seat=arguments.get("wind_seat"),
                flower_tiles=arguments.get("flower_tiles", []),
                is_robbing_kong=arguments.get("is_robbing_kong", False),
                is_last_tile=arguments.get("is_last_tile", False)
            )
            
            summary = f"### 🀄️ 麻將台數計算結果 (標準規則)\n"
            summary += f"- **總台數**: {result['total_tai']} 台\n"
            summary += f"- **詳細台數內容**:\n"
            for reason in result['reasons']:
                summary += f"  - {reason}\n"
            
            return [types.TextContent(type="text", text=summary)]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error during calculation: {str(e)}")]
    
    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-tw-mahjong",
                server_version="0.2.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
