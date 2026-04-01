# 🔧 调试模式说明

## 概述
调试模式用于测试和验证报告生成逻辑，**不会发送任何邮件**。

---

## 启用调试模式

### 方式1：Windows 批处理脚本（推荐）
```bash
debug_report.bat
```

### 方式2：PowerShell
```powershell
$env:DEBUG_MODE='true'
python send_strategy_email_v3_6.py
```

### 方式3：命令行
```bash
# Windows CMD
set DEBUG_MODE=true
python send_strategy_email_v3_6.py

# Linux/macOS
export DEBUG_MODE=true
python3 send_strategy_email_v3_6.py
```

---

## 调试模式输出

启用调试模式时，脚本会输出：

```
[DEBUG] 调试模式已启用 - 不会发送任何邮件
Fetching news from ProSearch...
Fetching stock data...
Got 31 s1, 29 s2, 1 s3, 60 s4, 63 s5
Total ranked: 107, short-term: 1
[DEBUG] 邮件发送已跳过（调试模式）
[DEBUG] 收件人: 18339435211@139.com
[DEBUG] 抄送: 732016354@qq.com,850229452@qq.com,2625260548@qq.com
[DEBUG] 主题: 📊 五大策略综合选股报告 | 2026-03-31
[DEBUG] 报告生成完成（未发送）
```

---

## 调试检查清单

### ✓ 数据获取
- [ ] ProSearch 新闻获取成功
- [ ] 股票数据获取成功
- [ ] 数据行数符合预期

### ✓ 报告生成
- [ ] 五大策略数据正确
- [ ] 综合胜率排行正确
- [ ] 短线追击标的正确
- [ ] HTML 格式正确

### ✓ 邮件配置
- [ ] 收件人地址正确
- [ ] 抄送地址正确
- [ ] 邮件主题正确

---

## 常见问题

### Q: 调试模式下为什么没有发送邮件？
A: 这是正常的。调试模式的目的就是不发送邮件，只验证逻辑。

### Q: 如何关闭调试模式？
A: 直接运行 `send_strategy_email_v3_6.py`（不设置 DEBUG_MODE 环境变量）

### Q: 调试模式下可以检查什么？
A: 
- 数据获取是否正常
- 报告生成是否正确
- 邮件配置是否完整
- 持仓分析是否准确

### Q: 如何在调试模式下保存报告？
A: 修改脚本，在 `send()` 函数中添加文件保存逻辑

---

## 调试工作流

1. **启用调试模式**
   ```bash
   debug_report.bat
   ```

2. **检查输出**
   - 确认数据获取成功
   - 确认报告生成成功
   - 确认邮件配置正确

3. **验证数据**
   - 检查股票数据是否准确
   - 检查策略筛选是否正确
   - 检查胜率计算是否准确

4. **关闭调试模式**
   - 直接运行 `send_strategy_email_v3_6.py`
   - 或设置 `DEBUG_MODE=false`

5. **发送正式报告**
   - 运行 `setup_cron.bat` 设置定时任务
   - 或手动运行 `cron_integrated.py`

---

## 调试技巧

### 保存报告到文件
编辑 `send_strategy_email_v3_6.py`，在最后添加：
```python
# 保存 HTML 报告
with open('report_debug.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('[DEBUG] 报告已保存到 report_debug.html')
```

### 输出详细日志
在脚本开头添加：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 检查特定策略
修改 `clean_stocks()` 函数的筛选条件，测试不同的策略

---

## 环境变量

| 变量 | 值 | 说明 |
|------|-----|------|
| DEBUG_MODE | true | 启用调试模式（不发送邮件） |
| DEBUG_MODE | false | 禁用调试模式（正常发送邮件） |

---

**最后更新**: 2026-03-31 19:40 GMT+8
