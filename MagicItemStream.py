from pathlib import Path
from shiny import App, render, ui, reactive
import random

# --- Arcane Determinism Logic ---
def roll_price(r: str) -> int:
    if r == "Common":
        return (random.randint(1, 6) + 1) * 10
    elif r == "Uncommon":
        return int(random.randint(1, 6) * 100 * (1 + random.choice([0, 0.10, 0.15])))
    elif r == "Rare":
        return int((random.randint(1, 10) + random.randint(1, 10)) * 1000 * (1 + random.uniform(0.10, 0.15)))
    elif r == "Very Rare":
        return int((random.randint(1, 4) + 1) * 10000 * (1 + random.uniform(0.10, 0.15)))
    return 0

def get_persuasion_discount(roll: int) -> int:
    if roll < 15: return 0
    if roll <= 20: return 10
    if roll <= 26: return 20
    return 30

# --- Glassmorphic Style & Video Layout ---
glass_css = """
    #video-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        overflow: hidden;
        background: #000; /* Fallback if video fails */
    }
    #bg-video {
        width: 100%;
        height: 100%;
        object-fit: cover;
        filter: brightness(0.4) saturate(1.2);
    }

    body {
        margin: 0;
        padding: 0;
        color: #ffffff;
        background-color: #000;
    }

    /* Glassmorphism Effect */
    .glass-panel {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) saturate(180%);
        -webkit-backdrop-filter: blur(15px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.7);
        padding: 20px;
    }

    h1 {
        font-weight: 800;
        letter-spacing: 2px;
        text-shadow: 0 4px 10px rgba(0,0,0,0.8);
    }

    .legible-white {
        color: #ffffff !important;
        font-weight: 500;
        text-shadow: 1px 1px 3px rgba(0,0,0,1);
    }

    .text-mystic {
        color: #00e5ff;
        font-weight: 800;
        text-shadow: 0 0 15px rgba(0, 229, 255, 0.8);
    }

    .btn-glass {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 700;
    }
    .btn-glass:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
        color: white;
    }

    /* Input focus colors */
    .form-control:focus, .form-select:focus {
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border-color: #00e5ff;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.5);
    }
"""

app_ui = ui.page_fluid(
    ui.tags.style(glass_css),
    
    # Static Video Background
    ui.tags.div(
        ui.tags.video(
            ui.tags.source(src="Magic_Popup_Shop (1).mp4", type="video/mp4"),
            id="bg-video",
            autoplay=True,
            loop=True,
            playsinline=True,
            muted=True
        ),
        id="video-container"
    ),

    ui.h1("🔮 MYSTIC MARKET VALUATOR", class_="text-center py-5 text-white"),
    
    ui.layout_sidebar(
        ui.sidebar(
            ui.div(
                ui.input_select("rarity", "Item Rarity", 
                               choices=["Common", "Uncommon", "Rare", "Very Rare"]),
                ui.input_slider("discount", "Manual Discount (%)", 0, 100, 0),
                ui.input_numeric("persuasion_roll", "Persuasion Check", value=10, min=1, max=40),
                ui.input_action_button("reroll", "Invoke Price", class_="btn-glass w-100 mt-3"),
                class_="glass-panel"
            ),
            ui.hr(style="opacity: 0.2;"),
            ui.span("Adjust the weave to reveal the cost.", class_="legible-white ms-2")
        ),
        
        ui.div(
            ui.card(
                ui.card_header("Valuation Record", style="background:transparent; color: #fff;"),
                ui.output_ui("valuation_output"),
                class_="glass-panel"
            )
        ),
    ),
)

def server(input, output, session):
    base_price = reactive.Value(0)

    @reactive.Effect
    @reactive.event(input.rarity, input.reroll)
    def _():
        base_price.set(roll_price(input.rarity()))

    @output
    @render.ui
    def valuation_output():
        bp = base_price()
        p_disc = get_persuasion_discount(input.persuasion_roll())
        total_disc = input.discount() + p_disc
        final_price = int(bp * (1 - total_disc / 100))
        
        return ui.div(
            ui.p(ui.strong("Market Value: "), f"{bp:,} gp", class_="legible-white"),
            ui.p(ui.strong("Persuasion Bonus: "), f"{p_disc}%", class_="legible-white"),
            ui.p(ui.strong("Final Concession: "), f"{total_disc}%", class_="legible-white"),
            ui.hr(style="border-top: 1px solid rgba(255, 255, 255, 0.2);"),
            ui.h2(f"{final_price:,} gp", class_="text-mystic"),
            ui.p("The deal is struck in silver.", style="font-style: italic; opacity: 0.6;")
        )

# Identify the 'www' directory relative to the script location
www_path = Path(__file__).parent / "www"
app = App(app_ui, server, static_assets=str(www_path))
