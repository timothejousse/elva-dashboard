import json
import os
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
REPORT_PATH = ROOT / "agents/outputs/report.json"
TEMPLATE_PATH = ROOT / "dashboard/template.html"
OUTPUT_PATH = ROOT / "dashboard/index.html"


def load_report():
    with open(REPORT_PATH) as f:
        return json.load(f)


def tag_color(tag):
    colors = {
        "urgent": ("#FEF3C7", "#D97706", "#FCD34D"),
        "opportunite": ("#D1FAE5", "#059669", "#6EE7B7"),
        "creatif": ("#DBEAFE", "#2563EB", "#93C5FD"),
    }
    return colors.get(tag, ("#F3F4F6", "#6B7280", "#D1D5DB"))


def tag_label(tag):
    labels = {"urgent": "Urgent", "opportunite": "Opportunité", "creatif": "Créatif"}
    return labels.get(tag, tag)


def render_actions(actions):
    html = ""
    for a in actions:
        bg, text, border = tag_color(a["tag"])
        html += f"""
        <div class="action-item">
          <div class="check"></div>
          <div class="action-n">{a['rang']}</div>
          <div class="action-body">
            <div class="action-title">{a['action']}</div>
            <div class="action-desc">{a['pourquoi']}</div>
            <div class="action-how">{a['comment']}</div>
            <span class="tag" style="background:{bg};color:{text};border-color:{border}">{tag_label(a['tag'])}</span>
          </div>
        </div>"""
    return html


def render_alert(alert):
    if not alert.get("active"):
        return ""
    return f"""
    <div class="alert">
      <div class="alert-icon">⚠️</div>
      <div class="alert-body">
        <div class="alert-title">{alert['message']}</div>
      </div>
    </div>"""


def roas_color(roas, target=2.5):
    if roas >= target:
        return "#16a34a"
    elif roas >= target * 0.7:
        return "#d97706"
    return "#dc2626"


def roas_trend(roas, target=2.5):
    if roas >= target:
        return f'<span class="kpi-trend up">✓ Objectif atteint</span>'
    return f'<span class="kpi-trend down">↓ Cible {target}x</span>'


def generate(report):
    kpis = report["kpis"]
    winner = report.get("winneuse_semaine", {})
    brief = report.get("brief_semaine", {})

    with open(TEMPLATE_PATH) as f:
        html = f.read()

    replacements = {
        "{{DATE}}": report["date"],
        "{{HEURE}}": report.get("heure_rapport", "08:15"),
        "{{VERDICT}}": report.get("verdict_global", ""),
        "{{RESUME}}": report.get("resume_executif", ""),
        "{{ROAS}}": str(kpis["roas"]) + "x",
        "{{ROAS_COLOR}}": roas_color(kpis["roas"]),
        "{{ROAS_TREND}}": roas_trend(kpis["roas"]),
        "{{CPM}}": str(kpis["cpm"]) + "€",
        "{{REVENUS}}": str(kpis["revenus"]) + "€",
        "{{DEPENSE}}": str(kpis["depense"]) + "€",
        "{{ALERT_HTML}}": render_alert(report.get("alerte", {})),
        "{{ACTIONS_HTML}}": render_actions(report.get("actions_prioritaires", [])),
        "{{WINNER_MARQUE}}": winner.get("marque", "—"),
        "{{WINNER_JOURS}}": str(winner.get("jours_actif", "—")),
        "{{WINNER_HOOK}}": winner.get("hook", "—"),
        "{{WINNER_SCORE}}": str(winner.get("hook_score", "—")),
        "{{WINNER_LECON}}": winner.get("lecon", "—"),
        "{{BRIEF_TITRE}}": brief.get("titre", "—"),
        "{{BRIEF_HOOK}}": brief.get("hook", "—"),
        "{{BRIEF_FORMAT}}": brief.get("format", "—"),
        "{{BRIEF_CTA}}": brief.get("cta", "—"),
    }

    for placeholder, value in replacements.items():
        html = html.replace(placeholder, str(value))

    with open(OUTPUT_PATH, "w") as f:
        f.write(html)

    print(f"✅ Dashboard généré : {OUTPUT_PATH}")


if __name__ == "__main__":
    report = load_report()
    generate(report)
