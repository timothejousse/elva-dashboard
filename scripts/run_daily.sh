#!/bin/bash
set -e

TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
DATE=$(date '+%Y-%m-%d')
BASE_DIR="/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce"

echo "🚀 [$TIMESTAMP] Démarrage des agents Elva..."

mkdir -p "$BASE_DIR/agents/outputs"
mkdir -p "$BASE_DIR/logs"

LOG_FILE="$BASE_DIR/logs/run_$DATE.log"
exec > >(tee -a "$LOG_FILE") 2>&1

# ─── 1/6 Spy Concurrent ───────────────────────────────────────────────────────
echo "🔍 [1/6] Spy Concurrent..."
claude --print --dangerously-skip-permissions \
  "$(cat "$BASE_DIR/agents/prompts/01-spy-concurrent.md")" \
  2>/dev/null | tail -1 > /dev/null
echo "✅ spy.json généré"

# ─── 2/6 Analyse Performance ─────────────────────────────────────────────────
echo "📈 [2/6] Analyse Performance..."
claude --print --dangerously-skip-permissions \
  "$(cat "$BASE_DIR/agents/prompts/02-analyse-performance.md")" \
  2>/dev/null | tail -1 > /dev/null
echo "✅ performance.json généré"

# ─── 3/6 Hook & Virality ─────────────────────────────────────────────────────
echo "🧠 [3/6] Hook & Virality..."
claude --print --dangerously-skip-permissions \
  "$(cat "$BASE_DIR/agents/prompts/03-hook-virality.md")" \
  2>/dev/null | tail -1 > /dev/null
echo "✅ hook.json généré"

# ─── 4/6 Budget Optimizer ────────────────────────────────────────────────────
echo "💰 [4/6] Budget Optimizer..."
claude --print --dangerously-skip-permissions \
  "$(cat "$BASE_DIR/agents/prompts/04-budget-optimizer.md")" \
  2>/dev/null | tail -1 > /dev/null
echo "✅ budget.json généré"

# ─── 5/6 Brief Créatif ───────────────────────────────────────────────────────
echo "✍️  [5/6] Brief Créatif..."
claude --print --dangerously-skip-permissions \
  "$(cat "$BASE_DIR/agents/prompts/05-brief-creatif.md")" \
  2>/dev/null | tail -1 > /dev/null
echo "✅ brief.json généré"

# ─── 6/6 Media Buyer Expert ──────────────────────────────────────────────────
echo "🎯 [6/6] Media Buyer Expert..."
claude --print --dangerously-skip-permissions \
  "$(cat "$BASE_DIR/agents/prompts/06-media-buyer.md")" \
  2>/dev/null | tail -1 > /dev/null
echo "✅ report.json généré"

# ─── Dashboard ───────────────────────────────────────────────────────────────
echo "📊 Génération du dashboard..."
python3 "$BASE_DIR/scripts/generate_dashboard.py"
echo "✅ dashboard/index.html généré"

# ─── Push GitHub Pages ───────────────────────────────────────────────────────
echo "🚀 Push vers GitHub Pages..."
cd "$BASE_DIR"
git add dashboard/index.html
git commit -m "chore: daily dashboard update $DATE" --allow-empty
git push origin main
echo "✅ [$TIMESTAMP] Rapport terminé. Dashboard mis à jour."
