import json
import os
from datetime import datetime, date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
REPORT_PATH = ROOT / "agents/outputs/report.json"
PERFORMANCE_PATH = ROOT / "agents/outputs/performance.json"
SPY_PATH = ROOT / "agents/outputs/spy.json"
BUDGET_PATH = ROOT / "agents/outputs/budget.json"
HISTORY_DIR = ROOT / "agents/outputs/history"
DASHBOARD_DIR = ROOT / "dashboard"

HISTORY_DIR.mkdir(parents=True, exist_ok=True)
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default or {}


def archive_report():
    """Archive today's report.json to history/"""
    if REPORT_PATH.exists():
        today = date.today().isoformat()
        dest = HISTORY_DIR / f"{today}.json"
        dest.write_text(REPORT_PATH.read_text())


def load_history():
    """Load all historical reports sorted by date desc"""
    reports = []
    if HISTORY_DIR.exists():
        for f in sorted(HISTORY_DIR.glob("*.json"), reverse=True):
            try:
                data = json.loads(f.read_text())
                data["_date"] = f.stem
                reports.append(data)
            except Exception:
                pass
    return reports


def nav(active):
    tabs = [
        ("index.html", "Rapport du jour"),
        ("analytics.html", "Analytics"),
        ("ads.html", "Mes Ads"),
        ("concurrents.html", "Concurrents"),
    ]
    links = ""
    for href, label in tabs:
        cls = "nav-tab active" if href == active else "nav-tab"
        links += f'<a href="{href}" class="{cls}">{label}</a>'
    return f"""
    <nav class="nav">
      <div class="nav-logo">&#x26A1; Elva</div>
      {links}
    </nav>"""


def style():
    return """
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #F9FAFB; color: #111827; }
      .nav { background: #fff; border-bottom: 1px solid #E5E7EB; padding: 0 24px; display: flex; align-items: center; height: 52px; }
      .nav-logo { font-weight: 800; font-size: 16px; color: #F97316; margin-right: 32px; letter-spacing: -0.5px; }
      .nav-tab { padding: 16px; font-size: 14px; color: #6B7280; border-bottom: 2px solid transparent; margin-bottom: -1px; text-decoration: none; display: inline-block; }
      .nav-tab.active { color: #F97316; border-bottom-color: #F97316; font-weight: 600; }
      .nav-tab:hover { color: #374151; }
      .page-header { background: #fff; border-bottom: 1px solid #E5E7EB; padding: 16px 24px; display: flex; align-items: center; justify-content: space-between; }
      .page-header h1 { font-size: 20px; font-weight: 700; }
      .page-body { padding: 20px 24px; max-width: 1200px; margin: 0 auto; }
      .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }
      .kpi-card { background: #fff; border: 1px solid #E5E7EB; border-radius: 12px; padding: 18px 20px; }
      .kpi-label { font-size: 12px; color: #6B7280; font-weight: 500; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.05em; }
      .kpi-value { font-size: 26px; font-weight: 800; margin-bottom: 4px; }
      .kpi-compare { font-size: 12px; color: #6B7280; }
      .kpi-bar { height: 3px; background: #F3F4F6; border-radius: 2px; margin-top: 10px; overflow: hidden; }
      .kpi-bar-fill { height: 100%; border-radius: 2px; }
      .card { background: #fff; border: 1px solid #E5E7EB; border-radius: 12px; overflow: hidden; margin-bottom: 16px; }
      .card-header { padding: 14px 20px; border-bottom: 1px solid #F3F4F6; display: flex; align-items: center; justify-content: space-between; }
      .card-header h3 { font-size: 14px; font-weight: 600; }
      .table-row { display: grid; padding: 12px 20px; border-bottom: 1px solid #F9FAFB; align-items: center; font-size: 13px; }
      .table-row.thead { background: #F9FAFB; font-size: 11px; font-weight: 600; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; }
      .badge { font-size: 11px; padding: 3px 10px; border-radius: 20px; font-weight: 600; display: inline-flex; align-items: center; gap: 4px; }
      .badge-red { background: #FEF2F2; color: #DC2626; }
      .badge-green { background: #F0FDF4; color: #16A34A; }
      .badge-amber { background: #FFFBEB; color: #D97706; }
      .badge-orange { background: #FFF7ED; color: #EA580C; }
      .badge-blue { background: #EFF6FF; color: #2563EB; }
      .up { color: #16A34A; } .down { color: #DC2626; } .neutral { color: #6B7280; }
      .alert-box { background: #FEF2F2; border: 1px solid #FECACA; border-radius: 12px; padding: 14px 18px; display: flex; gap: 12px; align-items: flex-start; margin-bottom: 16px; }
    </style>"""


def roas_color(roas, target=2.5):
    if roas >= target:
        return "#16A34A"
    elif roas >= target * 0.7:
        return "#D97706"
    return "#DC2626"


def ad_status(roas, days):
    if roas < 1.5 and days >= 3:
        return "COUPER", "badge-red"
    elif roas >= 2.5 and days >= 5:
        return "SCALER", "badge-green"
    elif roas >= 2.0:
        return "GARDER", "badge-amber"
    else:
        return "SURVEILLER", "badge-orange"


def verdict_badge(verdict):
    v = verdict.lower()
    if "✅" in verdict or "ok" in v or "atteint" in v:
        return "badge-green"
    elif "⚠️" in verdict or "sous" in v or "faible" in v:
        return "badge-red"
    return "badge-amber"


# ─── PAGE 1 : RAPPORT DU JOUR ─────────────────────────────────────────────────

def generate_index(report):
    kpis = report.get("kpis", {})
    alerte = report.get("alerte", {})
    actions = report.get("actions_prioritaires", [])
    winner = report.get("winneuse_semaine", {})
    brief = report.get("brief_semaine", {})

    def tag_color(tag):
        return {"urgent": ("badge-red", "&#x1F534;"), "opportunite": ("badge-green", "&#x1F4C8;"), "creatif": ("badge-blue", "&#x270D;")}.get(tag, ("badge-amber", "&bull;"))

    alert_html = ""
    if alerte.get("active"):
        alert_html = f'<div class="alert-box"><div style="font-size:20px">&#x26A0;&#xFE0F;</div><div><div style="font-weight:700;color:#DC2626;margin-bottom:2px">Alerte</div><div style="font-size:13px;color:#374151">{alerte["message"]}</div></div></div>'

    actions_html = ""
    for a in actions:
        badge_cls, icon = tag_color(a.get("tag", ""))
        actions_html += f"""
        <div style="display:flex;gap:14px;align-items:flex-start;padding:14px 20px;border-bottom:1px solid #F9FAFB;">
          <div style="width:28px;height:28px;border-radius:50%;background:#F97316;color:#fff;font-weight:800;font-size:13px;display:flex;align-items:center;justify-content:center;flex-shrink:0">{a['rang']}</div>
          <div style="flex:1">
            <div style="font-weight:600;font-size:14px;margin-bottom:3px">{a['action']}</div>
            <div style="font-size:12px;color:#6B7280;margin-bottom:4px">{a['pourquoi']} &mdash; {a['comment']}</div>
            <span class="badge {badge_cls}">{icon} {a.get('tag','').capitalize()}</span>
          </div>
          <div style="font-size:12px;color:#16A34A;font-weight:600;white-space:nowrap">{a.get('impact','')}</div>
        </div>"""

    roas_val = kpis.get("roas", 0)
    rc = roas_color(roas_val)
    roas_trend = f'<span style="color:#16A34A">&#x2713; Objectif atteint</span>' if roas_val >= 2.5 else f'<span style="color:#DC2626">&#x2193; Cible 2.5x</span>'

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="3600"><title>Elva &mdash; Rapport du jour</title>{style()}</head>
<body>
{nav("index.html")}
<div class="page-header">
  <div>
    <h1>{report.get("verdict_global","Rapport du jour")}</h1>
    <div style="font-size:13px;color:#6B7280;margin-top:4px">{report.get("date","")} &middot; {report.get("heure_rapport","08:15")}</div>
  </div>
</div>
<div class="page-body">
  <p style="font-size:14px;color:#374151;margin-bottom:20px;line-height:1.6;background:#fff;padding:14px 18px;border-radius:10px;border:1px solid #E5E7EB">{report.get("resume_executif","")}</p>

  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">ROAS</div>
      <div class="kpi-value" style="color:{rc}">{roas_val}x</div>
      <div class="kpi-compare">{roas_trend}</div>
      <div class="kpi-bar"><div class="kpi-bar-fill" style="width:{min(roas_val/2.5*100,100):.0f}%;background:{rc}"></div></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">CPM</div>
      <div class="kpi-value" style="color:#D97706">{kpis.get("cpm",0)}&euro;</div>
      <div class="kpi-compare">Cible &lt; 12&euro;</div>
      <div class="kpi-bar"><div class="kpi-bar-fill" style="width:{min(kpis.get('cpm',0)/20*100,100):.0f}%;background:#D97706"></div></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Revenus Shopify</div>
      <div class="kpi-value" style="color:#16A34A">{kpis.get("revenus",0)}&euro;</div>
      <div class="kpi-compare">D&eacute;pense : {kpis.get("depense",0)}&euro;</div>
      <div class="kpi-bar"><div class="kpi-bar-fill" style="width:{min(kpis.get('revenus',0)/200*100,100):.0f}%;background:#16A34A"></div></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">D&eacute;pense Meta</div>
      <div class="kpi-value">{kpis.get("depense",0)}&euro;</div>
      <div class="kpi-compare">Budget : 50&euro;/jour</div>
      <div class="kpi-bar"><div class="kpi-bar-fill" style="width:{min(kpis.get('depense',0)/50*100,100):.0f}%;background:#6B7280"></div></div>
    </div>
  </div>

  {alert_html}

  <div class="card" style="margin-bottom:16px">
    <div class="card-header"><h3>Actions prioritaires du jour</h3></div>
    {actions_html}
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
    <div class="card">
      <div class="card-header"><h3>&#x1F3C6; Winneuse de la semaine</h3></div>
      <div style="padding:16px 20px">
        <div style="font-weight:700;font-size:15px;margin-bottom:4px">{winner.get("marque","&mdash;")}</div>
        <div style="font-size:12px;color:#6B7280;margin-bottom:10px">Active {winner.get("jours_actif","&mdash;")} jours &middot; Hook score {winner.get("hook_score","&mdash;")}/100</div>
        <div style="font-size:13px;color:#374151;font-style:italic;margin-bottom:8px">&ldquo;{winner.get("hook","&mdash;")}&rdquo;</div>
        <div style="font-size:12px;color:#F97316;font-weight:500">&#x1F4A1; {winner.get("lecon","&mdash;")}</div>
      </div>
    </div>
    <div class="card">
      <div class="card-header"><h3>&#x270D;&#xFE0F; Brief cr&eacute;atif</h3></div>
      <div style="padding:16px 20px">
        <div style="font-weight:700;font-size:15px;margin-bottom:4px">{brief.get("titre","&mdash;")}</div>
        <div style="font-size:13px;color:#374151;font-style:italic;margin-bottom:8px">&ldquo;{brief.get("hook","&mdash;")}&rdquo;</div>
        <div style="font-size:12px;color:#6B7280">{brief.get("format","&mdash;")} &middot; CTA : {brief.get("cta","&mdash;")}</div>
      </div>
    </div>
  </div>
</div>
</body></html>"""

    (DASHBOARD_DIR / "index.html").write_text(html)
    print("OK index.html generated")


# ─── PAGE 2 : ANALYTICS ───────────────────────────────────────────────────────

def generate_analytics(report, history):
    kpis = report.get("kpis", {})

    # Sparkline SVG from history (last 14 days)
    roas_points = []
    labels = []
    for h in reversed(history[-14:]):
        v = h.get("kpis", {}).get("roas", 0)
        roas_points.append(v)
        labels.append(h.get("_date", "")[-5:])

    def sparkline_path(values, w=660, h=120, color="#F97316"):
        if not values or max(values) == min(values):
            return f'<line x1="0" y1="{h//2}" x2="{w}" y2="{h//2}" stroke="{color}" stroke-width="2"/>'
        mn, mx = min(values), max(values)
        pad = (mx - mn) * 0.2 or 0.5
        mn -= pad; mx += pad
        n = len(values)
        pts = []
        for i, v in enumerate(values):
            x = i / (n - 1) * w if n > 1 else w / 2
            y = h - (v - mn) / (mx - mn) * h
            pts.append(f"{x:.1f},{y:.1f}")
        path = "M" + " L".join(pts)
        # target line at 2.5
        ty = h - (2.5 - mn) / (mx - mn) * h
        target = f'<line x1="0" y1="{ty:.1f}" x2="{w}" y2="{ty:.1f}" stroke="#FCD34D" stroke-width="1.5" stroke-dasharray="6,4"/>'
        return f'{target}<path d="{path}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>'

    label_html = ""
    if labels:
        step = 660 / (len(labels) - 1) if len(labels) > 1 else 0
        for i, l in enumerate(labels):
            label_html += f'<text x="{i*step:.0f}" y="145" font-size="10" fill="#9CA3AF" text-anchor="middle">{l}</text>'

    history_rows = ""
    for i, h in enumerate(history[:20]):
        v = h.get("verdict_global", "&mdash;")
        kp = h.get("kpis", {})
        rc = roas_color(kp.get("roas", 0))
        bg = "#FAFAFA" if i % 2 else "#fff"
        history_rows += f"""
        <div class="table-row" style="grid-template-columns:100px 1fr 80px 80px 80px 110px;background:{bg}">
          <div style="font-weight:600">{h.get("_date","&mdash;")}</div>
          <div><span class="badge {verdict_badge(v)}">{v}</span></div>
          <div style="color:{rc};font-weight:700">{kp.get("roas","&mdash;")}x</div>
          <div style="color:#D97706">{kp.get("cpm","&mdash;")}&euro;</div>
          <div>{kp.get("revenus","&mdash;")}&euro;</div>
          <div><a href="index.html" style="color:#F97316;font-size:12px;text-decoration:none">Voir rapport &rarr;</a></div>
        </div>"""

    if not history_rows:
        history_rows = '<div style="padding:20px;text-align:center;color:#6B7280;font-size:13px">Aucun historique disponible &mdash; les donn&eacute;es s\'accumuleront apr&egrave;s chaque run quotidien.</div>'

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Elva &mdash; Analytics</title>{style()}</head>
<body>
{nav("analytics.html")}
<div class="page-header">
  <h1>Analytics</h1>
  <div style="font-size:13px;color:#6B7280">{report.get("date","")} &mdash; donn&eacute;es du dernier rapport</div>
</div>
<div class="page-body">
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">ROAS</div>
      <div class="kpi-value" style="color:{roas_color(kpis.get('roas',0))}">{kpis.get('roas',0)}x</div>
      <div class="kpi-compare">Cible : 2.5x</div>
      <div class="kpi-bar"><div class="kpi-bar-fill" style="width:{min(kpis.get('roas',0)/2.5*100,100):.0f}%;background:{roas_color(kpis.get('roas',0))}"></div></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">CPM</div>
      <div class="kpi-value" style="color:#D97706">{kpis.get('cpm',0)}&euro;</div>
      <div class="kpi-compare">Cible : &lt; 12&euro;</div>
      <div class="kpi-bar"><div class="kpi-bar-fill" style="width:{min(kpis.get('cpm',0)/20*100,100):.0f}%;background:#D97706"></div></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Revenus</div>
      <div class="kpi-value" style="color:#16A34A">{kpis.get('revenus',0)}&euro;</div>
      <div class="kpi-compare">D&eacute;pense : {kpis.get('depense',0)}&euro;</div>
      <div class="kpi-bar"><div class="kpi-bar-fill" style="width:{min(kpis.get('revenus',0)/200*100,100):.0f}%;background:#16A34A"></div></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">D&eacute;pense</div>
      <div class="kpi-value">{kpis.get('depense',0)}&euro;</div>
      <div class="kpi-compare">Budget : 50&euro;/jour</div>
      <div class="kpi-bar"><div class="kpi-bar-fill" style="width:{min(kpis.get('depense',0)/50*100,100):.0f}%;background:#6B7280"></div></div>
    </div>
  </div>

  <div class="card" style="margin-bottom:16px">
    <div class="card-header">
      <h3>&Eacute;volution du ROAS</h3>
      <div style="display:flex;gap:16px;font-size:12px;color:#6B7280">
        <span style="display:flex;align-items:center;gap:4px"><span style="width:12px;height:2px;background:#F97316;display:inline-block;border-radius:2px"></span>ROAS</span>
        <span style="display:flex;align-items:center;gap:4px"><span style="width:12px;height:2px;background:#FCD34D;display:inline-block;border-radius:2px;border-top:1px dashed #FCD34D"></span>Cible 2.5x</span>
      </div>
    </div>
    <div style="padding:20px;overflow:hidden">
      <svg viewBox="0 0 660 150" style="width:100%;height:150px">
        <line x1="0" y1="0" x2="660" y2="0" stroke="#F9FAFB" stroke-width="1"/>
        <line x1="0" y1="40" x2="660" y2="40" stroke="#F9FAFB" stroke-width="1"/>
        <line x1="0" y1="80" x2="660" y2="80" stroke="#F9FAFB" stroke-width="1"/>
        <line x1="0" y1="120" x2="660" y2="120" stroke="#F9FAFB" stroke-width="1"/>
        {sparkline_path(roas_points) if roas_points else '<text x="330" y="75" text-anchor="middle" font-size="13" fill="#9CA3AF">Données disponibles après le premier run</text>'}
        {label_html}
      </svg>
    </div>
  </div>

  <div class="card">
    <div class="card-header">
      <h3>Historique des rapports</h3>
      <span style="font-size:12px;color:#6B7280">{len(history)} rapports archiv&eacute;s</span>
    </div>
    <div class="table-row thead" style="grid-template-columns:100px 1fr 80px 80px 80px 110px">
      <div>Date</div><div>Verdict</div><div>ROAS</div><div>CPM</div><div>Revenus</div><div></div>
    </div>
    {history_rows}
  </div>
</div>
</body></html>"""

    (DASHBOARD_DIR / "analytics.html").write_text(html)
    print("OK analytics.html generated")


# ─── PAGE 3 : MES ADS ─────────────────────────────────────────────────────────

def generate_ads(performance, budget):
    meta = performance.get("meta", {})
    adsets = meta.get("adsets", []) or []
    creatifs_top = meta.get("top_creatifs", []) or []
    creatifs_couper = meta.get("creatifs_a_couper", []) or []
    budget_recs = budget.get("recommandations", []) or []

    # Merge creatives
    all_creatifs = creatifs_top + creatifs_couper
    creatif_rows = ""
    for i, c in enumerate(all_creatifs):
        roas = c.get("roas", 0)
        days = c.get("jours_actif", 0)
        status, badge_cls = ad_status(roas, days)
        rc = roas_color(roas)
        bg = "#FAFAFA" if i % 2 else "#fff"
        creatif_rows += f"""
        <div class="table-row" style="grid-template-columns:2fr 80px 80px 80px 80px 120px;background:{bg}">
          <div style="font-weight:600">{c.get("nom","&mdash;")}</div>
          <div style="color:{rc};font-weight:700">{roas}x</div>
          <div style="color:#D97706">{c.get("cpm","&mdash;")}&euro;</div>
          <div style="color:#6B7280">{days}j</div>
          <div>{c.get("depense","&mdash;")}&euro;</div>
          <div><span class="badge {badge_cls}">{status}</span></div>
        </div>"""

    if not creatif_rows:
        creatif_rows = '<div style="padding:20px;text-align:center;color:#6B7280;font-size:13px">Aucune donn&eacute;e cr&eacute;atif &mdash; disponible apr&egrave;s connexion Meta MCP</div>'

    adset_rows = ""
    for i, a in enumerate(adsets):
        roas = a.get("roas", 0)
        rc = roas_color(roas)
        bg = "#FAFAFA" if i % 2 else "#fff"
        adset_rows += f"""
        <div class="table-row" style="grid-template-columns:2fr 80px 80px 80px 120px;background:{bg}">
          <div style="font-weight:600">{a.get("adset","&mdash;")}</div>
          <div style="color:{rc};font-weight:700">{roas}x</div>
          <div>{a.get("budget","&mdash;")}&euro;/j</div>
          <div style="color:#6B7280">{a.get("statut","&mdash;")}</div>
          <div><span class="badge {'badge-green' if roas>=2.5 else 'badge-red' if roas<1.5 else 'badge-amber'}">{('SCALER' if roas>=2.5 else 'COUPER' if roas<1.5 else 'SURVEILLER')}</span></div>
        </div>"""

    if not adset_rows:
        adset_rows = '<div style="padding:20px;text-align:center;color:#6B7280;font-size:13px">Aucune donn&eacute;e adset &mdash; disponible apr&egrave;s connexion Meta MCP</div>'

    rec_html = ""
    for r in budget_recs[:3]:
        priority_color = "#DC2626" if r.get("priorite") == "haute" else "#D97706"
        rec_html += f"""
        <div style="padding:12px 20px;border-bottom:1px solid #F9FAFB;display:flex;gap:12px;align-items:flex-start">
          <div style="width:6px;height:6px;border-radius:50%;background:{priority_color};margin-top:5px;flex-shrink:0"></div>
          <div>
            <div style="font-weight:600;font-size:14px;margin-bottom:2px">{r.get("action","&mdash;")}</div>
            <div style="font-size:12px;color:#6B7280">{r.get("raison","&mdash;")} &middot; {r.get("comment","&mdash;")}</div>
          </div>
          <div style="font-size:12px;color:#16A34A;font-weight:600;white-space:nowrap;margin-left:auto">{r.get("impact_estime","")}</div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Elva &mdash; Mes Ads</title>{style()}</head>
<body>
{nav("ads.html")}
<div class="page-header">
  <h1>Mes Ads</h1>
  <div style="display:flex;gap:8px;font-size:12px">
    <span class="badge badge-green">SCALER = ROAS &ge; 2.5x &middot; 5j+</span>
    <span class="badge badge-amber">GARDER = ROAS &ge; 2.0x</span>
    <span class="badge badge-red">COUPER = ROAS &lt; 1.5x &middot; 3j+</span>
  </div>
</div>
<div class="page-body">

  {'<div class="card" style="margin-bottom:16px"><div class="card-header"><h3>&#x1F4B0; Recommandations budget</h3></div>' + rec_html + '</div>' if rec_html else ''}

  <div class="card" style="margin-bottom:16px">
    <div class="card-header"><h3>Adsets</h3></div>
    <div class="table-row thead" style="grid-template-columns:2fr 80px 80px 80px 120px">
      <div>Adset</div><div>ROAS</div><div>Budget</div><div>Statut</div><div>Action</div>
    </div>
    {adset_rows}
  </div>

  <div class="card">
    <div class="card-header"><h3>Cr&eacute;atifs actifs</h3></div>
    <div class="table-row thead" style="grid-template-columns:2fr 80px 80px 80px 80px 120px">
      <div>Cr&eacute;atif</div><div>ROAS</div><div>CPM</div><div>Dur&eacute;e</div><div>Spend</div><div>D&eacute;cision</div>
    </div>
    {creatif_rows}
  </div>
</div>
</body></html>"""

    (DASHBOARD_DIR / "ads.html").write_text(html)
    print("OK ads.html generated")


# ─── PAGE 4 : CONCURRENTS ─────────────────────────────────────────────────────

def generate_concurrents(spy):
    winneuses = spy.get("winneuses", []) or []
    top = spy.get("top_winneuse", {}) or {}

    cards_html = ""
    for w in winneuses:
        score = w.get("hook_score", "&mdash;")
        score_color = "#16A34A" if isinstance(score, (int, float)) and score >= 75 else "#D97706" if isinstance(score, (int, float)) and score >= 60 else "#DC2626"
        format_badge = {"lip sync": "badge-blue", "temoignage": "badge-green", "lifestyle": "badge-amber", "produit": "badge-orange"}.get(w.get("format", "").lower(), "badge-orange")
        cards_html += f"""
        <div class="card" style="margin-bottom:12px">
          <div style="padding:16px 20px">
            <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:10px">
              <div>
                <div style="font-weight:700;font-size:16px">{w.get("marque","&mdash;")}</div>
                <div style="font-size:12px;color:#6B7280;margin-top:2px">Active {w.get("jours_actif","&mdash;")} jours &middot; <span class="badge {format_badge}" style="font-size:10px">{w.get("format","&mdash;")}</span></div>
              </div>
              {'<div style="text-align:center"><div style="font-size:22px;font-weight:800;color:' + score_color + '">' + str(score) + '</div><div style="font-size:10px;color:#6B7280">hook score</div></div>' if score != "&mdash;" else ''}
            </div>
            <div style="background:#F9FAFB;border-radius:8px;padding:10px 14px;margin-bottom:10px;font-size:13px;font-style:italic;color:#374151">
              &ldquo;{w.get("hook","&mdash;")}&rdquo;
            </div>
            <div style="font-size:12px">
              <span style="color:#F97316;font-weight:600">Angle :</span> <span style="color:#374151">{w.get("angle","&mdash;")}</span>
              <span style="margin-left:12px;color:#F97316;font-weight:600">&#x1F4A1; Le&ccedil;on :</span> <span style="color:#374151">{w.get("lecon","&mdash;")}</span>
            </div>
          </div>
        </div>"""

    if not cards_html:
        cards_html = '<div style="padding:40px;text-align:center;color:#6B7280">Aucune donn&eacute;e concurrente &mdash; disponible apr&egrave;s le premier run des agents</div>'

    top_html = ""
    if top:
        score = top.get("hook_score", "&mdash;")
        top_html = f"""
        <div style="background:linear-gradient(135deg,#FFF7ED,#FEF3C7);border:2px solid #F97316;border-radius:12px;padding:20px;margin-bottom:16px">
          <div style="font-size:11px;font-weight:700;color:#F97316;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px">&#x1F3C6; Top winneuse cette semaine</div>
          <div style="display:flex;align-items:flex-start;gap:16px">
            <div style="flex:1">
              <div style="font-weight:700;font-size:18px">{top.get("marque","&mdash;")}</div>
              <div style="font-size:12px;color:#6B7280;margin:4px 0 8px">{top.get("jours_actif","&mdash;")} jours actif</div>
              <div style="font-size:14px;font-style:italic;color:#374151;margin-bottom:8px">&ldquo;{top.get("hook","&mdash;")}&rdquo;</div>
              <div style="font-size:13px;color:#374151"><span style="color:#F97316;font-weight:600">Le&ccedil;on cl&eacute; :</span> {top.get("lecon","&mdash;")}</div>
            </div>
            <div style="text-align:center;flex-shrink:0">
              <div style="font-size:36px;font-weight:900;color:#F97316">{score}</div>
              <div style="font-size:11px;color:#6B7280">hook score</div>
            </div>
          </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Elva &mdash; Concurrents</title>{style()}</head>
<body>
{nav("concurrents.html")}
<div class="page-header">
  <h1>Analyse Concurrents</h1>
  <div style="font-size:13px;color:#6B7280">Ads actives 30j+ &middot; Meta Ad Library</div>
</div>
<div class="page-body">
  {top_html}
  <h3 style="font-size:14px;font-weight:600;color:#374151;margin-bottom:12px">Toutes les winneuses d&eacute;tect&eacute;es</h3>
  {cards_html}
</div>
</body></html>"""

    (DASHBOARD_DIR / "concurrents.html").write_text(html)
    print("OK concurrents.html generated")


# ─── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    archive_report()
    report = load_json(REPORT_PATH)
    performance = load_json(PERFORMANCE_PATH)
    spy = load_json(SPY_PATH)
    budget = load_json(BUDGET_PATH)
    history = load_history()

    generate_index(report)
    generate_analytics(report, history)
    generate_ads(performance, budget)
    generate_concurrents(spy)

    print(f"Dashboard complete: {len(history)} reports in history")
