# 📊 定时任务配置说明

## 概述
工作日自动推送五大策略综合选股报告，时间点：**9:20, 11:00, 13:30, 15:00**

---

## 文件清单

### 1. 报告生成脚本
- **send_strategy_email_v3_5.py** - 最新版本，融合多个财经网站
  - 获取实时新闻（ProSearch）
  - 获取股票数据（东方财富API）
  - 生成HTML邮件
  - 发送到 18339435211@139.com

### 2. 定时执行脚本
- **cron_report.py** - 定时任务执行器
  - 调用 send_strategy_email_v3_5.py
  - 记录执行日志
  - 处理错误

### 3. 配置文件
- **email_config.txt** - 邮件配置
  ```
  SMTP_HOST=smtp.qq.com
  SMTP_PORT=465
  SMTP_USER=jing.owne@foxmail.com
  SMTP_PASS=ythdheeocoxodiii
  FROM_NAME=Marcus
  ```

- **cron_config.yaml** - 定时任务配置（参考）
  ```yaml
  schedule: "20 9 * * 1-5"   # 周一到周五 9:20
  schedule: "0 11 * * 1-5"   # 周一到周五 11:00
  schedule: "30 13 * * 1-5"  # 周一到周五 13:30
  schedule: "0 15 * * 1-5"   # 周一到周五 15:00
  ```

---

## 报告内容

### 数据来源
- **东方财富** - 股票行情、涨停板、连板分析
- **新浪财经** - 实时行情、财经新闻
- **同花顺** - 涨停雷达、技术分析
- **财经网** - 经济数据（PMI、GDP等）
- **第一财经** - 深度分析、政策解读
- **ProSearch** - 实时新闻聚合

### 报告结构
1. **🏆 综合胜率TOP10** - 5大策略综合评分排行
2. **⚡ 短线追击** - 涨停板+连板监控（涨幅≥8%）
3. **💡 操作建议** - 买入/卖出信号、止损原则、风险管理
4. **📈 今日总结** - 市场表现、热点板块、政策面、经济数据
5. **策略①-⑤** - 详细数据表格（各25只）
6. **📊 Marcus签名** - 个人身份、免责声明

### 五大策略
| 策略 | 名称 | 指标 | 筛选条件 |
|------|------|------|---------|
| ① | 放量上涨 | 换手率+MACD+KDJ | 按换手率排序 |
| ② | 成交额排名 | 成交量+封单+大单 | 按成交额排序 |
| ③ | 多因子量化 | PE+PB+ROE | 涨幅≥3% |
| ④ | AI技术面 | KDJ+MACD+RSI | 主力净流入>0 |
| ⑤ | 目标价+机构 | 目标价+董监高+北向 | 净流入≥1亿 |

---

## 筛选标准

### 排除条件
- ❌ 新股（上市<3个月）
- ❌ 低流动性标的（日均成交<1亿）
- ❌ 688开头科创板
- ❌ 8开头北交所

### 综合胜率算法
```
基础分 = 50
+ 策略命中数 × 10
+ 主力净流入 × 2
+ 换手率加分（≥5%: +15, ≥2%: +10）
+ 成交额加分（≥10亿: +10）
= 最终胜率（上限97%）
```

### 操作建议
**买入信号:**
- 胜率≥70% 的标的
- MACD + KDJ 双金叉
- 连续3天净流入
- 涨幅≤5%，20天内有涨停

**卖出信号:**
- ⚠️ **止损原则：股票-3% 无条件出**
- 涨幅≥9.5% 且换手率≥5%
- MACD死叉或KDJ高位钝化
- 主力净流出转向

---

## 如何启用定时任务

### 方式1：OpenClaw 内置定时任务（推荐）
```bash
# 查看已配置的定时任务
openclaw cron list

# 启用特定任务
openclaw cron enable stock-report-0920

# 查看任务执行日志
openclaw cron logs stock-report-0920
```

### 方式2：Windows 任务计划程序
```cmd
# 创建任务（以管理员身份运行）
schtasks /create /tn "Stock Report 9:20" /tr "python C:\Users\admin\.qclaw\workspace\cron_report.py" /sc daily /st 09:20 /d MON,TUE,WED,THU,FRI
```

### 方式3：Linux/macOS crontab
```bash
# 编辑 crontab
crontab -e

# 添加以下行
20 9 * * 1-5 python3 /path/to/cron_report.py
0 11 * * 1-5 python3 /path/to/cron_report.py
30 13 * * 1-5 python3 /path/to/cron_report.py
0 15 * * 1-5 python3 /path/to/cron_report.py
```

---

## 故障排查

### 邮件未发送
1. 检查 email_config.txt 配置
2. 验证 SMTP 凭证是否正确
3. 检查网络连接
4. 查看日志：`openclaw cron logs stock-report-0920`

### 数据获取失败
1. 检查东方财富 API 是否可用
2. 验证 ProSearch 网关连接
3. 检查网络代理设置

### 定时任务未执行
1. 确认任务已启用：`openclaw cron list`
2. 检查系统时间是否正确
3. 查看任务日志

---

## 自定义配置

### 修改推送时间
编辑 `cron_config.yaml`，修改 `schedule` 字段：
```yaml
schedule: "0 10 * * 1-5"  # 改为 10:00
```

### 修改收件人
编辑 `send_strategy_email_v3_5.py`，修改最后一行：
```python
send('your_email@example.com', '📊 五大策略综合选股报告 | 2026-03-31', html, cfg)
```

### 修改报告内容
编辑 `send_strategy_email_v3_5.py`，调整：
- 策略筛选条件
- 表格显示数量
- HTML 样式
- 数据来源

---

## 监控和维护

### 日常检查
- 每周检查一次任务执行日志
- 确认邮件是否正常发送
- 验证数据准确性

### 定期更新
- 每月更新一次财经网站爬虫规则
- 根据市场变化调整筛选条件
- 优化报告排版和内容

### 性能优化
- 缓存股票数据，减少 API 调用
- 异步获取新闻，加快报告生成
- 压缩 HTML 邮件大小

---

## 联系方式
- **报告生成**: Marcus（高级日内动量策略师）
- **技术支持**: 查看日志或联系系统管理员
- **反馈建议**: 欢迎提出改进意见

---

**最后更新**: 2026-03-31 18:39 GMT+8
