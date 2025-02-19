# 类：Inst 

Inst 是 Instrument 的缩写。

成员名|类型|解释
---|---|---
id |string|标识名称。由不同Effect施加的Inst具有不同的id，可以通过此id避免重复添加inst
at |array[string]|生效位置，可以看作分类，用作指定类别数据的统计
const|bool|是否为“常量”。如果为否，计算时会把value视为指令，返回该指令的结果。
value |variant|值，任意变量。

## id 标识名称

## 其它内容

- [UnitAttribute 单位属性在战斗系统中的应用](docs/battle_system/unit_attribute.md#inst)
- [类：UnitAttribute](docs/classes/UnitAttribute.md#)