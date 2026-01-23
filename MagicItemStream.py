from shiny import App, render, ui, reactive
import random

def roll_price(r: str) -> int:
    if r == "Common":
        return (random.randint(1, 6) + 1) * 10
    elif r == "Uncommon":
        base = random.randint(1, 6) * 100
        markup = random.choice([0, 0.10, 0.15])
        return int(base * (1 + markup))
    elif r == "Rare":
        base = (random.randint(1, 10) + random.randint(1, 10)) * 1000
        markup = random.uniform(0.10, 0.15)
        return int(base * (1 + markup))
    elif r == "Very Rare":
        base = (random.randint(1, 4) + 1) * 10000
        markup = random.uniform(0.10, 0.15)
        return int(base * (1 + markup))
    return 0

def get_persuasion_discount(roll: int) -> int:
    if roll < 15: return 0
    if roll <= 17: return 5
    if roll <= 20: return 10
    if roll <= 23: return 15
    if roll <= 26: return 20
    if roll <= 29: return 25
    return 30

# --- Refined Mystical Styles ---
mystical_css = """
    body {
        background: radial-gradient(circle at center, #0d1b2a 0%, #000814 100%);
        color: #e0e1dd;
        font-family: 'Segoe UI', serif;
    }
    .card {
        background-color: rgba(27, 38, 59, 0.8);
        border: 1px solid #778da9;
        box-shadow: 0 0 20px rgba(0, 180, 216, 0.1);
        border-radius: 12px;
    }
    .card-header {
        background-color: #415a77 !important;
        color: #ffffff !important;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    .sidebar {
        background-color: #1b263b !important;
        border-right: 2px solid #778da9;
    }
    .btn-primary {
        background-color: #778da9;
        border: none;
        color: #0d1b2a;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .btn-primary:hover {
        background-color: #ffffff;
        box-shadow: 0 0 15px #ffffff;
        color: #0d1b2a;
    }
    /* Forces white color for requested labels and values */
    .legible-metric {
        color: #ffffff !important;
        font-size: 1.1rem;
    }
    .weave-instruction {
        color: #ffffff !important;
        font-style: italic;
        margin-top: 20px;
        display: block;
    }
    .shiny-input-container label {
        color: #778da9;
    }
    .text-mystic {
        color: #00b4d8;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 180, 216, 0.6);
    }
"""

app_ui = ui.page_fluid(
    ui.tags.style(mystical_css),
    ui.panel_title(ui.h1("🔮 Mystic Market Valuator", class_="text-center py-4")),
    
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select(
                "rarity", 
                "Item Rarity", 
                choices=["Common", "Uncommon", "Rare", "Very Rare"]
            ),
            ui.input_slider("discount", "Manual Discount (%)", 0, 100, 0),
            
            ui.tooltip(
                ui.input_numeric("persuasion_roll", "Persuasion Check", value=10, min=1, max=40),
                "The silver-tongued may find lower prices.",
                id="persuasion_tip"
            ),
            
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
            ui.hr(style="border-top: 1px solid #778da9;"),
            ui.h3(f"Final Tribute: {final_price:,} gp", class_="text-mystic"),
            ui.div(
                ui.p(
                    "The merchant awaits your coin." if total_disc < 30 
                    else "A legendary bargain has been struck.",
                    class_="fst-italic",
                    style="color: #778da9;"
                )
            )
        )

app = App(app_ui, server)
