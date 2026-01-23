from shiny import App, render, ui, reactive
import random

# --- Logic Remains Unchanged ---
def roll_price(r: str) -> int:
    if r == "Common": return (random.randint(1, 6) + 1) * 10
    elif r == "Uncommon":
        base = random.randint(1, 6) * 100
        return int(base * (1 + random.choice([0, 0.10, 0.15])))
    elif r == "Rare":
        base = (random.randint(1, 10) + random.randint(1, 10)) * 1000
        return int(base * (1 + random.uniform(0.10, 0.15)))
    elif r == "Very Rare":
        base = (random.randint(1, 4) + 1) * 10000
        return int(base * (1 + random.uniform(0.10, 0.15)))
    return 0

def get_persuasion_discount(roll: int) -> int:
    if roll < 15: return 0
    if roll <= 17: return 5
    if roll <= 20: return 10
    if roll <= 23: return 15
    if roll <= 26: return 20
    if roll <= 29: return 25
    return 30

# --- The Visual & Auditory Weave ---
# REPLACE THIS URL with your actual GitHub Raw link
VIDEO_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/assets/Magic_Popup_Shop%20(1).mp4"

mystical_css = """
    /* Background Video Layering */
    #bg-video {
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -1;
        object-fit: cover;
        filter: brightness(0.4) contrast(1.1); /* Darken to ensure text pop */
    }

    body {
        background-color: #000814;
        color: #e0e1dd;
        font-family: 'Segoe UI', serif;
        overflow-x: hidden;
    }

    /* Translucent containers to let the video peek through */
    .container-fluid {
        position: relative;
        z-index: 1;
        background: transparent;
    }

    .card {
        background-color: rgba(13, 27, 42, 0.7) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(119, 141, 169, 0.4);
        border-radius: 12px;
    }

    .sidebar {
        background-color: rgba(27, 38, 59, 0.8) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid #778da9;
    }

    .legible-metric, .weave-instruction {
        color: #ffffff !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }

    .text-mystic {
        color: #00b4d8;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(0, 180, 216, 0.8);
    }

    .btn-primary {
        background-color: #778da9;
        border: none;
        color: #0d1b2a;
        font-weight: bold;
    }
"""

app_ui = ui.page_fluid(
    ui.tags.style(mystical_css),
    
    # The Background Video element
    ui.tags.video(
        ui.tags.source(src=VIDEO_URL, type="video/mp4"),
        id="bg-video",
        autoplay=True,
        loop=True,
        playsinline=True,
        # Note: 'muted' is omitted to allow sound, but browsers may block autoplay
    ),

    ui.panel_title(ui.h1("🔮 Mystic Market Valuator", class_="text-center py-4 text-white")),
    
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select("rarity", "Item Rarity", 
                           choices=["Common", "Uncommon", "Rare", "Very Rare"]),
            ui.input_slider("discount", "Manual Discount (%)", 0, 100, 0),
            ui.input_numeric("persuasion_roll", "Persuasion Check", value=10, min=1, max=40),
            ui.input_action_button("reroll", "Invoke New Price", class_="btn-primary w-100 mt-3"),
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
        
        return ui.div(
            ui.p(ui.span(f"Base Market Value: {bp:,} gp", class_="legible-metric")),
            ui.p(ui.span(f"Charisma Concession: {p_disc}%", class_="legible-metric")),
            ui.p(ui.span(f"Total Reduction: {total_disc}%", class_="legible-metric")),
            ui.hr(style="border-top: 1px solid rgba(119, 141, 169, 0.5);"),
            ui.h3(f"Final Tribute: {final_price:,} gp", class_="text-mystic"),
            ui.p("The merchant awaits your coin.", class_="fst-italic text-white-50")
        )

app = App(app_ui, server)
