sigit: dict = {
    "id": "sigit",
    "name": "Sigit Gaming",
    "class": "Vigilancer",
    "showdown": True,  # is character equiped?
    "element": "Fire",
    "level": 1,
    "exp": 0,
    "multiplier": 1,  # multiplier each level (stats adjustment)
    "battle": False,  # is in battle?
    "stats": {
        "HP": 98,
        "max_HP": 98,
        "Mana": 45,
        "max_Mana": 45,
        "DEF": 19,
        "ATK": 17,
        "AGI": 87,  # how character arranged in battle
        "Crit_DMG": 1.5,
        "Crit_Rate": 0.05,
    },
    "amplification": {"water": 0, "fire": 0, "ice": 0, "leaf": 0},  # bonus damage
    "resistance": {"water": 0, "fire": 0, "ice": 0, "leaf": 0},  # damage resistance
    "story": {
        "short": "Sigit is a gamer who enjoys playing lots of games at 3am.",
        "long": "When Sigit was playing a game in his room, he felt something strange in his hand. The screen in front of Sigit turned white and he felt a strange energy from his mouse, he seemed to be able to control the surroundings with his game.",
    },
    "buff": [],  # buff in battle
    "debuff": [],  # debuff in battle
    "equipment": [],  # equpment
    "skills": [
        {
            "type": "attack",
            "name": "Mouse Attack",
            "description": "Sigit throws a mouse at an enemy, dealing {percentage}% ATK damage.",
            "ATK": 0.5,
            "level": 1,
        },
        {
            "type": "first",
            "name": "GG Gaming",
            "action": "allies",
            "status": "buff",
            "main": "ATK",
            "cost": 15,
            "cd": 1,
            "cd_left": 0,
            "description": "Sigit shouts GG Gaming to an ally, giving them a {percentage}% ATK buff for 2 turns. This effect unstackable.",
            "ATK": 0,
            "level": 1,
            "buff": {
                "name": "GG Gaming",
                "turn": 2,
                "turn_left": 0,
                "type": "status",
                "status": ["ATK"],
                "ATK": 0.25,
                "amplification": 0,  # calculated amplification from char/target
                "base": "character",
            },
            "debuff": {},
        },
        {
            "type": "second",
            "name": "Lose Streak",
            "status": "attack",
            "action": "aoe",
            "cost": 12,
            "main": "ATK",
            "cd": 2,
            "cd_left": 0,
            "description": "Sigit is furious because he often loses in the game. He throws his PC part to all enemies (AOE), dealing {percentage}% ATK damage.",
            "ATK": 0.75,
            "level": 1,
            "buff": {},
            "debuff": {},
        },
        {
            "type": "third",
            "name": "My Damn PC!",
            "action": "aoe",
            "status": "debuff",
            "cost": 10,
            "cd": 3,
            "cd_left": 0,
            "description": "Sigit was annoyed when his PC lagged. He cursed all enemies and reduced their ATK by {percentage}% of their ATK for 1 turn. This effect unstackable.",
            "ATK": 0,
            "level": 1,
            "main": "ATK",
            "buff": {},
            "debuff": {
                "name": "Lag Issue",
                "turn": 1,
                "turn_left": 0,
                "type": "status",
                "status": ["ATK"],
                "ATK": 0.25,
                "amplification": 0,  # calculated amplification from char/target
                "DOT": False,
                "DMG": 0,
                "base": "target",
            },
        },
    ],
}
