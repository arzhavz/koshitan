akira: dict = {
    "id": "akira",
    "name": "Gus Akira",
    "class": "Priest",
    "showdown": True,  # is character equiped?
    "element": "Leaf",
    "level": 1,
    "exp": 0,
    "multiplier": 1,  # multiplier each level (stats adjustment)
    "battle": False,  # is in battle?
    "stats": {
        "HP": 106,
        "max_HP": 106,
        "Mana": 42,
        "max_Mana": 42,
        "DEF": 17,
        "ATK": 15,
        "AGI": 90,  # how character arranged in battle
        "Crit_DMG": 1.5,
        "Crit_Rate": 0.05,
    },
    "amplification": {"water": 0, "fire": 0, "ice": 0, "leaf": 0},  # bonus damage
    "resistance": {"water": 0, "fire": 0, "ice": 0, "leaf": 0},  # damage resistance
    "story": {
        "short": "Gus Akira is known for being eccentric and having abilities as a religious figure.",
        "long": "Gus Akira gained power when he accidentally hit a banana tree in the garden. He became aware of his magical ability to spread goodness. With his ability, he can give spirit to everyone. Because of his simple appearance, he is famous for his simplicity.",
    },
    "buff": [],  # buff in battle
    "debuff": [],  # debuff in battle
    "equipment": [],  # equpment
    "skills": [
        {
            "type": "attack",
            "name": "A Wise Handshake",
            "description": "Gus Akira gives a handshake that creates an aura of kindness, attacking a single target with {percentage}% ATK damage.",
            "ATK": 0.5,
            "level": 1,
        },
        {
            "type": "first",
            "name": "Holy Prayer Water",
            "action": "ally",
            "status": "heal",
            "main": "max_HP",
            "heal": "HP",
            "cost": 8,
            "cd": 1,
            "cd_left": 0,
            "description": "Gus Akira gives holy water that has been given a prayer to the ally, restoring HP by {percentage}% of Gus Akira's HP.",
            "max_HP": 0.35,
            "level": 1,
            "buff": {},
            "debuff": {},
        },
        {
            "type": "second",
            "name": "Motorcycle Propeller",
            "action": "single",
            "status": "attack",
            "main": "ATK",
            "cost": 14,
            "cd": 2,
            "cd_left": 0,
            "description": "Gus Akira crashes his signature motorbike into a single target, dealing {percentage}% ATK damage.",
            "ATK": 0.95,
            "level": 1,
            "buff": {},
            "debuff": {},
        },
        {
            "type": "third",
            "name": "Holy Preaching",
            "action": "single",
            "status": "dot",
            "main": "ATK",
            "cost": 17,
            "cd": 3,
            "cd_left": 0,
            "description": "Gus Akira gives preaching to one enemy, giving DoT of {percentage}% ATK for 2 turns.",
            "ATK": 0,
            "level": 1,
            "buff": {},
            "debuff": {
                "name": "Gus Akira's Preaching",
                "turn": 2,
                "turn_left": 0,
                "ATK": 0.2,
                "DOT": True,
                "DMG": 0,
                "base": "character",
            },
        },
    ],
}
