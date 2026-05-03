from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config import config
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=config.APP_TITLE,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION,
    contact={
        "name": "Quirky_Dweed Team",
        "url": "https://github.com/Knight6azer/Grifffithhhhh",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)

tags_metadata = [
    {"name": "General", "description": "General endpoints for the platform."},
    {"name": "Characters", "description": "Endpoints related to Quirky_Dweed characters."},
    {"name": "Rankings", "description": "Endpoints for tier lists and community rankings."},
]

# Initialize Database Clients
supabase = None
from lib.characters import CharacterManager

if config.validate():
    try:
        from supabase import create_client
        
        supabase = create_client(config.SUPABASE_URL, config.SUPABASE_ANON_KEY)
        logger.info("Successfully connected to Supabase")
    except Exception as e:
        logger.error(f"Failed to initialize database clients: {e}")

# Always initialize CharacterManager, falling back to mock data if supabase is None
character_manager = CharacterManager(supabase)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/public", StaticFiles(directory="public"), name="public")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", tags=["General"])
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "title": "Quirky_Dweed"
    })

@app.get("/characters", tags=["Characters"])
async def characters_list(request: Request, q: str = None, role: str = None):
    characters = []
    if character_manager:
        if q or role:
            characters = character_manager.search_characters(q, role)
        else:
            characters = character_manager.get_all_characters()
    
    return templates.TemplateResponse("characters.html", {
        "request": request, 
        "characters": characters, 
        "title": "Character Hub",
        "search_query": q or "",
        "selected_role": role or ""
    })

@app.get("/characters/{character_id}", tags=["Characters"])
async def character_detail(request: Request, character_id: int):
    character = None
    if character_manager:
        character = character_manager.get_character_by_id(character_id)
    
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
        
    return templates.TemplateResponse("character_detail.html", {
        "request": request, 
        "character": character, 
        "title": f"{character.get('name', 'Character')} - Details"
    })

@app.get("/tier-lists", tags=["Rankings"])
async def tier_lists_view(request: Request):
    tier_lists = []
    if supabase:
        try:
            response = supabase.table("tier_lists").select("*").execute()
            tier_lists = response.data
        except Exception as e:
            logger.error(f"Error fetching tier lists: {e}")
    else:
        # Mock tier list
        tier_lists = [
            {
                "name": "Global Standings - Season 4",
                "characters": [
                    {"name": "Ahri", "tier": "S"},
                    {"name": "Yasuo", "tier": "S"},
                    {"name": "Cassiopeia", "tier": "A"},
                    {"name": "Thresh", "tier": "S"}
                ]
            }
        ]
            
    return templates.TemplateResponse("tier_lists.html", {
        "request": request, 
        "tier_lists": tier_lists, 
        "title": "Tier Lists"
    })

@app.get("/resources", tags=["General"])
async def resources_view(request: Request):
    return templates.TemplateResponse("resources.html", {
        "request": request, 
        "title": "Community Resources"
    })

@app.get("/about", tags=["General"])
async def about_view(request: Request):
    return templates.TemplateResponse("about.html", {
        "request": request,
        "title": "About Us"
    })

@app.get("/api/characters", tags=["Characters", "API"])
async def api_characters_list(q: str = None, role: str = None):
    if not character_manager:
        raise HTTPException(status_code=500, detail="Database not initialized")
    if q or role:
        return character_manager.search_characters(q, role)
    return character_manager.get_all_characters()

@app.get("/api/characters/{character_id}", tags=["Characters", "API"])
async def api_character_detail(character_id: int):
    if not character_manager:
        raise HTTPException(status_code=500, detail="Database not initialized")
    character = character_manager.get_character_by_id(character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
