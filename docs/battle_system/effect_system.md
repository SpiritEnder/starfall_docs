# 效果
!!! note

    *“一切都是效果。”* <p align="right">——SpiritEnder</p>

效果是回合制的绝佳调料。无论是眩晕，还是dot，减益增益，都是效果`Effect`的功劳。

## 效果是啥？

一切的设计都源于需求。让我们设想一个最基础的效果：

> 攻击力提升20%，持续2回合。

我们当然需要一个**效果对象**来管理这些“效果”。最简单的设想是，效果对象控制其要更改的属性，以及持续时间。

> Effect( *属性名*, *计算方式*, *数值*, *持续回合* )  
> Effect(“攻击力”, “乘”, 0.2, 2)

然后将该效果附属在角色属性UnitAttributes中。每当读取**攻击力**的时候，就统计所有属性名为**攻击力**的效果，并按规则计算数值：

```py
func get_attr(attr_name):
    var value_base = self.get(name) # 获得指定属性的基础值
    var value_add = 0.0 # 加值
    var value_mul = 1.0 # 乘值
    for effect in effect_list: # 遍历单位属性的效果列表
        if effect.attr_name == attr_name: # 仅考虑更改指定属性的效果 
            if effect.caculate_mode == "乘":
                valur_mul *= effect.value
            elif effect.caculate_mode == "加":
                valur_add += effect.value
            elif ...
    return value_base * value_mul + value_add ... # 按指定规则计算数据并返回

func round_end(): # 回合结束时触发
    ...
    for unit in units: # 遍历角色属性
        ...
        var list_to_be_deleted # 待删除效果
        for effect in effect_list: # 遍历效果列表
            effect.continue_round -= 1 # 持续回合数减一
            if effect.continue_round == 0:
                list_to_be_deleted.append(effect) # 如果持续回合耗尽，将效果标记为待删除
        for effect in list_to_be_deleted:
            effect_list.erase(effect) # 根据待删除列表移除角色属性中的效果
        list_to_be_deleted.free() # 清空待删除列表
    ...
```

!!! note  
    不要在遍历过程中删除元素！

但是很显然，这个东西的扩展性不强。但凡小改一下条件：

- 攻击力提升，**数值为生命上限的20%**，持续两回合。
- 攻击力提升20%，**当角色持有护盾时触发**。
- **攻击敌方后排角色时**，攻击力提升20%，持续两回合。

再按照原来的思路设计就爆了。那咋办呢？

我们再根据当前的需求做进一步设计：

- 效果的数值可以动态调整
- 效果的触发条件多元化
- 修改已经掷出的其他`object`

很显然，单单效果这一个类已经无法做到这么多事情了。让我们先看看其它已有的设计，有没有可以复用的玩意：

- [指令系统：动态数据获取和计算](command_system.md#指令系统)
- [Inst计算块：高拓展性的轻量数据组件](unit_attribute.md#类inst)

现在一切都可以实现了！……吗？


## 效果的效果是什么？

在游戏中，技能可以向单位添加效果。  
`unit.effect_list.append(*效果*)`

效果在被添加时，会向当前的关卡注册其持有的触发器。

## 其他的内容


### <span id="class.UnitEffect">类：UnitEffect (效果)</span>

文档中简称为Effect。

成员名|类型|解释
---|---|---
name |String | 效果名，唯一标识
tag |Array | 标签（文本数组）
visible |bool | 可见状态，效果是否展示在状态栏
trigger |Array[UnitEffectTrigger] | 效果触发器集合，单个元素为[UnitEffectTrigger](#class.UnitEffectTrigger)
effect |Array | 实际效果(指令)
content |Dictionary | 展示的文本和图像内容

### <span id="class.UnitEffectTrigger">类：UnitEffectTrigger (效果触发器)</span>

文档中简称为EffectTrigger。

成员名|类型|解释
---|---|---
trigger_name |String | 触发器识别名
trigger_times |int | 总生效次数
trigger_times_run |bool | 触发时是否执行指令
trigger_destroy |bool | 触发次数耗尽时是否销毁效果
trigger_destroy_run| bool | 触发次数耗尽时是否执行指令
trigger_global |bool | 是否为全局触发器
target |[UnitEffect](#class.UnitEffect) | 指向其触发的效果

#### 系统内置触发器

内置触发器识别名|触发位置|参考条目
---|---|---
 round_start| 角色回合开始时|[回合系统：回合前后](round_system.md#before_and_after_the_round)
 round_end| 角色回合结束时|[回合系统：回合前后](round_system.md#before_and_after_the_round)
 global_round_start| 全局回合开始时|[回合系统：全局回合](round_system.md#全局回合)
 global_round_end| 全局回合结束时|
 skill_emit| 角色技能施放前|
 skill_emit_after| 角色技能施放后|
 skip| 角色跳过轮次行动时|
 target_effect_append| 向目标添加效果前|
 target_effect_append_after| 向目标添加效果后|
 target_effect_remove| 为目标移除效果时|
 target_effect_remove_after| 为目标移除效果后|
 effect_append| 自身被添加效果时|
 effect_append_after| 自身被添加效果后|
 effect_remove| 为自身移除效果时|
 effect_remove_after| 为自身移除效果后|
 state_health| 自身接受治疗时|
 state_damage| 自身受到伤害时|
 state_shield| 自身护盾量变化时|
 state_zero| 自身血量归零时|
 state_revive| 自身被复活时|
 state_kill| 自身被击杀时|
 target_state_health| 敌方接受治疗时|
 target_state_damage| 敌方受到伤害时|
 target_state_shield|敌方护盾量变化时|
 target_state_zero| 敌方血量归零时|
 target_state_revive| 敌方被复活时|
 target_state_kill| 敌方被击杀时 |