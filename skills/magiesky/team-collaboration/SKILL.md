---
name: team-collaboration
description: 与团队协作系统交互的Skill，提供用户认证、项目管理、任务管理等功能
version: 1.0.0
---

# Team Collaboration Skill

用于与团队协作系统交互的Skill，提供项目管理、任务管理、用户认证等功能。

## API Base URL
- 后端: http://localhost:8080
- 前端: http://localhost:12345

## Tools

### auth_register
注册新用户账号

```typescript
type auth_register = (_: {
  // 用户名（必须唯一）
  username: string,
  // 密码
  password: string,
  // 昵称
  nickname: string,
  // 角色：PM、产品经理、研发、测试、小说家、小红书运营
  role: "PM" | "产品经理" | "研发" | "测试" | "小说家" | "小红书运营",
}) => any;
```

### auth_login
用户登录

```typescript
type auth_login = (_: {
  // 用户名
  username: string,
  // 密码
  password: string,
}) => any;
```

### create_project
创建新项目

```typescript
type create_project = (_: {
  // 项目名称
  name: string,
  // 项目描述
  description?: string,
  // 计划上线日期
  planDate?: string,
  // 产品经理ID（可选）
  ownerId?: number,
}) => any;
```

### get_projects
获取项目列表

```typescript
type get_projects = () => any;
```

### create_task
创建任务

```typescript
type create_task = (_: {
  // 需求ID
  requirementId: number,
  // 指派人ID
  assigneeId: number,
  // 任务标题
  title: string,
  // 任务描述
  description?: string,
  // 任务类型：开发、测试
  type: "开发" | "测试",
}) => any;
```

### get_my_tasks
获取当前用户的所有任务

```typescript
type get_my_tasks = () => any;
```

### get_pending_tasks
获取当前用户的待处理任务

```typescript
type get_pending_tasks = () => any;
```

### update_task_status
更新任务状态

```typescript
type update_task_status = (_: {
  // 任务ID
  taskId: number,
  // 新状态：待处理、进行中、已完成
  status: "待处理" | "进行中" | "已完成",
}) => any;
```

### get_users
获取用户列表

```typescript
type get_users = (_: {
  // 可选：按角色过滤
  role?: string,
}) => any;
```

### get_product_managers
获取产品经理列表

```typescript
type get_product_managers = () => any;
```

## 使用示例

```typescript
// 1. 注册
await auth_register({
  username: "pm-agent",
  nickname: "PM小助手",
  password: "secure123",
  role: "PM"
});

// 2. 登录获取token
const loginRes = await auth_login({
  username: "pm-agent",
  password: "secure123"
});
const token = loginRes.data.token;

// 3. 创建项目
await create_project({
  name: "新项目",
  description: "项目描述",
  planDate: "2026-04-01"
});

// 4. 创建任务
await create_task({
  requirementId: 1,
  assigneeId: 2,
  title: "开发登录模块",
  type: "开发"
});

// 5. 获取我的任务
const tasks = await get_my_tasks();

// 6. 更新任务状态
await update_task_status({
  taskId: 1,
  status: "已完成"
});
```

## 注意事项

- 大多数API需要在Header中携带Authorization: Bearer {token}
- Agent也可以使用X-API-Key: agent-api-key-12345进行认证
- 登录后会返回token，后续请求需要使用该token
