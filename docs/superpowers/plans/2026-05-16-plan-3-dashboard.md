# Elva Agent Team — Plan 3 : Dashboard Web

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Créer le script Python qui injecte `agents/outputs/report.json` dans le template HTML glassmorphisme orange et génère `dashboard/index.html` déployé automatiquement sur GitHub Pages.

**Architecture:** `generate_dashboard.py` lit `report.json` et remplace des placeholders dans un template HTML statique. GitHub Actions déploie automatiquement à chaque push.

**Tech Stack:** Python 3, HTML/CSS (glassmorphisme, accent #F97316), GitHub Pages, GitHub Actions

**Prérequis :** Plans 1 et 2 complétés — `report.json` existe et est valide.

---

## Structure de fichiers

```
E-commerce/
├── scripts/
│   ├── run_daily.sh           ← (Plan 2, modifié ici)
│   └── generate_dashboard.py  ← à créer
├── dashboard/
│   ├── template.html          ← template avec placeholders
│   └── index.html             ← généré automatiquement
└── .github/
    └── workflows/
        └── deploy-dashboard.yml  ← (Plan 1, déjà créé)
```

---

### Task 1 : Script generate_dashboard.py

**Files:**
- Create: `scripts/generate_dashboard.py`

- [ ] **Step 1 : Créer le script de génération**

Créer `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/scripts/generate_dashboard.py` :

```python
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
```

- [ ] **Step 2 : Vérifier la syntaxe Python**

```bash
cd /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce
python3 -c "import ast; ast.parse(open('scripts/generate_dashboard.py').read()); print('✅ Syntaxe OK')"
```

Expected : `✅ Syntaxe OK`

---

### Task 2 : Template HTML glassmorphisme orange

**Files:**
- Create: `dashboard/template.html`

- [ ] **Step 1 : Créer le template avec placeholders**

Copier le design validé (dashboard-final.html) et remplacer les données statiques par des placeholders `{{VARIABLE}}`.

Créer `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/dashboard/template.html` en copiant le contenu de `.superpowers/brainstorm/.../content/dashboard-final.html` puis remplacer :

| Valeur statique | Placeholder |
|---|---|
| `1.8x` (ROAS) | `{{ROAS}}` |
| `style="color:#F97316"` sur ROAS | `style="color:{{ROAS_COLOR}}"` |
| `↓ Cible non atteinte` | `{{ROAS_TREND}}` |
| `14.2€` (CPM) | `{{CPM}}` |
| `86€` (Revenus) | `{{REVENUS}}` |
| `48€` (Dépense) | `{{DEPENSE}}` |
| `16 mai 2026` (date sidebar) | `{{DATE}}` |
| `08h15` (live badge) | `{{HEURE}}` |
| Bloc alerte complet | `{{ALERT_HTML}}` |
| Bloc actions complet | `{{ACTIONS_HTML}}` |
| `Concurrent A` | `{{WINNER_MARQUE}}` |
| `52 jours actif` | `{{WINNER_JOURS}}` |
| Hook concurrent | `{{WINNER_HOOK}}` |
| `78` (hook score) | `{{WINNER_SCORE}}` |
| `Question rhétorique...` | `{{WINNER_LECON}}` |
| `Brief #3 — Confort quotidien` | `{{BRIEF_TITRE}}` |
| Hook brief | `{{BRIEF_HOOK}}` |
| `9:16, 15s, lip sync` | `{{BRIEF_FORMAT}}` |
| `Découvrir` | `{{BRIEF_CTA}}` |

Ajouter dans le `<head>` :
```html
<meta http-equiv="refresh" content="3600">
```
(refresh automatique toutes les heures)

- [ ] **Step 2 : Vérifier que tous les placeholders sont présents**

```bash
grep -o '{{[A-Z_]*}}' /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/dashboard/template.html | sort -u
```

Expected : liste de tous les placeholders définis dans `generate_dashboard.py`.

---

### Task 3 : Tester la génération complète

**Files:**
- Verify: `dashboard/index.html`

- [ ] **Step 1 : Créer un report.json de test**

```bash
cat > /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/agents/outputs/report.json << 'EOF'
{
  "date": "2026-05-16",
  "heure_rapport": "08:15",
  "verdict_global": "⚠️ ROAS sous la cible",
  "resume_executif": "Ton CPM élevé vient d'un hook score faible. Priorité : couper Lookalike 2% et tester l'angle confort.",
  "kpis": {"roas": 1.8, "roas_cible": 2.5, "cpm": 14.2, "revenus": 86.0, "depense": 48.0},
  "alerte": {"active": true, "message": "Adset Lookalike 2% — ROAS 0.6 depuis 3 jours · 18€/jour gaspillés", "urgence": "haute"},
  "actions_prioritaires": [
    {"rang": 1, "action": "Couper l'adset Lookalike 2%", "pourquoi": "ROAS 0.6 depuis 3 jours", "comment": "Meta Ads Manager > Désactiver Lookalike 2%", "impact": "+18€/jour", "tag": "urgent"},
    {"rang": 2, "action": "Scaler Broad FR +20%", "pourquoi": "ROAS 2.8 stable sur 5 jours", "comment": "Budget : 12€ → 14€", "impact": "+20% revenus", "tag": "opportunite"},
    {"rang": 3, "action": "Tourner brief lip sync #3", "pourquoi": "Gap hook score vs concurrents", "comment": "Voir brief ci-dessous", "impact": "-15% CPM potentiel", "tag": "creatif"}
  ],
  "winneuse_semaine": {"marque": "Concurrent A", "jours_actif": 52, "hook": "Le seul soutien-gorge que je remets tous les jours...", "hook_score": 78, "angle": "confort_quotidien", "lecon": "Question rhétorique + démonstration immédiate"},
  "brief_semaine": {"titre": "Brief #3 — Confort quotidien", "hook": "Le seul soutien-gorge que je remets tous les jours...", "format": "9:16, 15s, lip sync", "cta": "Lien dans la bio"}
}
EOF
```

- [ ] **Step 2 : Générer le dashboard**

```bash
cd /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce
python3 scripts/generate_dashboard.py
```

Expected : `✅ Dashboard généré : .../dashboard/index.html`

- [ ] **Step 3 : Vérifier visuellement**

```bash
open /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/dashboard/index.html
```

Expected : dashboard orange glassmorphisme avec les vraies données du JSON.

- [ ] **Step 4 : Vérifier qu'aucun placeholder n'est resté**

```bash
grep -c '{{' /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/dashboard/index.html
```

Expected : `0`

---

### Task 4 : Déploiement GitHub Pages

**Files:**
- Verify: `.github/workflows/deploy-dashboard.yml` (déjà créé en Plan 1)

- [ ] **Step 1 : Commiter et pousser le dashboard généré**

```bash
cd /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce
git add dashboard/ scripts/generate_dashboard.py
git commit -m "feat: add dashboard template and generator script"
git push origin main
```

- [ ] **Step 2 : Vérifier que GitHub Actions se déclenche**

```bash
gh run list --limit 3
```

Expected : un workflow "Deploy Dashboard" en cours ou complété.

- [ ] **Step 3 : Vérifier le dashboard en ligne**

Ouvrir `https://ton-username.github.io/elva-dashboard/` dans le navigateur.

Expected : dashboard orange glassmorphisme avec les données du test JSON.

---

### Task 5 : Test end-to-end complet

**Files:**
- Verify: tous

- [ ] **Step 1 : Lancer run_daily.sh complet**

```bash
/bin/bash /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/scripts/run_daily.sh
```

Expected output :
```
🚀 [2026-05-16 HH:MM] Démarrage des agents Elva...
🔍 [1/6] Spy Concurrent...
✅ spy.json généré
📈 [2/6] Analyse Performance...
✅ performance.json généré
🧠 [3/6] Hook & Virality...
✅ hook.json généré
💰 [4/6] Budget Optimizer...
✅ budget.json généré
✍️  [5/6] Brief Créatif...
✅ brief.json généré
🎯 [6/6] Media Buyer Expert...
✅ report.json généré
📊 Génération du dashboard...
✅ dashboard/index.html généré
🚀 Push vers GitHub Pages...
✅ [2026-05-16 HH:MM] Rapport terminé. Dashboard mis à jour.
```

- [ ] **Step 2 : Vérifier le dashboard en ligne avec les vraies données**

Ouvrir `https://ton-username.github.io/elva-dashboard/`

Expected : données réelles de tes comptes Meta, Shopify, Pinterest.

---

## Validation finale Plan 3

- [ ] `generate_dashboard.py` tourne sans erreur
- [ ] `dashboard/index.html` généré sans placeholder restant
- [ ] Dashboard visible sur GitHub Pages
- [ ] GitHub Actions déploie automatiquement à chaque push sur main
- [ ] Run complet `run_daily.sh` → dashboard mis à jour sur GitHub Pages
- [ ] Cron 08h00 confirmé (`crontab -l`)
