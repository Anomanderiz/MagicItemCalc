import math
import os
import random
from pathlib import Path

import bcrypt
import requests
from shiny import App, reactive, render, ui

# --- Discord Webhook Configuration ---
# Replace with the unique thread-link provided by your Discord server settings.
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
APP_PASSWORD_HASH = os.environ.get("APP_PASSWORD_HASH")


def verify_password(password: str) -> bool:
    """Verify a password without ever sending the configured hash to the client."""
    if not password or not APP_PASSWORD_HASH:
        return False

    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            APP_PASSWORD_HASH.encode("utf-8"),
        )
    except (TypeError, ValueError):
        # Fail closed when APP_PASSWORD_HASH is not a valid bcrypt hash.
        return False


def send_to_discord(char_name, artifact_name, rarity, base, final, total_discount, consumable_price=None):
    """Dispatches a formatted missive to the Madame's Discord ledger."""
    if not DISCORD_WEBHOOK_URL or DISCORD_WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_URL":
        return False

    fields = [
        {"name": "Artifact", "value": f"*{artifact_name}*", "inline": False},
        {"name": "Rarity", "value": rarity, "inline": True},
        {"name": "Market Value", "value": format_price(base), "inline": True},
        {"name": "Total Concession", "value": f"{total_discount}%", "inline": True},
        {"name": "Final Tribute", "value": f"**{format_price(final)}**", "inline": False},
    ]
    if consumable_price is not None:
        fields.append({"name": "Consumable Price", "value": format_price(consumable_price), "inline": False})

    payload = {
        "username": "Madame Morrible",
        "embeds": [{
            "title": "Arcane Transaction Chronicled",
            "color": 0x00f2ff,
            "description": f"The weave has finalized a deal for **{char_name}**.",
            "fields": fields,
            "footer": {"text": "Madame Morrible's Magic Mores | Inscribed in the eternal ledger."}
        }]
    }
    
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        return response.status_code == 204
    except Exception:
        return False

# --- Mercantile Logic ---
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

def get_persuasion_discount(roll: int | None) -> int:
    if roll is None:
        return 0
    if roll < 15: return 0
    if roll <= 20: return 10
    if roll <= 26: return 20
    return 30

NON_CONSUMABLE_RARE_PRICE_FLOOR = 600

def format_price(price: float) -> str:
    if float(price).is_integer():
        return f"{int(price):,} gp"
    return f"{price:,.1f} gp"

def calculate_prices(base: int, rarity: str, total_discount_pct: int, is_consumable: bool) -> tuple[int, int, float | None]:
    if base <= 0:
        return 0, 0, 0 if is_consumable else None

    discount_multiplier = 1 - total_discount_pct / 100
    effective_base = base

    if rarity != "Common" and not is_consumable:
        minimum_base = math.ceil(NON_CONSUMABLE_RARE_PRICE_FLOOR / discount_multiplier)
        effective_base = max(base, minimum_base)

    final_cost = int(effective_base * discount_multiplier)
    consumable_price = final_cost / 2 if is_consumable else None
    return effective_base, final_cost, consumable_price

# --- Glassmorphic Visuals ---
glass_css = """
    html, body {
        height: 100%;
    }
    #video-container {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1; overflow: hidden; background: #000;
    }
    @supports (height: 100svh) {
        #video-container { height: 100svh; }
    }
    #bg-video {
        width: 100%; height: 100%; object-fit: cover;
        filter: brightness(0.35) saturate(1.3) contrast(1.1);
    }
    body {
        margin: 0; padding: 0; color: #ffffff;
        background-color: #000; font-family: 'Garamond', serif;
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
        font-weight: 800; letter-spacing: 4px; text-transform: uppercase;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.4);
        font-family: 'Palatino', serif;
    }
    .hero-title {
        font-size: 2.8rem;
        padding-top: 2.5rem !important;
        padding-bottom: 2.5rem !important;
    }
    .control-label, label, .legible-white {
        color: #ffffff !important; font-weight: 500;
        text-shadow: 2px 2px 4px rgba(0,0,0,1);
    }
    .layout-shell {
        padding: 0 24px 40px;
    }
    .receipt-title { font-size: 1.8rem !important; font-weight: bold; }
    .weave-instruction {
        color: #ffffff !important; font-size: 1.4rem; font-style: italic;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 1);
        display: block; margin-top: 20px;
    }
    .text-mystic {
        color: #00f2ff; font-weight: 800;
        text-shadow: 0 0 25px rgba(0, 242, 255, 0.9);
    }
    .btn-glass {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.4);
        color: white; transition: 0.3s ease-in-out;
        font-weight: 700; text-transform: uppercase;
    }
    .btn-glass:hover {
        background: rgba(255, 255, 255, 0.35);
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(255, 255, 255, 0.2);
    }
    .login-shell {
        min-height: 100vh;
        min-height: 100svh;
        display: grid;
        place-items: center;
        padding: 24px;
    }
    .login-panel {
        width: min(100%, 430px);
        text-align: center;
    }
    .login-title {
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }
    .login-subtitle {
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 1.5rem;
    }
    .login-error {
        color: #ffb4b4;
        margin: 1rem 0 0;
    }
    .form-control, .form-select {
        background: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
    }
    @media (max-width: 768px), (max-aspect-ratio: 3/4) {
        .layout-shell .bslib-sidebar-layout {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        .layout-shell .bslib-sidebar-layout > .sidebar {
            order: 1;
            width: 100%;
        }
        .layout-shell .bslib-sidebar-layout > .main {
            order: 2;
            width: 100%;
        }
        .hero-title {
            font-size: 1.9rem;
            letter-spacing: 2px;
            padding-top: 1.5rem !important;
            padding-bottom: 1.5rem !important;
        }
        .layout-shell {
            padding: 0 12px 28px;
        }
        .glass-panel {
            padding: 16px;
            border-radius: 18px !important;
        }
        .receipt-title { font-size: 1.4rem !important; }
        .weave-instruction { font-size: 1.05rem; margin-top: 12px; }
        .text-mystic { font-size: 2rem; }
        .btn-glass { padding: 0.75rem 1rem; }
    }
"""


def login_ui(error_message: str | None = None):
    children = [
        ui.h1("The Shop Is Sealed", class_="login-title"),
        ui.p(
            "Speak the password to enter Madame Morrible's emporium.",
            class_="login-subtitle",
        ),
        ui.input_password(
            "login_password",
            "Password",
            placeholder="Enter the password",
        ),
        ui.input_action_button(
            "login_submit",
            "Unlock the Door",
            class_="btn-glass w-100 mt-3",
        ),
    ]

    if error_message:
        children.append(ui.p(error_message, class_="login-error", role="alert"))

    return ui.div(
        ui.div(*children, class_="glass-panel login-panel"),
        class_="login-shell",
    )


def calculator_ui():
    return ui.TagList(
        ui.h1(
            "Madame Morrible's Magic Mores",
            class_="text-center py-5 text-white hero-title",
        ),
        ui.div(
            ui.layout_sidebar(
                ui.sidebar(
                    ui.div(
                        ui.input_text(
                            "character_name",
                            "Seeker's Name",
                            placeholder="Who dares bargain?",
                        ),
                        ui.input_text(
                            "artifact_name",
                            "Artifact Name",
                            placeholder="What treasure is this?",
                        ),
                        ui.input_select(
                            "rarity",
                            "Artifact Rarity",
                            choices=["Common", "Uncommon", "Rare", "Very Rare"],
                        ),
                        ui.input_checkbox("is_consumable", "Consumable", False),
                        ui.input_slider(
                            "discount", "Manual Discount (%)", 0, 30, 0
                        ),
                        ui.input_numeric(
                            "persuasion_roll",
                            "Persuasion Roll",
                            value=10,
                            min=1,
                            max=40,
                        ),
                        ui.input_action_button(
                            "reroll",
                            "Invoke Valuation",
                            class_="btn-glass w-100 mt-3",
                        ),
                        class_="glass-panel",
                    ),
                    ui.hr(style="opacity: 0.2;"),
                    ui.span(
                        "Adjust the weave to reveal the cost.",
                        class_="weave-instruction ms-2",
                    ),
                    open="always",
                    max_height_mobile="100vh",
                ),
                ui.div(
                    ui.card(
                        ui.card_header(
                            "Arcane Receipt",
                            class_="receipt-title",
                            style="background:transparent; color: #fff;",
                        ),
                        ui.output_ui("valuation_output"),
                        class_="glass-panel",
                    )
                ),
            ),
            class_="layout-shell",
        ),
    )


app_ui = ui.page_fluid(
    ui.tags.meta(name="viewport", content="width=device-width, initial-scale=1"),
    ui.tags.style(glass_css),
    ui.tags.div(
        ui.tags.video(
            ui.tags.source(src="Magic_Popup_Shop (1).mp4", type="video/mp4"),
            id="bg-video", autoplay=True, loop=True, playsinline=True, muted=True
        ),
        id="video-container"
    ),
    ui.output_ui("page_content"),
)


def server(input, output, session):
    authenticated = reactive.Value(False)
    login_error = reactive.Value(None)
    rolled_result = reactive.Value(None)
    last_processed_reroll = reactive.Value(0)

    @output
    @render.ui
    def page_content():
        if authenticated():
            return calculator_ui()
        return login_ui(login_error())

    @reactive.Effect
    @reactive.event(input.login_submit, ignore_init=True)
    def _authenticate():
        if verify_password(input.login_password()):
            login_error.set(None)
            authenticated.set(True)
            return

        if APP_PASSWORD_HASH:
            login_error.set("That password did not open the door.")
        else:
            login_error.set(
                "Access is not configured. Set APP_PASSWORD_HASH in the hosting environment."
            )

    def current_input_signature():
        return (
            input.character_name().strip(),
            input.artifact_name().strip(),
            input.rarity(),
            input.is_consumable(),
            input.discount(),
            input.persuasion_roll(),
        )

    @reactive.Effect
    def _clear_stale_roll():
        result = rolled_result()
        if result is None:
            return

        if result["input_signature"] != current_input_signature():
            rolled_result.set(None)

    @reactive.Effect
    @reactive.event(input.reroll, ignore_init=True)
    def _roll_base_price():
        if not authenticated():
            return

        reroll_count = input.reroll()
        if reroll_count <= last_processed_reroll.get():
            return
        last_processed_reroll.set(reroll_count)

        input_signature = current_input_signature()
        char, art, rarity, is_consumable, manual_disc, persuasion_roll = input_signature

        # The Madame requires both names before the ritual begins.
        if not char or not art:
            ui.notification_show("Both Seeker and Artifact must be named before the stars speak.", type="warning")
            return

        # 1. Generate the base market value
        new_base = roll_price(rarity)
        persuasion_disc = get_persuasion_discount(persuasion_roll)
        total_disc = min(30, manual_disc + persuasion_disc)
        effective_base, final_cost, consumable_price = calculate_prices(
            new_base, rarity, total_disc, is_consumable
        )

        discord_logged = send_to_discord(
            char,
            art,
            rarity,
            effective_base,
            final_cost,
            total_disc,
            consumable_price,
        )
        if not discord_logged:
            ui.notification_show("The valuation was cast, but the Discord ledger could not be updated.", type="warning")

        rolled_result.set(
            {
                "char": char,
                "art": art,
                "market_value": effective_base,
                "influence_bonus": persuasion_disc,
                "aggregate_reduction": total_disc,
                "final_cost": final_cost,
                "consumable_price": consumable_price,
                "discord_logged": discord_logged,
                "input_signature": input_signature,
            }
        )

    @output
    @render.ui
    def valuation_output():
        if not authenticated():
            return ui.div()

        char = input.character_name().strip()
        art = input.artifact_name().strip()
        result = rolled_result()
        
        # Name-gate the receipt display
        if not char or not art:
            return ui.div(
                ui.p("Names are the anchors of reality. Provide both Seeker and Artifact to unveil the cost.", 
                     class_="legible-white fst-italic", style="font-size: 1.2rem; margin-top: 20px;")
            )
        
        if result is None:
            return ui.div(
                ui.p(f"The artifact '{art}' awaits its destiny for {char}. Invoke the valuation.", 
                     class_="legible-white fst-italic", style="margin-top: 20px;")
            )

        receipt_children = [
            ui.p(ui.strong("Seeker: "), result["char"], class_="legible-white"),
            ui.p(ui.strong("Artifact: "), result["art"], class_="legible-white"),
            ui.p(ui.strong("Market Value: "), format_price(result["market_value"]), class_="legible-white"),
            ui.p(ui.strong("Influence Bonus: "), f"{result['influence_bonus']}%", class_="legible-white"),
            ui.p(ui.strong("Aggregate Reduction: "), f"{result['aggregate_reduction']}%", class_="legible-white"),
            ui.hr(style="border-top: 1px solid rgba(255, 255, 255, 0.3);"),
            ui.h2(format_price(result["final_cost"]), class_="text-mystic"),
        ]

        if result["consumable_price"] is not None:
            receipt_children.append(
                ui.p(ui.strong("Consumable Price: "), format_price(result["consumable_price"]), class_="legible-white")
            )

        if result["discord_logged"]:
            receipt_children.append(
                ui.p("This transaction is now eternal in the Discord ledger.", style="font-style: italic; opacity: 0.7;")
            )
        else:
            receipt_children.append(
                ui.p("The valuation was cast, but the Discord ledger could not be updated.", style="font-style: italic; opacity: 0.7;")
            )

        return ui.div(*receipt_children)

# Identifying the 'www' directory for static assets
www_path = Path(__file__).parent / "www"
app = App(app_ui, server, static_assets=str(www_path))
