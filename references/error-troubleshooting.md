# SPSS 常见错误排查手册

## 一、数据文件问题

### 1.1 打开文件失败

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| "无法打开文件" | 文件路径含中文/特殊字符 | 将文件移到纯英文路径 |
| "文件格式不识别" | 文件扩展名与内容不匹配 | 确认 .sav/.csv/.xlsx 格式正确 |
| "密码保护" | 数据文件有密码 | 输入密码或联系数据来源方 |
| "版本不兼容" | 高版本 SPSS 保存的文件用低版本打开 | 用高版本重新保存为兼容格式 |

### 1.2 数据导入问题

**CSV 导入后变量类型错误**：
```spss
* 问题: 数值变量被识别为字符串
* 原因: CSV 中有非数字字符（如 "N/A"、"--"、空格）

* 解决: 先清理数据，再导入
* 或在导入时指定变量类型:
GET DATA /TYPE=TXT
  /FILE='data.csv'
  /DELIMITERS=","
  /FIRSTCASE=2
  /VARIABLES=id F5.0 name A20 score F5.2.
```

**Excel 导入后中文乱码**：
- 确保 Excel 文件编码为 UTF-8
- 或在 SPSS 中设置：`Edit → Options → General → Character Encoding for Data Files → UTF-8`

---

## 二、变量操作问题

### 2.1 变量名错误

| 错误 | 原因 | 解决 |
|------|------|------|
| "变量名不唯一" | 有重名变量 | 重命名：`RENAME VARIABLES (dup = dup2).` |
| "变量名以数字开头" | SPSS 要求变量名以字母或 @ 开头 | 改名：如 `2group` → `group2` |
| "变量名过长" | 超过 64 字符 | 缩短变量名 |
| "变量名含空格" | SPSS 不允许变量名含空格 | 用下划线替代：`my_var` |

### 2.2 COMPUTE / RECODE 不生效

```spss
* 问题: COMPUTE 后数据没变化
* 原因: 忘记加 EXECUTE

COMPUTE new_var = old_var * 2.
EXECUTE.  /* 必须加这行! */

* 问题: RECODE 后值标签丢失
* 解决: 重新添加值标签
RECODE gender (1=2)(2=1).
VALUE LABELS gender 1 '女' 2 '男'.
EXECUTE.
```

### 2.3 缺失值处理问题

```spss
* 问题: 计算均值时出现 "系统缺失"
* 原因: 任何参与计算的变量有缺失，结果就是缺失

* 解决 1: 用 MEAN() 函数（自动忽略缺失值，但要求至少 N 个有效值）
COMPUTE score = MEAN.3(item1, item2, item3, item4, item5).
/* .3 表示至少需要 3 个有效值才计算 */

* 解决 2: 用 SUM() 同理
COMPUTE total = SUM.3(item1, item2, item3, item4, item5).

* 问题: 用户缺失值与系统缺失值混淆
* 系统缺失显示为 "." — 没有被赋值
* 用户缺失显示为你设定的值 — 用 MISSING VALUES 设定
MISSING VALUES var1 (9, 99).
```

---

## 三、分析操作问题

### 3.1 t 检验

| 问题 | 原因 | 解决 |
|------|------|------|
| "分组变量只有 1 个有效值" | 分组变量编码不对 | 检查 `VALUE LABELS` 和分组定义 |
| 输出只有系统缺失 | 变量含太多缺失值 | 先清洗数据 |
| 方差齐性不满足 | 两组方差差异大 | 读 "不等方差" 那一行 (Welch) |

### 3.2 ANOVA

```spss
* 问题: 事后检验结果为空
* 原因: F 检验不显著时 SPSS 默认不输出事后检验

* 解决: 即使不显著也强制输出
ONEWAY score BY group
  /POSTHOC=TUKEY ALPHA(0.05).

* 问题: "至少需要两组" 报错
* 原因: 分组变量只有一个有效类别
* 解决: 检查分组变量的频率分布
FREQUENCIES VARIABLES=group.
```

### 3.3 回归分析

```spss
* 问题: "因变量为常数" 报错
* 原因: DV 没有变异（所有值相同）或全部缺失
* 解决: 检查 DV 的描述统计

* 问题: VIF > 10 (多重共线性)
* 解决方案 (按优先级):
* 1. 删除高相关的自变量
* 2. 用主成分回归
* 3. 用岭回归

* 问题: 残差不正态
* 解决: 对 DV 做对数转换
COMPUTE log_dv = LG10(dv).
EXECUTE.

* 问题: "自变量间存在完全共线性"
* 原因: 某个 IV 是其他 IV 的线性组合
* 解决: 逐个检查相关矩阵，删除 r > .90 的变量
CORRELATIONS /VARIABLES=iv1 iv2 iv3 iv4 /PRINT=TWOTAIL NOSIG.
```

### 3.4 因子分析

```spss
* 问题: KMO < .60
* 原因: 变量间相关太弱，不适合做因子分析
* 解决: 删除与其他变量相关低的题项，重新计算 KMO

* 问题: 提取的因子数与预期不符
* 原因: 特征值 > 1 标准可能不准确
* 解决: 结合碎石图和理论判断因子数
FACTOR
  /VARIABLES item1 TO item20
  /PLOT EIGEN
  /CRITERIA MINEIGEN(1)
  /EXTRACTION PC.
* 手动指定因子数:
FACTOR
  /CRITERIA FACTORS(3).  /* 提取 3 个因子 */

* 问题: 某个题项在两个因子上都有高载荷 (交叉载荷)
* 解决: 删除该题项，或用 Promax 旋转允许因子相关
```

### 3.5 信度分析

```spss
* 问题: α < .70
* 解决步骤:
* 1. 检查是否有反向题未反转
FREQUENCIES VARIABLES=item3 item5 item7.
* 2. 查看 "删除该项后的 α"，删除使 α 上升的题项
* 3. 查看 CITC < .30 的题项
* 4. 检查是否混入了不同维度的题项

* 问题: α 为负值
* 原因: 题项间出现负相关（通常是因为反向题未处理）
* 解决: 找到并反转反向题
```

### 3.6 卡方检验

```spss
* 问题: 期望频率 < 5 的格子超过 20%
* 解决 1: 用 Fisher 精确检验
CROSSTABS
  /TABLES=var1 BY var2
  /STATISTICS=CHISQ
  /CELLS=COUNT EXPECTED.

* 解决 2: 合并类别（减少行或列数）
RECODE edu (1=1)(2=1)(3=2)(4=3)(5=3).
VALUE LABELS edu 1 '低' 2 '中' 3 '高'.
EXECUTE.
```

---

## 四、语法问题

### 4.1 常见语法错误

| 错误 | 原因 | 解决 |
|------|------|------|
| "命令未终止" | 忘记加句号 `.` | 检查每个命令是否以 `.` 结尾 |
| "无法识别的命令" | 关键字拼写错误 | 核对命令拼写 |
| "子命令不允许在此处" | 子命令顺序不对 | 调整顺序 |
| "变量不存在" | 变量名拼写错误 | 用 `DISPLAY DICTIONARY.` 查看所有变量名 |
| "字符串值用于数值变量" | 类型不匹配 | 用 AUTORECODE 转换 |
| "缺少必需的子命令" | 漏了必须指定的参数 | 补充完整 |

### 4.2 中文路径问题

```spss
* 问题: 文件路径含中文导致报错
* 解决 1: 用纯英文路径
GET FILE='C:\data\mydata.sav'.

* 解决 2: 用 Unicode 模式
SET UNICODE=ON.
GET FILE='C:\数据\我的数据.sav'.
```

### 4.3 编码问题

```spss
* 问题: 中文变量标签显示乱码
* 解决: 设置编码
SET LOCALE='Chinese (Simplified)_China.936'.

* 或在 Edit → Options → General 中设置
```

---

## 五、输出问题

### 5.1 输出为空

| 原因 | 解决 |
|------|------|
| 没有数据 | 检查是否选择了正确的数据文件 |
| 全部是缺失值 | 检查变量的缺失值情况 |
| FILTER/SPLIT FILE 生效 | 运行 `USE ALL.` 和 `SPLIT FILE OFF.` |
| SELECT IF 条件太严格 | 放宽选择条件 |

### 5.2 输出表格被截断

```spss
* 设置输出表格宽度
SET TLOOK='C:\Program Files\IBM\SPSS\Styles\Looks\StandardT.stt'.

* 或在 Edit → Options → Pivot Tables 中设置
```

### 5.3 导出输出

```spss
* 导出为 Word (推荐)
OUTPUT EXPORT
  /CONTENTS EXPORT=VISIBLE
  /DOCX DOCUMENTFILE='output.docx'.

* 仅导出特定表格
OUTPUT EXPORT
  /SELECT TABLES=1 3 5
  /DOCX DOCUMENTFILE='selected.docx'.
```

---

## 六、性能问题

### 6.1 大数据集运行缓慢

| 原因 | 解决 |
|------|------|
| 数据量太大 | 用 `SAMPLE` 命令抽样 |
| 变量太多 | 只选择需要的变量 |
| 输出太多 | 减少输出选项 |
| 内存不足 | 关闭其他程序，增加 SPSS 内存设置 |

```spss
* 抽样 10% 的数据做预分析
SAMPLE .1.
EXECUTE.

* 或指定样本量
SAMPLE 500 FROM 5000.
EXECUTE.
```

### 6.2 SPSS 崩溃

- 保存工作：`SAVE OUTFILE='backup.sav'.`
- 定期保存输出：`OUTPUT SAVE OUTFILE='backup.spv'.`
- 检查数据量是否超出 SPSS 版本限制
- 尝试重启 SPSS 后重新打开自动恢复文件
