<span id="class.UnitEffect">类：UnitEffect (效果)</span>
===

文档中简称为Effect。

成员名|类型|解释
---|---|---
[effect_name](#struct.effect_name) | String | 效果名，唯一标识
[effect_tag](#struct.effect_tag) | Array | 标签（文本数组）
[effect_resource](#struct.effect_resource) | Dictionary | 效果资源，展示的文本和图像内容。
[effect_trigger](#struct.effect_trigger) | Dictionary | 效果触发器，键值对为触发名及其回调函数。
[effect_callback](#struct.effect_callback) | Dictionary | 键：触发名，值：效果触发回调函数（[Inst](/battle_system/unit_attribute#class.inst)的集合）
[effect_data](#struct.effect_data) | Dictionary | 储存效果中可能会使用到的辅助元数据，比如剩余回合数或剩余生效次数

<span id="struct.effect_name">effect_name 效果名称</span>
---

用于唯一表示效果。具有相同效果名称的效果重复添加时，只会刷新属性而不是建立一个新效果。若要使效果看起来是可叠加的，可以考虑使用`_restore`触发，并在回调中写叠层逻辑。

<span id="struct.effect_tag">effect_tag 效果标签</span>
---

标签数组，用于标识效果的各种类型，用于辅助系统和其他指令。比如，标注这个效果是增益还是减益。下面提供了一些常用的标签和含义：

- [所有的标签(tags)](/constant/all_the_tags#)

<span id="struct.effect_resource">effect_resource 效果资源</span>
---

这并不是一个类。以下提供了系统内置的可能会读取或展示的属性，不须全部包含。

成员名|类型|解释
---|---|---
visible|bool|可见状态，效果是否展示在状态栏。*必须包含*
title|String|标题文本，可选
content|String|内容文本，可选
icon|Image|图标，可选

<span id="struct.effect_trigger">effect_trigger 效果触发器</span>
---

键：触发器识别名。可以使用内置识别名，也可以自定义。  
值：回调函数名。即`effect_callback`中的键。

内置识别名有固定的触发位置。在使用内置识别名时，系统在指定的位置会激活触发器，并执行效果在`值`中指定的回调函数。  
自定义识别名不会自动触发，需要在技能或是指令中使用`-trigger`来手动触发。

触发效果时，指令会在尾部附加一个`data`，类型为词典，包含了一部分可能会用到的已有参数，比如，效果本身（键为`effect`）。对于局部触发器，还会默认提供持有该效果的单位（键为`unit`）。  

!!! Note
你可以在指令中使用`-get`来获取词典内的值，比如*get*,*effect*,`data`，等同于`data[effect]`。详见[指令系统](/battle_system/command_system#)

内置触发器识别名|触发位置|提供条目|参考条目
---|---|---|---
 round_start| 角色回合开始时 | `上一位行动者` | [回合系统：回合前后](/battle_system/round_system#before_and_after_the_round)
 round_end| 角色回合结束时 | `行动结果`、`下一位行动者` |[回合系统：回合前后](/battle_system/round_system#before_and_after_the_round)
 global_round_start| 全局回合开始时||[回合系统：全局回合](/battle_system/round_system#全局回合)
 global_round_end| 全局回合结束时||
 skill_emit| 角色技能施放前|`将要施放的技能`||
 skill_emit_after| 角色技能施放后|`技能结果`||
 skip| 角色跳过轮次行动时|`跳过轮次技能`||
 target_effect_append| 向目标添加效果前|`目标`|
 target_effect_append_after| 向目标添加效果后|`目标`|
 target_effect_remove| 为目标移除效果时|`目标`|
 target_effect_remove_after| 为目标移除效果后|`目标`|
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
 
<span id="struct.effect_callback">effect_callback 效果回调</span>
---

键：触发名  
值：Inst的集合。

当效果被触发时，会执行效果回调中的inst。比如：

```python
effect_callback["round_start"] = [
  {Inst_1},
  {Inst_2},
  ...
]
```

当触发`round_start`时，会按顺序执行`Inst_1`,`Inst_2`...  
指定回调名下的所有inst都会执行，如果想要中断，请在后续的inst中使用逻辑判断，比如设置和读取`data["continue"] = false`
 
<span id="struct.effect_data">effect_data 效果数据</span>
---

效果触发时，在指令中默认提供。对`effect`使用`-get,effect_data`访问。

对于计次触发或计回合触发，就可以借用`effect_data`来判定。比如：

```python
effect_data["round"] = 2

effect_trigger["round_start"] = "round_counter" # 系统内置触发round_start时，执行回调函数round_counter

effect_callback["round_counter"] = [{
  -set,round,  # 将回合设置为：
    -sub,  # 原有回合数减一
      -get,round,
        -get,effect_data
      1,
    -get,effect_data,
    
  -var,effect_data  # 将effect_data设置为一个临时量，以引用传递
    -get,effect_data,
      -get,effect,
        -data, # 获取系统提供的参数
}]
effect_callback["destroy_test"] = [{
  # 移除效果
  -remove,effect,
    -get,effect,
      -data
  # 判断剩余回合数是否小于等于0，如果为真则执行上述指令
  -if,<=,0
    -get,round,
      -get,effect_data,
        -get,effect,
          -data
}]
```

## 其他内容

- [effect_system 效果系统](/battle_system/effect_system#effect)