from typing import List, Dict, Iterable
from modifier import Modifier
from champion import Champion
from functools import reduce
from item import Item
import operator


def product(iterable):
    return reduce(operator.mul, iterable, 1)


class Stat:
    caps: Dict[float, float] = {}
    default: float = 0
    max: float = float('inf')

    def __init__(self, default=0, max=float('inf'), caps=None):
        self.caps = caps
        self.default = default
        self.max = max

    def __set_name__(self, owner, name: str):
        self.name = name

        # create property to get base values
        setattr(owner, "base_" + name, property(self.get_base))

        # auto-populate items with stat modifiers
        setattr(Modifier, name, 0)
        setattr(Modifier, "scaling_" + name, 0)
        setattr(Modifier, "base_" + name, 0)
        setattr(Modifier, "max_" + name, 0)
        setattr(Champion, name, self.default)

    def __get__(self, instance, owner) -> float:
        base = self.get_base(instance)
        bonus = sum(getattr(item, self.name) for item in instance.items)
        bonus += sum(getattr(item, "scaling_" + self.name) for item in instance.items) * instance.level
        total = base + bonus
        if self.caps:
            total = self._cap(total)
        return min(total, self.max)

    def get_base(self, instance) -> float:
        base = getattr(instance.champion, self.name)
        scaling = getattr(instance.champion, "scaling_" + self.name)
        level_mult = (instance.level - 1) * (0.685 + 0.0175 * instance.level)
        base_mult = sum(getattr(item, "base_" + self.name) for item in instance.items)
        return (base + scaling * level_mult) * (1 + base_mult)

    def _cap(self, uncapped: float) -> float:
        total = 0
        thresholds = sorted(self.caps.keys(), reverse=True)
        for threshold in thresholds:
            if uncapped < threshold:
                continue
            total += (uncapped - threshold) * self.caps[threshold]
            uncapped = threshold

        return total + uncapped


class MultStat:
    default = 0

    def __init__(self, default=0):
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name

        # auto-populate items with stat modifiers
        setattr(Modifier, name, 0)
        setattr(Champion, name, self.default)

    def __get__(self, instance, owner):
        base = 1 - getattr(instance.champion, self.name)
        bonus = product(1-getattr(mod, self.name) for mod in instance.modifiers)
        total = base * bonus
        return 1-total


class Character:
    champion: Champion = None
    level: int = 1
    items: List[Item] = []
    masteries = []
    runes = []

    ad = Stat()
    ap = Stat()
    move_speed = Stat(caps={415: .8, 490: .5})
    health = Stat()
    mana = Stat()
    armor = Stat()
    mr = Stat()
    lethality = Stat()
    percent_armor_pen = MultStat()
    bonus_armor_pen = MultStat()
    flat_magic_pen = Stat()
    percent_magic_pen = MultStat()
    attack_speed = Stat(max=2.5)
    crit_chance = Stat(max=100)
    crit_damage = Stat(default=2)
    life_steal = Stat()
    range = Stat()
    health_regen = Stat()
    tenacity = MultStat()
    cdr = Stat(max=40)
    mana_regen = Stat()
    spell_vamp = Stat()

    @property
    def flat_armor_pen(self):
        return self.lethality * (.6 + self.level / 18 * .4)

    @property
    def modifiers(self) -> Iterable[Modifier]:
        return self.items + self.masteries + self.runes
