# 效果
> *“一切都是效果。”* <p align="right">——SpiritEnder</p>

效果是回合制的绝佳调料。无论是眩晕，还是dot，减益增益，都是效果`Effect`的功劳。

## 类：UnitEffect (效果)

文档中简称为Effect。

成员名（类型）|解释
---|---
name (String) | 效果名，唯一标识
tag (Array) | 标签（文本数组）
visible (bool) | 可见状态，效果是否展示在状态栏
trigger (Array[UnitEffectTrigger]) | 效果触发器集合，单个项目为[UnitEffectTrigger](#类uniteffecttrigger-效果触发器)
effect (Array) | 实际效果(指令)
content (Dictionary) | 展示的文本和图像内容

## 类：UnitEffectTrigger (效果触发器)

文档中简称为EffectTrigger。

成员名（类型）|解释
---|---
trigger_name (String) | 触发器识别名
trigger_times (int) | 总生效次数
trigger_times_run (bool) | 触发时是否执行指令
trigger_destroy (bool) | 触发次数耗尽时是否销毁效果
trigger_destroy_run (bool) | 触发次数耗尽时是否执行指令
trigger_global (bool) | 是否为全局触发器
target (UnitEffect) | 指向其触发的效果

## 效果如何作用

在游戏中，技能可以向单位添加效果。  
`unit.effect_list.append(*效果*)`

效果在被添加时，会向当前的关卡注册其持有的触发器。

## 其他的内容
### 系统内置效果器

效果触发位置|解释
---|---
 round_start| 角色回合开始时
 round_end| 角色回合结束时
 global_round_start| 全局回合开始时
 global_round_end| 全局回合结束时
 skill_emit| 角色技能施放前
 skill_emit_after| 角色技能施放后
 skip| 角色跳过轮次行动时
 target_effect_append| 向目标添加效果前
 target_effect_append_after| 向目标添加效果后
 target_effect_remove| 为目标移除效果时
 target_effect_remove_after| 为目标移除效果后
 effect_append| 自身被添加效果时
 effect_append_after| 自身被添加效果后
 effect_remove| 为自身移除效果时
 effect_remove_after| 为自身移除效果后
 state_health| 自身接受治疗时
 state_damage| 自身受到伤害时
 state_shield| 自身护盾量变化时
 state_zero| 自身血量归零时
 state_revive| 自身被复活时
 state_kill| 自身被击杀时
 target_state_health| 敌方接受治疗时
 target_state_damage| 敌方受到伤害时
 target_state_shield|敌方护盾量变化时
 target_state_zero| 敌方血量归零时
 target_state_revive| 敌方被复活时
 target_state_kill| 敌方被击杀时 