class Messages:
    charListPage: str = """\
### **🔹 Character Profile 🔹**  
📜 **ID:** `{char.id}`  
📝 **Name:** `{char.name}`  
🛡️ **Class:** `{char.class}`  
🌟 **Element:** `{char.element}`  
📈 **Level:** `{char.level}` | `{char.exp} XP`  

━━━━━━━━━━━━━━━━━━  
### **💠 Stats Overview**  
❤️ **HP:** `{stats.HP}/{stats.max_HP}`  
🔵 **Mana:** `{stats.Mana}/{stats.max_Mana}`  
🛡️ **Defense (DEF):** `{stats.DEF}`  
⚔️ **Attack (ATK):** `{stats.ATK}`  
⚡ **Agility (AGI):** `{stats.AGI}`  
💥 **Critical DMG:** `{cdm}%`  
🎯 **Critical Rate:** `{cdr}%`  
━━━━━━━━━━━━━━━━━━  

🔍 **Want to view more details?**  
Type `/character {char.id}`  
"""
    charDetailPage: str = """\
### **📜 Character Status 📜**  
**ID:** `{char.id}`  
**Name:** `{char.name}`  
**Class:** `{char.class}`  
**Element:** `{char.element}`  
**Level:** `{char.level}` | `{char.exp} XP`  

━━━━━━━━━━━━━━━━━━  
### **💠 Attributes & Stats**  
❤️ **HP:** `{stats.HP}/{stats.max_HP}`  
🔵 **Mana:** `{stats.Mana}/{stats.max_Mana}`  
⚔️ **ATK:** `{stats.ATK}`  
🛡️ **DEF:** `{stats.DEF}`  
⚡ **AGI:** `{stats.AGI}`  
💥 **Crit DMG:** `{cdm}%`  
🎯 **Crit Rate:** `{cdr}%`  
━━━━━━━━━━━━━━━━━━  
""".strip()

    amplificationResistancePage: str = """\
### **🌀 Elemental Affinities 🌀**  
**Character:** `{char.name}`  
━━━━━━━━━━━━━━━━━━  
🔺 **Amplifications:**  
🌊 Water: `{amp.water}%`  
🔥 Fire: `{amp.fire}%`  
❄️ Ice: `{amp.ice}%`  
🍃 Leaf: `{amp.leaf}%`  

🛡️ **Resistances:**  
🌊 Water: `{res.water}%`  
🔥 Fire: `{res.fire}%`  
❄️ Ice: `{res.ice}%`  
🍃 Leaf: `{res.leaf}%`  
━━━━━━━━━━━━━━━━━━  
""".strip()

    skillPage: str = """\
### **🔥 Skill Set 🔥**  
**Character:** `{char.name}`  
━━━━━━━━━━━━━━━━━━  
{skills}  
━━━━━━━━━━━━━━━━━━  
""".strip()

    storyPage: str = """\
### **📖 Character Story 📖**  
**Character:** `{char.name}`  
━━━━━━━━━━━━━━━━━━  
📜 **Short Story:**  
_{story.short}_  

📖 **Long Story:**  
_{story.long}_  
━━━━━━━━━━━━━━━━━━  
""".strip()