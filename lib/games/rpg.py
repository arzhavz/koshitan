import random
import json
import math

from typing import Any
from rich.pretty import pprint
        

class RPGame:
    def __init__(self, user: dict) -> None:
        self.user = user  
        self.crate = json.loads(user["crate"])
        self.item = json.loads(user["item"])

    def open_crate(self, rarity: str) -> None:
        """
        Membuka crate berdasarkan rarity dan menambahkan item ke inventaris user.

        Aturan:
            - common: mendapatkan hingga 3 jenis item dan total item 4 hingga 10 item.
            - uncommon: mendapatkan hingga 4 jenis item dan total item 15 hingga 25 item.
            - rare: mendapatkan hingga 5 jenis item dan total item 50 hingga 75 item.
            - epic: mendapatkan semua item dan total item 150 hingga 200 item.
            - legendary: mendapatkan semua item dan total item 500 hingga 1000 item.
        """
        items = ["wheat", "wood", "stone", "steel", "trash"]

        rules = {
            "treasure":  {"max_types": 0, "min_total": 0, "max_total": 0, "money": [(500, 0.55), (2500, 0.25), (5000, 0.19), (250000, 0.01)]},
            "common":    {"max_types": 3, "min_total": 25, "max_total": 50, "money": 1000},
            "uncommon":  {"max_types": 4, "min_total": 100, "max_total": 200, "money": 2500},
            "rare":      {"max_types": 5, "min_total": 250, "max_total": 500, "money": 7500},
            "epic":      {"max_types": len(items), "min_total": 550, "max_total": 1000, "guaranteed_all": True, "money": 20000},
            "legendary": {"max_types": len(items), "min_total": 1050, "max_total": 2500, "guaranteed_all": True, "money": 150000}
        }

        if rarity not in self.user["crate"] or self.crate[rarity] <= 0:
            return f"⚠️ You don't have enough crate(s) **{rarity}** to open!"
        
        rule = rules[rarity]
        if rarity == "treasure":
            moneys = Utils.choice(rule.get("money"))
            self.user["money"] += moneys
            return moneys, self.crate
        moneys = random.randint(round(rule["money"] * 0.2), rule["money"])
        self.crate[rarity] -= 1
        self.user["money"] += moneys
        min_total = rule["min_total"]
        max_total = rule["max_total"]

        if rule.get("guaranteed_all", False):
            chosen_items = items  
        else:
            max_types = rule["max_types"]
            available_types = min(max_types, len(items))
            num_types = random.randint(1, available_types)
            chosen_items = random.sample(items, num_types)  

        total_quantity = random.randint(min_total, max_total)
        
        distribution = {item: 1 for item in chosen_items}
        remaining = total_quantity - len(chosen_items)

        while remaining > 0:
            item = random.choice(chosen_items)
            distribution[item] += 1
            remaining -= 1

        for item, qty in distribution.items():
            self.item[item] += qty

        return distribution, moneys, (self.crate, self.item)
    
    class Battle:
        def __init__(self, party: list[dict], monsters: list[dict]) -> None:
            self.party = party
            self.monsters = monsters

        def damage(self, DMG: int, attacker, defender) -> int:
            base_damage = DMG

            crit_multiplier = (
                attacker.Crit_DMG + 1 if random.random() < attacker.Crit_Rate else 1
            )

            try:
                def_factor = (defender.DEF * 1.1) / math.log(
                attacker.level * defender.level / defender.DEF, math.pi
                )
                def_adjust = math.cos(
                    math.fsum([math.sqrt(defender.DEF), defender.level, attacker.level])
                    / attacker.level
                    + 10
                )
                log_factor = math.log(
                    defender.DEF, math.factorial(defender.level + attacker.level)
                )
                part1 = abs(
                    (1 - abs(1 - (math.radians(def_factor / def_adjust) % log_factor)))
                )
                part2 = math.cos(
                    (
                        math.tan((defender.DEF * 1.1) / math.e)
                        * math.fsum(
                            [
                                math.sin(defender.DEF),
                                defender.DEF // defender.level,
                                defender.DEF // attacker.level,
                                math.pi,
                            ]
                        )
                    )
                    // (math.sqrt(defender.level + attacker.level) * 25)
                ) % math.asinh(defender.DEF)
                part3 = (defender.DEF * 1.1) / (
                    defender.DEF * math.sqrt(defender.DEF * defender.level) + 100
                )
                def_multiplier = abs(part1 + part2 - part3 + 1) % 1
            except (ValueError, ZeroDivisionError):
                def_multiplier = 1

            damage = base_damage * crit_multiplier * def_multiplier
            return round(damage)
        

class Utils:
    @staticmethod
    def choice(items):
        total_weight = sum(weight for _, weight in items)
        rand_val = random.uniform(0, total_weight)
        cumulative_weight = 0
        for item, weight in items:
            cumulative_weight += weight
            if rand_val <= cumulative_weight:
                return item
            
    @staticmethod
    def find(value, data, key="id"):
        return next((item for item in data if item.get(key) == value), None)
    
    @staticmethod
    def overwrite(value: dict, data: list, id: Any) -> list:
        for item in data:
            if item.get("id") == id:
                item.update(value)
                break
        return data

class Estate:
    """UNUSED"""
    def __init__(self, user: dict) -> None:
        self.user = user

    def initial(self):
        house = {
            "price": 5000,
            "item_base": 100,
            "item_cost": {
                "food": 1.25,
                "wood": 1.25,
                "stone": 1.00,
                "steel": 1.00,
                "trash": 0.50
            },
            "money_coef": 100, #per cycle
            "money_cycle": 30, #regen cycle (s)
            "money_max": 7500, #max capacity
            "level": 1,
            "last_claim": 0,
            "name": "",
            "id": "",
            "worth": 7500 
        }
        pass 
        
