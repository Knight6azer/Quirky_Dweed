# Character data and utilities for Quirky_Dweed

from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class CharacterManager:
    def __init__(self, supabase_client=None):
        self.supabase = supabase_client
        self.mock_characters = [
            {
                "id": 1,
                "name": "Sung Jinwoo",
                "role": "Hunter",
                "origin": "Manhwa",
                "series": "Solo Leveling",
                "power_level": "SSS",
                "archetype": "Protagonist",
                "description": "The Shadow Monarch. Once the weakest E-Rank Hunter, Jinwoo ascended to become the most powerful being in existence through the System.",
                "lore": "Sung Jinwoo began as humanity's weakest hunter, mocked and pitied by all. After a near-death experience in a double dungeon, he was chosen by the System and granted the ability to level up without limits. Through relentless grinding, sacrifice, and sheer willpower, he rose from E-Rank to become the Shadow Monarch — commanding an army of the dead and standing as humanity's last line of defense against the Monarchs.",
                "image_url": "/public/placeholder.svg"
            },
            {
                "id": 2,
                "name": "Gojo Satoru",
                "role": "Sorcerer",
                "origin": "Manga",
                "series": "Jujutsu Kaisen",
                "power_level": "Special Grade",
                "archetype": "Mentor",
                "description": "The Strongest Sorcerer. With his Limitless cursed technique and the Six Eyes, Gojo stands as an insurmountable wall between cursed spirits and humanity.",
                "lore": "Born with both the Limitless technique and the Six Eyes — a combination not seen in four hundred years — Gojo Satoru disrupted the balance of the jujutsu world simply by existing. As a teacher at Tokyo Jujutsu High, he mentors the next generation while simultaneously being the single greatest deterrent against curse-kind. His Infinity makes him virtually untouchable, and his Domain Expansion, Unlimited Void, overwhelms any opponent with infinite information.",
                "image_url": "/public/placeholder.svg"
            },
            {
                "id": 3,
                "name": "Guts",
                "role": "Swordsman",
                "origin": "Manga",
                "series": "Berserk",
                "power_level": "Superhuman",
                "archetype": "Anti-Hero",
                "description": "The Black Swordsman. A lone warrior branded by fate, Guts wages an endless war against demonic apostles with nothing but his massive Dragonslayer sword and iron will.",
                "lore": "Born from the corpse of his hanged mother, Guts has known nothing but battle since childhood. After being betrayed during the Eclipse by his closest friend Griffith, he was branded with the Mark of Sacrifice, condemning him to be hunted by demons for eternity. Armed with the Dragonslayer — a sword so massive it was said no human could wield it — and the Berserker Armor, Guts carves a bloody path through the darkness, driven by rage, love, and an unyielding refusal to submit to fate.",
                "image_url": "/public/placeholder.svg"
            },
            {
                "id": 4,
                "name": "Frieren",
                "role": "Mage",
                "origin": "Manga",
                "series": "Frieren: Beyond Journey's End",
                "power_level": "Legendary",
                "archetype": "Protagonist",
                "description": "The Slayer of Demons. An elven mage who outlives her companions and embarks on a journey to understand the human connections she once took for granted.",
                "lore": "Frieren is an elven mage who was part of the Hero's party that defeated the Demon King. While the quest took ten years, for an elf who has lived over a thousand, it felt like a fleeting moment. After the hero Himmel's death, Frieren realizes she barely knew her companions and sets out on a new journey — retracing their steps to understand the meaning of the bonds she formed, and to find the magic to speak with the dead one last time.",
                "image_url": "/public/placeholder.svg"
            },
            {
                "id": 5,
                "name": "Levi Ackerman",
                "role": "Soldier",
                "origin": "Manga",
                "series": "Attack on Titan",
                "power_level": "Peak Human",
                "archetype": "Anti-Hero",
                "description": "Humanity's Strongest Soldier. A cold, efficient killing machine whose unmatched combat skills make him worth an entire brigade.",
                "lore": "Raised in the Underground City beneath the walls, Levi survived a brutal upbringing that forged him into the deadliest soldier humanity has ever produced. As captain of the Survey Corps' Special Operations Squad, he has slain more Titans than any other soldier in history. Despite his small stature and stoic demeanor, Levi carries the weight of every comrade he's lost, channeling his grief into a relentless pursuit of freedom for humanity.",
                "image_url": "/public/placeholder.svg"
            },
            {
                "id": 6,
                "name": "Cha Hae-In",
                "role": "Hunter",
                "origin": "Manhwa",
                "series": "Solo Leveling",
                "power_level": "S-Rank",
                "archetype": "Protagonist",
                "description": "South Korea's strongest female hunter and vice-guild master. Her swordsmanship is as elegant as it is deadly.",
                "lore": "As an S-Rank Hunter and vice-guild master of the Hunters Guild, Cha Hae-In possesses a unique ability to smell the mana of other hunters — most of which she finds repulsive. When she first encountered Sung Jinwoo, she was stunned to find his mana had a pleasant scent, drawing her into his orbit. A master swordswoman who holds her own against the strongest opponents, Hae-In proves that power and grace are not mutually exclusive.",
                "image_url": "/public/placeholder.svg"
            }
        ]

    def get_all_characters(self) -> List[Dict[str, Any]]:
        """Fetch all characters from the database."""
        if not self.supabase:
            return self.mock_characters
        try:
            response = self.supabase.table("characters").select("*").execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching characters: {e}")
            return []

    def get_character_by_id(self, character_id: int) -> Dict[str, Any]:
        """Fetch a specific character by ID."""
        if not self.supabase:
            return next((c for c in self.mock_characters if c["id"] == character_id), {})
        try:
            response = self.supabase.table("characters").select("*").eq("id", character_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error fetching character {character_id}: {e}")
            return {}

    def search_characters(self, query: Optional[str] = None, role: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search characters by name (case-insensitive) and optionally filter by role."""
        if not self.supabase:
            q = query.lower() if query else ""
            results = self.mock_characters
            if q:
                results = [c for c in results if q in c["name"].lower()]
            if role:
                results = [c for c in results if c.get("role", "").lower() == role.lower()]
            return results
        try:
            # Note: Supabase 'ilike' for case-insensitive search
            db_query = self.supabase.table("characters").select("*")
            if query:
                db_query = db_query.ilike("name", f"%{query}%")
            if role:
                db_query = db_query.ilike("role", role)
            response = db_query.execute()
            return response.data
        except Exception as e:
            logger.error(f"Error searching characters with query '{query}' and role '{role}': {e}")
            return []

    def create_character(self, character_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new character."""
        if not self.supabase:
            logger.warning("Cannot create character without Supabase.")
            return {}
        try:
            response = self.supabase.table("characters").insert(character_data).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error creating character: {e}")
            return {}