# NOMAD 账户注册指南

**创建日期:** 2026-03-10  
**目的:** 获取 NOMAD API Token 用于数据获取

---

## 🚀 注册步骤

### 步骤 1: 访问 NOMAD

**URL:** https://nomad-lab.eu/

---

### 步骤 2: 注册账户

1. 点击右上角 **"Login"**
2. 选择 **"Register"**
3. 填写信息:
   - **Email:** 你的邮箱
   - **Password:** 设置密码
   - **Name:** 你的姓名
   - **Affiliation:** 机构/学校 (可选)
4. 点击 **"Register"**
5. 验证邮箱 (查收确认邮件)

---

### 步骤 3: 获取 API Token

1. 登录后访问：https://nomad-lab.eu/user/
2. 找到 **"API Token"** 或 **"Access Token"**
3. 复制 Token (格式类似：`abc123xyz...`)

---

### 步骤 4: 配置脚本

编辑 `scripts/nomad_fetcher.py`:

```python
NOMAD_TOKEN = "你的 Token"  # 粘贴复制的 Token
```

---

### 步骤 5: 测试

```bash
cd D:\OpenClaw\workspace\11-research\cnt-research
py scripts/nomad_fetcher.py --query "carbon nanotube" --limit 10
```

---

## 📊 NOMAD 数据说明

**数据类型:**
- 计算材料科学数据
- DFT 计算结果
- 电子结构、能带、态密度等

**CNT 相关数据:**
- 碳纳米管电子性质
- 石墨烯计算数据
- 纳米材料模拟结果

**目标:** 获取 50+ CNT 相关记录

---

## ⚠️ 注意事项

1. **Token 保密:** 不要提交到 Git
2. **API 限制:** 有请求频率限制
3. **数据许可:** 遵守 NOMAD 数据使用协议

---

## 🔗 相关资源

- **NOMAD 官网:** https://nomad-lab.eu/
- **API 文档:** https://nomad-lab.eu/prod/v1/api/
- **数据搜索:** https://nomad-lab.eu/prod/v1/search/

---

*最后更新：2026-03-10*
