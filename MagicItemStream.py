from shiny import App, render, ui, reactive
import random

# --- Core Logic ---
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

# --- The Visual Anchor ---
# Note: Ensure this URL points directly to the raw mp4 file.
VIDEO_URL = "https://raw.githubusercontent.com/YOUR_USER/YOUR_REPO/main/assets/Magic_Popup_Shop%20(1).mp4"

mystical_css = """
    #video-bg-container {
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
        filter: brightness(0.3) contrast(1.2);
    }

    body {
        background-color: #000814;
        margin: 0;
        padding: 0;
    }

    .container-fluid {
        position: relative;
        z-index: 1;
        padding: 2rem;
    }

    .card {
        background-color: rgba(13, 27, 42, 0.8) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(224, 225, 221, 0.3);
        border-radius: 15px;
        color: #ffffff;
    }

    .sidebar {
        background-color: rgba(27, 38, 59, 0.9) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(119, 141, 169, 0.4);
        border-radius: 15px;
        color: #ffffff;
    }

    .legible-white, label, .weave-instruction {
        color: #ffffff !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 1);
    }

    .text-mystic {
        color: #00d4ff;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(0, 212, 255, 0.8);
    }

    .btn-silver {
        background-color: #e0e1dd;
        color: #0d1b2a;
        font-weight: bold;
        border: none;
        transition: 0.3s ease-in-out;
    }
    .btn-silver:hover {
        background-color: #ffffff;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.4);
    }
"""

app_ui = ui.page_fluid(
    ui.tags.style(mystical_css),
    
    # Video Foundation
    ui.tags.div(
        ui.tags.video(
            ui.tags.source(src=VIDEO_URL, type="video/mp4"),
            id="bg-video",
            autoplay=True,
            loop=True,
            playsinline=True,
            muted=True # Essential for most browsers to allow autoplay
        ),
        id="video-bg-container"
    ),

    ui.h1("🔮 Mystic Market Valuator", class_="text-center py-4 text-white"),
    
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select("rarity", "Item Rarity", 
                           choices=["Common", "Uncommon", "Rare", "Very Rare"]),
            ui.input_slider("discount", "Manual Discount (%)", 0, 100, 0),
            ui.input_numeric("persuasion_roll", "Persuasion Check", value=10, min=1, max=40),
            ui.input_action_button("reroll", "Invoke New Price", class_="btn-silver w-100 mt-3"),
            ui.hr(),
            ui.span("Adjust the weave of fate to see the price shift.", class_="weave-instruction"),
        ),
        
        ui.card(
            ui.card_header("Arcane Valuation"),
            ui.output_ui("results_display"),
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
    def results_display():
        bp = base_price()
        p_disc = get_persuasion_discount(input.persuasion_roll())
        total_disc = input.discount() + p_disc
        final_price = int(bp * (1 - total_disc / 100))
        
        # Using positional arguments for content to avoid list-attribute errors
        return ui.div(
            ui.p(ui.strong("Base Market Value: "), f"{bp:,} gp", class_="legible-white"),
            ui.p(ui.strong("Charisma Concession: "), f"{p_disc}%", class_="legible-white"),
            ui.p(ui.strong("Total Reduction: "), f"{total_disc}%", class_="legible-white"),
            ui.hr(style="border-top: 1px solid rgba(255, 255, 255, 0.3);"),
            ui.h3(f"Final Tribute: {final_price:,} gp", class_="text-mystic"),
        )

app = App(app_ui, server)
