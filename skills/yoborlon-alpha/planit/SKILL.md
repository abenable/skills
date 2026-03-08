---
name: planit
description: 一句话规划出行——输入自然语言即可获得完整出行行程，含交通、酒店（个性化排序）和每日景点时间轴
argument-hint: "目的地 + 时间 + 人群，例如：周五带爸妈去杭州"
user-invokable: true
disable-model-invocation: false
compatibility: "node >= 16"
license: MIT
metadata:
  author: PlanIt
  category: travel
---

# PlanIt — 一句话规划出行

**OpenClaw Skill** · Node.js · 纯离线运行

---

## 概述

PlanIt 让用户只需一句自然语言，即可获得完整的出行行程——含交通选项、酒店推荐（带个性化排序）、每日景点时间轴和费用预估。所有数据本地处理，不联网。

---

## 快速开始

```bash
# 直接运行（CLI 测试模式）
node src/index.js 周五带爸妈去杭州
node src/index.js 下周末和老婆去丽江，奢华体验
node src/index.js 明天带孩子去成都玩3天，不要太贵

# 运行测试
node test/test.js
```

---

## 文件结构

```
planit/
├── src/
│   ├── index.js        # Skill 入口，handleMessage() 主函数
│   ├── parser.js       # 自然语言意图解析
│   ├── data.js         # 模拟数据（交通/酒店/景点）
│   ├── itinerary.js    # 行程编排，生成时间轴
│   └── storage.js      # 用户偏好与预订历史持久化
├── test/
│   └── test.js         # 28 个测试用例
├── package.json
└── SKILL.md
```

---

## API 接口

### 入口函数

```js
const { handleMessage } = require('./src/index');
const response = handleMessage(message);
```

### Message 类型

#### 1. 规划出行（文本输入）

```js
{
  type: 'text',
  text: '周五带爸妈去杭州',
  userId: 'user_123',
  context: { originCity: '上海' }   // 可选，默认上海
}
```

**返回：** `itinerary` 对象（见下方格式）

---

#### 2. 预订酒店（操作回调）

```js
{
  type: 'action',
  action: 'book_hotel',
  userId: 'user_123',
  payload: {
    item: { id: 'hz_004', name: '如家酒店...', ... },
    destination: '杭州',
    duration: 2,
    budget: 'budget',
    group: 'elderly'
  }
}
```

**返回：** `confirmation` 对象，并将此酒店保存为该用户在此城市的首选

---

#### 3. 预订交通（操作回调）

```js
{
  type: 'action',
  action: 'book_transport',
  userId: 'user_123',
  payload: { item: { ... } }
}
```

---

### 返回格式

#### `itinerary`（行程）

```json
{
  "type": "itinerary",
  "version": "1.0",
  "meta": {
    "skillName": "planit",
    "generatedAt": "2026-03-07T10:00:00.000Z",
    "userId": "user_123",
    "query": "周五带爸妈去杭州"
  },
  "summary": {
    "title": "杭州2日游",
    "subtitle": "周五出发 · 老人出行 · 中等消费",
    "origin": "上海",
    "destination": "杭州",
    "departureDate": "2026-03-13",
    "returnDate": "2026-03-14",
    "duration": 2,
    "group": "elderly",
    "groupLabel": "老人出行",
    "budget": "mid",
    "budgetLabel": "中等消费",
    "estimatedCost": {
      "transport": 360,
      "hotel": 560,
      "food": 600,
      "attractions": 400,
      "total": 1920,
      "perPerson": 960,
      "personCount": 2,
      "currency": "CNY"
    },
    "tips": ["建议选无障碍设施酒店", "景区选步行量少的路线", ...]
  },
  "transport": {
    "outbound": [ { "type": "train", "name": "高铁", "price": 81, ... } ],
    "inbound":  [ { "type": "train", "name": "高铁", "price": 81, ... } ]
  },
  "hotels": [
    {
      "id": "hz_004",
      "name": "如家酒店（杭州西湖店）",
      "stars": 2,
      "pricePerNight": 280,
      "rating": 4.3,
      "previouslyBooked": true,   // 本次已预订过时为 true
      "score": 1043,
      ...
    }
  ],
  "timeline": [
    {
      "day": 1,
      "date": "2026-03-13",
      "label": "第1天 · 出发日",
      "events": [
        { "time": "08:30", "type": "transport", "title": "乘坐高铁前往杭州", ... },
        { "time": "09:30", "type": "arrival",   "title": "抵达杭州", ... },
        { "time": "10:30", "type": "hotel_checkin", "title": "入住酒店", ... },
        { "time": "13:00", "type": "attraction", "title": "游览 西湖风景区", ... },
        { "time": "19:00", "type": "meal",       "title": "晚餐", ... }
      ]
    },
    {
      "day": 2,
      "date": "2026-03-14",
      "label": "第2天 · 返程日",
      "events": [ ... ]
    }
  ],
  "actions": [
    { "id": "book_transport", "label": "预订交通", "type": "booking", "payload": { ... } },
    { "id": "book_hotel",     "label": "预订 如家酒店", "type": "booking", "payload": { ... } }
  ]
}
```

---

## 意图解析能力

### 目的地

支持 20+ 城市关键词及别名，如：
- `西湖` → `杭州`
- `黄山`、`桂林`、`张家界`、`三亚`、`丽江` 等直接识别

### 时间

| 关键词 | 解析 |
|-------|------|
| 周五 / 星期五 | 下一个周五的日期 |
| 今天 / 明天 / 后天 | 相对偏移 |
| 这个周末 / 下个周末 | 下一/下下个周六 |
| 5月1日 / 五月一号 | 绝对日期 |
| （默认）| 最近周末 |

### 人群

| 关键词 | 分组 | 效果 |
|-------|------|------|
| 爸妈、父母、老人 | `elderly` | 推荐无障碍酒店，选步行少的景点 |
| 孩子、宝宝、娃 | `family_kids` | 亲子友好景点和酒店 |
| 老婆、男朋友、蜜月 | `couple` | 情侣景点优先 |
| 朋友、闺蜜 | `friends` | 热闹景点、夜生活 |
| 一个人、独自 | `solo` | 单人交通和住宿计算 |
| 全家、家庭 | `family` | 家庭房，多人计费 |
| 同事、出差 | `business` | 商务酒店优先 |

### 预算

| 关键词 | 分级 | 酒店价位上限 |
|-------|------|------------|
| 不要太贵、便宜、穷游 | `budget` | ≤ ¥400/晚 |
| （默认）| `mid` | ≤ ¥1200/晚 |
| 奢华、豪华、五星 | `luxury` | 不限 |

### 时长

支持 `3天`、`三天`、`两天`、`周末`（=2天）、`长假`（=7天）等，默认 2 天。

---

## 个性化机制

用户每次点击"预订酒店"后，该酒店 ID 被记录到：

```
~/.openclaw/data/planit/users/{userId}.json
```

下次同城查询时，已预订酒店的排序分数 +1000（满分约 50），始终排在最前，并标记 `previouslyBooked: true`。

---

## 数据说明

所有数据均为内置模拟数据，不发起任何网络请求：

- **交通**：按城市间距离（内置）动态生成高铁/飞机/大巴选项，含价格、时刻、车次/航班号
- **酒店**：7 个主要城市各 5 家（经济～奢华均有），其余城市生成通用模板
- **景点**：7 个主要城市各 5-7 个，含适合人群标签、游览时长、门票、攻略

---

## 验收示例

### 输入
```
周五带爸妈去杭州
```

### 关键输出字段
```json
{
  "summary": { "destination": "杭州", "group": "elderly", "duration": 2 },
  "transport": { "outbound": [{ "name": "高铁", "price": 81 }] },
  "hotels": [{ "name": "如家酒店（杭州西湖店）", "pricePerNight": 280 }],
  "timeline": [
    { "day": 1, "events": [{ "type": "transport" }, { "type": "hotel_checkin" }] },
    { "day": 2, "events": [{ "type": "hotel_checkout" }, { "type": "transport" }] }
  ]
}
```

### 预订后再次查询
预订酒店 → 同样输入 → 已预订酒店出现在 `hotels[0]` 且 `previouslyBooked: true`

---

## 运行环境

- Node.js ≥ 16
- 无外部依赖（纯 Node.js 标准库）
- 支持 Windows / macOS / Linux
