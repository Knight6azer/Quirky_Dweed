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
                "name": "Ahri",
                "role": "Mage",
                "description": "The Spirit of Salvation. She guides souls to the afterlife with a gentle smile and a mesmerizing allure.",
                "lore": "The Spirit of Salvation, Ahri acts as a guide to the deceased as they travel to the spirit realm. She is a trickster who uses her charm and illusions to guide souls, but means them no harm. Many souls have been entranced by her, finding peace in her presence.",
                "image_url": "/public/placeholder.svg"
            },
            {
                "id": 2,
                "name": "Yasuo",
                "role": "Fighter",
                "description": "The Spirit of Heroism. He fights for what he believes in, even if it means going against the grain.",
                "lore": "The Spirit of Heroism, Yasuo is a legendary warrior who roams the spirit realm seeking redemption. His blade is as swift as the wind, and his resolve is unshakable. Though he is an outcast, he fights with a sense of honor.",
                "image_url": "/public/placeholder.svg"
            },
            {
                "id": 3,
                "name": "Cassiopeia",
                "role": "Mage",
                "description": "The Spirit of Temptation. She lures souls into her grasp with her enchanting beauty and deadly venom.",
                "lore": "The Spirit of Temptation, Cassiopeia is a beautiful but dangerous spirit. She weaves illusions and uses her intoxicating presence to trap unwary souls. Only those with true inner strength can resist her.",
                "image_url": "/public/placeholder.svg"
            },
            {
                "id": 4,
                "name": "Thresh",
                "role": "Support",
                "description": "The Spirit of Obsession. He collects souls with a cruel delight, keeping them trapped in his lantern.",
                "lore": "The Spirit of Obsession, Thresh is a malevolent entity who delights in tormenting souls. He collects them in his lantern, relishing in their despair. He is a dark presence in the spirit realm, feared by many.",
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