from shiny import App, render, ui, reactive
import random

# --- Arcane Determinism ---
def roll_price(r: str) -> int:
    if r == "Common": return (random.randint(1, 6) + 1) * 10
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

# --- The Glass & Chrome Esthetic ---
# If running locally with a 'www' folder, use "Magic_Popup_Shop (1).mp4"
# For GitHub, ensure this is the direct 'raw' link.
VIDEO_URL = "https://raw.githubusercontent.com/YOUR_USER/YOUR_REPO/main/www/Magic_Popup_Shop%20(1).mp4"

glass_css = """
    /* The Living Background */
    #video-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        overflow: hidden;
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
        background-color: #000; /* Fallback */
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Glassmorphic Containers */
    .container-fluid {
        z-index: 1;
        padding: 3rem;
        min-height: 100vh;
    }

    .card, .sidebar {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        color: #ffffff;
    }

    /* Typography & Legibility */
    h1 {
        font-weight: 800;
        letter-spacing: -1px;
        text-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    
    label, .weave-instruction, .legible-metric {
        color: #ffffff !important;
        font-weight: 500;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.8);
    }

    .text-mystic {
        color: #00e5ff;
        font-weight: 900;
        text-shadow: 0 0 20px rgba(0, 229, 255, 0.6);
    }

    /* Sleek Silver Controls */
    .btn-glass {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.4);
        color: white;
        backdrop-filter: blur(4px);
        transition: 0.2s all ease-in-out;
        font-weight: bold;
        padding: 12px;
    }
    .btn-glass:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255,255,255,0.2);
        color: white;
    }
    
    /* Input adjustments */
    .form-control, .form-select {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }
"""

app_ui = ui.page_fluid(
    ui.tags.style(glass_css),
    
    # Atmospheric Layer
    ui.tags.div(
        ui.tags.video(
            ui.tags.source(src=VIDEO_URL, type="video/mp4"),
            id="bg-video",
            autoplay=True,
            loop=True,
            playsinline=True,
            muted=True
        ),
        id="video-container"
    ),

    ui.h1("🔮 MYSTIC MARKET", class_="text-center py-5 text-white"),
    
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select("rarity", "Artifact Rarity", 
                           choices=["Common", "Uncommon", "Rare", "Very Rare"]),
            ui.input_slider("discount", "Manual Discount (%)", 0, 100, 0),
            ui.input_numeric("persuasion_roll", "Persuasion Roll", value=10, min=1, max=40),
            ui.input_action_button("reroll", "Invoke New Valuation", class_="btn-glass w-100 mt-4"),
            ui.hr(style="opacity: 0.3;"),
            ui.span("Observe as the weave shifts with every adjustment.", class_="weave-instruction"),
        ),
        
        ui.card(
            ui.card_header("Arcane Receipt", style="background: transparent; border-bottom: 1px solid rgba(255,255,255,0.1);"),
            ui.output_ui("valuation_output"),
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
            ui.p(ui.strong("Base Value: "), f"{bp:,} gp", class_="legible-metric"),
            ui.p(ui.strong("Silver-Tongue Bonus: "), f"{p_disc}%", class_="legible-metric"),
            ui.p(ui.strong("Aggregate Reduction: "), f"{total_disc}%", class_="legible-metric"),
            ui.hr(style="border-top: 1px solid rgba(255, 255, 255, 0.2);"),
            ui.h2(f"{final_price:,} gp", class_="text-mystic"),
            ui.p("The transaction is inscribed in the stars.", style="font-style: italic; opacity: 0.7; font-size: 0.9rem;")
        )

app = App(app_ui, server)
