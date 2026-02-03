# Taiwan 16-card Mahjong Tai Calculator MCP Server

此 MCP Server 提供台灣 16 張麻將的台數計算功能。

## 功能
- 計算基礎台數（莊家、連莊、自摸）
- 判定圈風與門風台數
- 判定花牌（正花、七搶一、八仙過海）
- 判定基本牌型（清一色、湊一色、字一色、碰碰胡、三元牌等）

## 安裝
1. 確保已安裝 Python 3.10+
2. 建立虛擬環境並安裝依賴：
   ```bash
   python -m venv .venv
   source .venv/bin/bin/activate  # macOS/Linux
   pip install -r requirements.txt
   ```

## 設定

### Dive 配置
- **Type**: `stdio`
- **Command**: `/Users/simonliuyuwei/clawd/projects/mcp-tw-mahjong/.venv/bin/python`
- **Args**: `/Users/simonliuyuwei/clawd/projects/mcp-tw-mahjong/src/server.py`

### Claude Desktop 配置
```json
{
  "mcpServers": {
    "tw-mahjong": {
      "command": "/Users/simonliuyuwei/clawd/projects/mcp-tw-mahjong/.venv/bin/python",
      "args": ["/Users/simonliuyuwei/clawd/projects/mcp-tw-mahjong/src/server.py"]
    }
  }
}
```
