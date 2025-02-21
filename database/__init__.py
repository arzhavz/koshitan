import aiosqlite
import json
import time
import random

from typing import Union, Dict

class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def create_table(self) -> None:
        """
        Create the users table with the necessary columns if it doesn't exist.
        """
        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                level INTEGER NOT NULL,
                exp INTEGER NOT NULL,
                money INTEGER NOT NULL,
                crate JSON,
                item JSON,
                energy JSON,
                orb JSON,
                soul JSON,
                character JSON,
                character_showdown JSON,
                character_equipment JSON,
                battle_session JSON                   
            )
            """)
        await self.connection.commit()

    async def register_user(self, user_id: int, level: int = 1, exp: int = 0, money: int = 0) -> None:
        """
        Register a new user if they do not already exist and ensure all columns are present.
        """
        default_data = {
            "crate": {"common": 0, "uncommon": 0, "rare": 0, "epic": 0, "legendary": 0, "treasure": 0},
            "energy": {"energy": 100, "max": 100, "regen": 5, "regen_cd": 60, "regen_last": 0},
            "item": {"wheat": 0, "wood": 0, "stone": 0, "steel": 0, "trash": 0},
            "orb": {"fire": 0, "water": 0, "ice": 0, "leaf": 0},
            "soul": {"warrior": 0, "vigilancer": 0, "priest": 0},
            "character": [],
            "character_showdown": [],
            "character_equipment": [],
        }

        await self.create_table()

        async with self.connection.execute(
            "SELECT * FROM users WHERE user_id=?", (user_id,)
        ) as cursor:
            existing_user = await cursor.fetchone()
            if not existing_user:
                await self.connection.execute(
                    """INSERT INTO users (user_id, level, exp, money, crate, item, energy, orb, soul, character, character_showdown, character_equipment, battle_session) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        user_id, level, exp, money,
                        json.dumps(default_data["crate"]),
                        json.dumps(default_data["item"]),
                        json.dumps(default_data["energy"]),
                        json.dumps(default_data["orb"]),
                        json.dumps(default_data["soul"]),
                        json.dumps(default_data["character"]),
                        json.dumps(default_data["character_showdown"]),
                        json.dumps(default_data["character_equipment"]),
                        json.dumps({})
                    ),
                )
                await self.connection.commit()
            else:
                columns = [desc[0] for desc in cursor.description]
                for key, value in default_data.items():
                    if key not in columns:
                        await self.connection.execute(
                            f"ALTER TABLE users ADD COLUMN {key} JSON",
                            (json.dumps(value),)
                        )
                await self.connection.commit()

    async def connect_user(self, user_id: int) -> Union[Dict, None]:
        """
        Fetch user data and return as a dictionary.
        """
        async with self.connection.execute(
            "SELECT id, user_id, level, exp, money, crate, item, energy, orb, soul, character, character_showdown, character_equipment, battle_session FROM users WHERE user_id=?",
            (user_id,)
        ) as cursor:
            user_data = await cursor.fetchone()
            if user_data:
                return {
                    "id": user_data[0],
                    "user_id": user_data[1],
                    "level": user_data[2],
                    "exp": user_data[3],
                    "money": user_data[4],
                    "crate": user_data[5],
                    "item": user_data[6],
                    "energy": user_data[7],
                    "orb": user_data[8],
                    "soul": user_data[9],
                    "character": user_data[10],
                    "character_showdown": user_data[11],
                    "character_equipment": user_data[12],
                    "battle_session": user_data[13]
                }
            return None

    async def update_user(self, user_id: int, data: Dict) -> None:
        """
        Update user data dynamically based on provided dictionary.
        """
        set_clause = ", ".join(f"{key}=?" for key in data.keys())
        values = list(data.values()) + [user_id]
        query = f"UPDATE users SET {set_clause} WHERE user_id=?"
        
        await self.connection.execute(query, values)
        await self.connection.commit()

    async def leveling(self, user_id: int, exp_gain: int) -> None:
        """
        Automatically trigger level-up when user EXP reaches or exceeds 750.
        """
        user = await self.connect_user(user_id)
        if not user:
            return
        energy = json.loads(user["energy"])
        crate = json.loads(user["crate"])
        crate_e = {
            "common": "<:commoncrate:1335016425827471491>",
            "uncommon": "<:uncommoncrate:1335016439085666408>",
            "rare": "<:rarecrate:1335016450381054155>",
            "epic": "<:epiccrate:1335016472044634242>",
            "legendary": "<:legendarycrate:1335016485134798888>"
        }
        reward = random.choice(["common", "epic", "legendary", "rare", "uncommon"])

        user["exp"] += exp_gain
        
        if user["exp"] >= 750:
            user["exp"] -= 750
            user["level"] += 1
            energy["max"] += 5
            energy["energy"] = energy["max"]
            user["money"] += 4500 + (5000 * 0.1 * user["level"])
            crate[reward] += 1

            user["crate"] = json.dumps(crate)
            user["energy"] = json.dumps(energy)
            await self.update_user(user_id, user)
            return {
                "status": True,
                "energy": energy["max"],
                "money": 4500 + int(5000 * 0.1 * user["level"]),
                "crate": crate_e[reward]
            }
        
        await self.update_user(user_id, user)

        return {
            "status": False
        }

    async def regen_energy(self, user_id: int) -> None:
        """
        Automatically regenerate energy.
        """
        user = await self.connect_user(user_id)

        if not user:
            return
        energy = json.loads(user["energy"])

        if energy["energy"] < energy["max"] and int(time.time()) > energy["regen_last"] + energy["regen_cd"]:
            elapsed_time = int(time.time()) - energy["regen_last"]
            regen_amount = energy["regen"] * (elapsed_time // energy["regen_cd"])

            energy["energy"] = min(energy["energy"] + regen_amount, energy["max"])
            energy["regen_last"] += (elapsed_time // energy["regen_cd"]) * energy["regen_cd"]

        user["energy"] = json.dumps(energy)
        await self.update_user(user_id, user)

    async def leaderboard(self) -> Dict:
        async with self.connection.execute(
            "SELECT user_id, money FROM users ORDER BY money DESC LIMIT 10"
        ) as cursor:
            top_money = await cursor.fetchall()

        async with self.connection.execute(
            "SELECT user_id, level FROM users ORDER BY level DESC LIMIT 10"
        ) as cursor:
            top_level = await cursor.fetchall()
        
        return top_money, top_level