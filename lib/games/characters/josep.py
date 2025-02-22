josep: dict = {
    "id": "josep",
    "name": "Josep Bremanta Samuel",
    "class": "Warrior",
    "showdown": True,  # is character equiped?
    "element": "Water",
    "level": 1,
    "exp": 0,
    "multiplier": 1,  # multiplier each level (stats adjustment)
    "battle": False,  # is in battle?
    "stats": {
        "HP": 90,
        "max_HP": 90,
        "Mana": 35,
        "max_Mana": 35,
        "DEF": 16,
        "ATK": 21,
        "AGI": 98,  # how character arranged in battle
        "Crit_DMG": 1.5,
        "Crit_Rate": 0.05,
    },
    "amplification": {"water": 0, "fire": 0, "ice": 0, "leaf": 0},  # bonus damage
    "resistance": {"water": 0, "fire": 0, "ice": 0, "leaf": 0},  # damage resistance
    "story": {
        "short": "Josep is a young man from the village. He loves fishing and dreams of becoming a professional angler.",
        "long": "One time when Josep was fishing in the Ciliwung River, he accidentally got a magical item that emitted bright light. The object was round like a scrotum. Then Josep rubbed the seed and it released magical energy, suddenly Josep felt something strange from his fishing rod. At that moment Josep got power with the basic element of Water and was able to control his fishing line.",
    },
    "buff": [],  # buff in battle
    "debuff": [],  # debuff in battle
    "equipment": [],  # equpment
    "skills": [
        {
            "type": "attack",
            "name": "Rod Strike",
            "description": "Josep slings an enemy with his fishing rod, dealing {percentage}% ATK damage to a single target.",
            "ATK": 0.5,
            "level": 1,
        },
        {
            "type": "first",
            "name": "String and Hook",
            "action": "single",  # aoe, single, adjacent, self, ally, allies
            "status": "attack",
            "main": "ATK",
            "cost": 9,
            "cd": 1,
            "cd_left": 0,
            "description": "Josep throws a hook tied to a string at a single target, dealing {percentage}% ATK damage, and also binding the target until it is paralyzed for 1 turn. This effect unstackable.",
            "ATK": 0.3,
            "level": 1,
            "buff": {},
            "debuff": {
                "name": "Tied with string",
                "turn": 1,
                "turn_left": 0,
                "type": "paralyzed",
                "DOT": False,
                "DMG": 0,
                "base": "character",
            },
        },
        {
            "type": "second",
            "name": "Dad's Fishing Rod",
            "action": "self",
            "status": "buff",
            "main": "ATK",
            "cost": 12,
            "cd": 2,
            "cd_left": 0,
            "description": "Josep borrows his father's fishing rod and gets an ATK increase of {percentage}% ATK for 1 turns. This effect unstackable.",
            "ATK": 0,
            "level": 1,
            "buff": {
                "name": "Dad's Fishing Rod",
                "turn": 1,
                "turn_left": 0,
                "type": "status",
                "status": ["ATK"],
                "ATK": 0.5,
                "amplification": 0,  # calculated amplification from char/target
                "base": "character",
            },
            "debuff": {},
        },
        {
            "type": "third",
            "name": "Semester 5",
            "action": "single",
            "status": "attack",
            "main": "ATK",
            "cost": 10,
            "cd": 3,
            "cd_left": 0,
            "description": "Josep remembers his college days and imagines his signature fishing technique, attacking a single target with {percentage}% ATK damage.",
            "ATK": 1.1,
            "level": 1,
            "buff": {},
            "debuff": {},
        },
    ],
}
