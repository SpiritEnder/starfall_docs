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

- [指令系统：动态数据获取和计算](/battle_system/command_system#)
- [Inst计算块](/classes/Inst#)

现在一切都可以实现了！……吗？

## <span id="effect">效果</span>

- [类：UnitEffect](/classes/UnitEffect#class.UnitEffect)

## 效果的效果是什么？

在游戏中，技能可以向单位添加效果。  
`unit.effect_list.append(*效果*)`

效果在被添加时，会向当前的关卡注册其持有的触发器。

## 其他的内容


