from modifier import Modifier
from champion import Champion

class Stat:
    default = 0
    max = float('inf')

    def __init__(self, default=0, max=float('inf')):
        self.default = default
        self.max = max
    def __set_name__(self, owner, name):
        self.name = name

        # create property to get base values
        setattr(owner, "base_" + name, property(self.get_base))

        # auto-populate items with stat modifiers
        setattr(Modifier, name, 0)
        setattr(Modifier, "scaling_" + name, 0)
        setattr(Modifier, "base_" + name, 0)
        setattr(Modifier, "max_" + name, 0)
        setattr(Champion, name, self.default)

    def __get__(self, instance, owner):
        base = self.get_base(instance)
        bonus = sum(getattr(item, self.name) for item in instance.items)
        bonus += sum(getattr(item, "scaling_" + self.name) for item in instance.items) * instance.level
        total = base + bonus
        return min(total, self.max)

    def get_base(self, instance):
        base = getattr(instance.champion, self.name)
        scaling = getattr(instance.champion, "scaling_" + self.name)
        level_mult = (instance.level - 1) * (0.685 + 0.0175 * instance.level)
        base_mult = sum(getattr(item, "base_" + self.name) for item in instance.items)
        return (base + scaling * level_mult) * (1 + base_mult)

    base = property(get_base)


class Character:
    champion = None
    level = 1
    items = []
    runes = []

    ad = Stat()
    ap = Stat()
    move_speed = Stat()  # TODO: This probably needs to be subclassed to account for the soft caps
    health = Stat()
    mana = Stat()
    armor = Stat()
    mr = Stat()
    flat_armor_pen = Stat()
    percent_armor_pen = Stat()
    bonus_armor_pen = Stat()
    flat_magic_pen = Stat()
    percent_magic_pen = Stat()
    attack_speed = Stat()
    crit_chance = Stat()
    crit_damage = Stat(default=2)
    life_steal = Stat()
    range = Stat()
    health_regen = Stat()
    tenacity = Stat()
    cdr = Stat(max=40)
    mana_regen = Stat()
    spell_vamp = Stat()

