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

# --- Enhanced Glassmorphic Style ---
glass_css = """
    #video-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        overflow: hidden;
        background: #000;
    }
    #bg-video {
        width: 100%;
        height: 100%;
        object-fit: cover;
        filter: brightness(0.35) saturate(1.3) contrast(1.1);
    }

    body {
        margin: 0;
        padding: 0;
        color: #ffffff;
        background-color: #000;
        font-family: 'Garamond', serif;
    }

    .glass-panel {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(20px) saturate(200%);
        -webkit-backdrop-filter: blur(20px) saturate(200%);
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        padding: 25px;
    }

    h1 {
        font-weight: 800;
        letter-spacing: 4px;
        text-transform: uppercase;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.4);
        font-family: 'Palatino', serif;
    }

    /* Enforced White Labels for Inputs */
    .control-label, label, .legible-white {
        color: #ffffff !important;
        font-weight: 500;
        text-shadow: 2px 2px 4px rgba(0,0,0,1);
    }

    /* Large Header for the Receipt Card */
    .receipt-title {
        font-size: 1.8rem !important;
        font-weight: bold;
        letter-spacing: 1px;
    }

    /* Larger Instructional Text */
    .weave-instruction {
        color: #ffffff !important;
        font-size: 1.4rem;
        font-style: italic;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 1);
        display: block;
        margin-top: 20px;
    }

    .text-mystic {
        color: #00f2ff;
        font-weight: 800;
        text-shadow: 0 0 25px rgba(0, 242, 255, 0.9);
    }

    .btn-glass {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.4);
        color: white;
        transition: 0.3s ease-in-out;
        font-weight: 700;
        text-transform: uppercase;
    }
    .btn-glass:hover {
        background: rgba(255, 255, 255, 0.35);
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(255, 255, 255, 0.2);
        color: white;
    }

    .form-control, .form-select {
        background: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
    }
"""

app_ui = ui.page_fluid(
    ui.tags.style(glass_css),
    
    # Static Video Background Layer
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

    ui.h1("Madame Morrible's Magic Mores", class_="text-center py-5 text-white"),
    
    ui.layout_sidebar(
        ui.sidebar(
            ui.div(
                ui.input_select("rarity", "Artifact Rarity", 
                               choices=["Common", "Uncommon", "Rare", "Very Rare"]),
                ui.input_slider("discount", "Manual Discount (%)", 0, 100, 0),
                ui.input_numeric("persuasion_roll", "Persuasion Roll", value=10, min=1, max=40),
                ui.input_action_button("reroll", "Invoke Valuation", class_="btn-glass w-100 mt-3"),
                class_="glass-panel"
            ),
            ui.hr(style="opacity: 0.2;"),
            ui.span("Adjust the weave to reveal the cost.", class_="weave-instruction ms-2")
        ),
        
        ui.div(
            ui.card(
                ui.card_header("Arcane Receipt", class_="receipt-title", style="background:transparent; color: #fff;"),
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
            ui.p(ui.strong("Influence Bonus: "), f"{p_disc}%", class_="legible-white"),
            ui.p(ui.strong("Aggregate Reduction: "), f"{total_disc}%", class_="legible-white"),
            ui.hr(style="border-top: 1px solid rgba(255, 255, 255, 0.3);"),
            ui.h2(f"{final_price:,} gp", class_="text-mystic"),
            ui.p("Inscribed in the ledger of destiny.", style="font-style: italic; opacity: 0.7;")
        )

# Identifying the 'www' directory for static assets
www_path = Path(__file__).parent / "www"
app = App(app_ui, server, static_assets=str(www_path))
