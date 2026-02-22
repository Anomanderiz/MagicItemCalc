from pathlib import Path
from shiny import App, render, ui, reactive
import random
import requests
import threading

# --- Discord Webhook Configuration ---
# Replace with the unique thread-link provided by your Discord server settings.
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1464165711759937689/QHY4-RHmThzEGWUaMf1oo2eZYo-rBqcX2txQZjJcqsCQbqd5alH7V6fRls1Xz8B92SJi"

def send_to_discord(char_name, artifact_name, rarity, base, final, total_discount):
    """Dispatches a formatted missive to the Madame's Discord ledger."""
    if not DISCORD_WEBHOOK_URL or DISCORD_WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_URL":
        return False
    
    payload = {
        "username": "Madame Morrible",
        "embeds": [{
            "title": "Arcane Transaction Chronicled",
            "color": 0x00f2ff,
            "description": f"The weave has finalized a deal for **{char_name}**.",
            "fields": [
                {"name": "Artifact", "value": f"*{artifact_name}*", "inline": False},
                {"name": "Rarity", "value": rarity, "inline": True},
                {"name": "Market Value", "value": f"{base:,} gp", "inline": True},
                {"name": "Total Concession", "value": f"{total_discount}%", "inline": True},
                {"name": "Final Tribute", "value": f"**{final:,} gp**", "inline": False}
            ],
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

def get_persuasion_discount(roll: int) -> int:
    if roll < 15: return 0
    if roll <= 20: return 10
    if roll <= 26: return 20
    return 30

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
    ui.h1("Madame Morrible's Magic Mores", class_="text-center py-5 text-white hero-title"),
    ui.div(
        ui.layout_sidebar(
            ui.sidebar(
                ui.div(
                    ui.input_text("character_name", "Seeker's Name", placeholder="Who dares bargain?"),
                    ui.input_text("artifact_name", "Artifact Name", placeholder="What treasure is this?"),
                    ui.input_select("rarity", "Artifact Rarity", 
                                   choices=["Common", "Uncommon", "Rare", "Very Rare"]),
                    ui.input_slider("discount", "Manual Discount (%)", 0, 30, 0),
                    ui.input_numeric("persuasion_roll", "Persuasion Roll", value=10, min=1, max=40),
                    ui.input_action_button("reroll", "Invoke Valuation", class_="btn-glass w-100 mt-3"),
                    class_="glass-panel"
                ),
                ui.hr(style="opacity: 0.2;"),
                ui.span("Adjust the weave to reveal the cost.", class_="weave-instruction ms-2"),
                open="always",
                max_height_mobile="100vh"
            ),
            ui.div(
                ui.card(
                    ui.card_header("Arcane Receipt", class_="receipt-title", style="background:transparent; color: #fff;"),
                    ui.output_ui("valuation_output"),
                    class_="glass-panel"
                )
            ),
        ),
        class_="layout-shell"
    ),
)

def server(input, output, session):
    base_price = reactive.Value(0)
    last_sent = reactive.Value(None)
    last_processed_reroll = reactive.Value(0)

    @reactive.Calc
    def total_discount():
        manual_disc = input.discount()
        persuasion_disc = get_persuasion_discount(input.persuasion_roll())
        return min(30, manual_disc + persuasion_disc)

    @reactive.Calc
    def final_price():
        bp = base_price()
        if bp <= 0:
            return 0
        return int(bp * (1 - total_discount() / 100))

    @reactive.Effect
    @reactive.event(input.reroll, ignore_init=True)
    def _roll_base_price():
        reroll_count = input.reroll()
        if reroll_count <= last_processed_reroll.get():
            return
        last_processed_reroll.set(reroll_count)

        char = input.character_name().strip()
        art = input.artifact_name().strip()

        # The Madame requires both names before the ritual begins.
        if not char or not art:
            ui.notification_show("Both Seeker and Artifact must be named before the stars speak.", type="warning")
            return

        # 1. Generate the base market value
        new_base = roll_price(input.rarity())
        base_price.set(new_base)
        total_disc = total_discount()
        final_cost = int(new_base * (1 - total_disc / 100))
        current = (char, art, input.rarity(), new_base, total_disc, final_cost)
        if last_sent.get() == current:
            return

        last_sent.set(current)
        threading.Thread(
            target=send_to_discord,
            args=(char, art, input.rarity(), new_base, final_cost, total_disc),
            daemon=True
        ).start()

    @output
    @render.ui
    def valuation_output():
        char = input.character_name().strip()
        art = input.artifact_name().strip()
        
        # Name-gate the receipt display
        if not char or not art:
            return ui.div(
                ui.p("Names are the anchors of reality. Provide both Seeker and Artifact to unveil the cost.", 
                     class_="legible-white fst-italic", style="font-size: 1.2rem; margin-top: 20px;")
            )
        
        if base_price() == 0:
            return ui.div(
                ui.p(f"The artifact '{art}' awaits its destiny for {char}. Invoke the valuation.", 
                     class_="legible-white fst-italic", style="margin-top: 20px;")
            )

        bp = base_price()
        p_disc = get_persuasion_discount(input.persuasion_roll())
        total_disc = total_discount()
        final_cost = final_price()
        
        return ui.div(
            ui.p(ui.strong("Seeker: "), char, class_="legible-white"),
            ui.p(ui.strong("Artifact: "), art, class_="legible-white"),
            ui.p(ui.strong("Market Value: "), f"{bp:,} gp", class_="legible-white"),
            ui.p(ui.strong("Influence Bonus: "), f"{p_disc}%", class_="legible-white"),
            ui.p(ui.strong("Aggregate Reduction: "), f"{total_disc}%", class_="legible-white"),
            ui.hr(style="border-top: 1px solid rgba(255, 255, 255, 0.3);"),
            ui.h2(f"{final_cost:,} gp", class_="text-mystic"),
            ui.p("This transaction is now eternal in the Discord ledger.", style="font-style: italic; opacity: 0.7;")
        )

# Identifying the 'www' directory for static assets
www_path = Path(__file__).parent / "www"
app = App(app_ui, server, static_assets=str(www_path))
