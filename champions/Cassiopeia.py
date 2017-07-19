from champion import Champion


class Cassiopeia(Champion):
    name = 'Cassiopeia'
    ad = 53.0
    scaling_ad = 3.0
    armor = 25.0
    scaling_armor = 3.5
    attack_speed = 0.647
    scaling_base_attack_speed = 0.015
    health = 525.0
    scaling_health = 75.0
    health_regen = 5.5
    scaling_health_regen = 0.5
    mana = 375.0
    scaling_mana = 60.0
    mana_regen = 6.0
    scaling_mana_regen = 0.8
    move_speed = 328.0
    mr = 30.0
    scaling_mr = 0.5
    range = 550.0

    # scaling_move_speed won't work here as that is non-linear
    @property
    def move_speed(self):
        return 328 + 4 * self.character.level
