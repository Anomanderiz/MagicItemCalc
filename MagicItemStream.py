from shiny import App, render, ui, reactive
import random

# --- Core Logic (Extracted for clarity) ---
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

# --- UI Definition ---
app_ui = ui.page_fluid(
    ui.panel_title("🧙‍♂️ Mystic Market Valuator"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select(
                "rarity", 
                "Item Rarity", 
                choices=["Common", "Uncommon", "Rare", "Very Rare"]
            ),
            ui.input_slider("discount", "Manual Discount (%)", 0, 100, 0),
            
            ui.tooltip(
                ui.input_numeric("persuasion_roll", "Persuasion Check (d20 + Mods)", value=10, min=1, max=40),
                "Higher rolls unlock steeper mercantile concessions.",
                id="persuasion_tip"
            ),
            
            ui.input_action_button("reroll", "🎲 Re-roll Base Price", class_="btn-primary w-100"),
            
            ui.hr(),
            ui.markdown(
                "**Guidance:** Adjust the sliders and rolls to see the price update *instantly* without a full page refresh."
            ),
        ),
        
        ui.card(
            ui.card_header("Valuation Summary"),
            ui.output_ui("results_display"),
        ),
    ),
)

# --- Server Logic ---
def server(input, output, session):
    # This reactive value stores our base price so it persists across UI changes 
    # until the user explicitly hits 'Reroll' or changes rarity.
    base_price = reactive.Value(0)

    # Initialize or update price when rarity changes or button is clicked
    @reactive.Effect
    @reactive.event(input.rarity, input.reroll)
    def _():
        base_price.set(roll_price(input.rarity()))

    @output
    @render.ui
    def results_display():
        # Reactive dependencies are tracked automatically
        bp = base_price()
        p_disc = get_persuasion_discount(input.persuasion_roll())
        total_disc = input.discount() + p_disc
        final_price = int(bp * (1 - total_disc / 100))
        
        # Determine a color for the message based on discount
        msg_color = "text-success" if total_disc > 20 else "text-muted"
        
        return ui.div(
            ui.p(ui.strong("Base Price: "), f"{bp:,} gp"),
            ui.p(ui.strong("Persuasion Discount: "), f"{p_disc}%"),
            ui.p(ui.strong("Total Discount: "), f"{total_disc}%"),
            ui.hr(),
            ui.h3(f"Final Price: {final_price:,} gp", class_="text-primary"),
            ui.p(
                "The merchant looks pleased with the deal." if total_disc < 40 
                else "You've practically robbed them blind.",
                class_=f"fst-italic {msg_color}"
            )
        )

app = App(app_ui, server)
