# Elva Agent Team — Plan 2 : Les 6 Agents

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Créer les 6 agents spécialisés + l'orchestrateur qui les coordonne et génère un fichier JSON de données pour le dashboard.

**Architecture:** Chaque agent est un fichier prompt Markdown + un appel `claude -p` en lecture seule. L'orchestrateur `run_daily.sh` les exécute en séquence et collecte les outputs JSON dans `agents/outputs/`.

**Tech Stack:** Claude Code CLI (`claude`), Bash, MCPs configurés en Plan 1, jq (parsing JSON)

**Prérequis :** Plan 1 complété — tous les MCPs fonctionnels.

---

## Structure de fichiers

```
E-commerce/
├── agents/
│   ├── prompts/
│   │   ├── 01-spy-concurrent.md
│   │   ├── 02-performance.md
│   │   ├── 03-hook-virality.md
│   │   ├── 04-budget-optimizer.md
│   │   ├── 05-brief-creatif.md
│   │   └── 06-media-buyer.md
│   └── outputs/               ← gitignored, générés à l'exécution
│       ├── spy.json
│       ├── performance.json
│       ├── hook.json
│       ├── budget.json
│       ├── brief.json
│       └── report.json
└── scripts/
    └── run_daily.sh
```

---

### Task 1 : Agent Spy Concurrent

**Files:**
- Create: `agents/prompts/01-spy-concurrent.md`

- [ ] **Step 1 : Créer le prompt du Spy Concurrent**

Créer `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/agents/prompts/01-spy-concurrent.md` :

````markdown
# Spy Concurrent — Elva Lingerie

Tu es un expert en veille publicitaire pour une marque de lingerie DTC française (Elva Lingerie).

## Objectif
Trouver les publicités les plus performantes de nos concurrents lingerie sur Meta.

## Concurrents à surveiller
Recherche les publicités actives pour ces types de marques :
- Marques lingerie DTC françaises (Etam, Ysé, Livy, Maaree)
- Marques lingerie DTC européennes (Hunkemöller, Sloggi)
- Petites marques DTC lingerie avec fort engagement

## Instructions
1. Utilise la Meta Ad Library API pour rechercher les publicités dans la catégorie lingerie/sous-vêtements
2. Filtre : pays France, actives depuis au moins 30 jours (= rentables prouvées)
3. Pour chaque publicité trouvée, extrait :
   - Marque et URL
   - Durée d'activité (jours)
   - Format (vidéo/lip sync/statique/carousel)
   - Hook d'ouverture (les 3 premières secondes ou le texte d'accroche)
   - Angle marketing (confort, sensualité, prix, UGC, avant/après, etc.)
4. Classe par durée d'activité décroissante
5. Garde les 5 meilleures

## Output
Réponds UNIQUEMENT avec ce JSON valide (aucun texte avant ou après) :

```json
{
  "date": "YYYY-MM-DD",
  "winneuses": [
    {
      "rang": 1,
      "marque": "Nom de la marque",
      "jours_actif": 52,
      "format": "lip_sync_video",
      "hook": "Le seul soutien-gorge que je remets tous les jours...",
      "angle": "confort_quotidien",
      "url_ad_library": "https://www.facebook.com/ads/library/?id=XXXXX",
      "note": "Voix off intime, CTA fin naturel"
    }
  ]
}
```
````

- [ ] **Step 2 : Créer le dossier outputs**

```bash
mkdir -p /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/agents/outputs
```

- [ ] **Step 3 : Tester l'agent manuellement**

```bash
cd /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce
claude -p agents/prompts/01-spy-concurrent.md --output-format json > agents/outputs/spy.json
```

Expected : fichier `spy.json` avec 5 winneuses en JSON valide.

```bash
cat agents/outputs/spy.json | jq '.winneuses | length'
```
Expected : `5`

---

### Task 2 : Agent Analyse Performance

**Files:**
- Create: `agents/prompts/02-performance.md`

- [ ] **Step 1 : Créer le prompt Performance**

Créer `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/agents/prompts/02-performance.md` :

````markdown
# Analyse Performance — Elva Lingerie

Tu es un analyste data e-commerce pour Elva Lingerie.

## Objectif
Collecter les métriques de performance du jour sur Meta, Shopify et Pinterest.

## Instructions

### Meta Ads (via MCP Meta Ads)
Récupère pour aujourd'hui et les 7 derniers jours :
- ROAS par campagne et adset
- CPM par adset
- CTR par créatif
- Fréquence par adset
- Dépense totale
- Identifier : top créatif (ROAS le plus haut) et pire adset (ROAS le plus bas)

### Shopify (via MCP Shopify)
Récupère pour aujourd'hui :
- Revenus totaux
- Nombre de commandes
- Panier moyen (AOV)
- Taux de conversion
- Top 3 produits vendus (nom + revenus)

### Pinterest Ads (via MCP Pinterest)
Récupère pour aujourd'hui :
- Impressions totales
- CTR moyen
- Dépense totale
- Top pin par CTR

## Output
Réponds UNIQUEMENT avec ce JSON valide :

```json
{
  "date": "YYYY-MM-DD",
  "meta": {
    "roas_global": 1.8,
    "cpm_moyen": 14.2,
    "depense_totale": 48.0,
    "top_creatif": {
      "nom": "Soutien-gorge dentelle vidéo",
      "roas": 3.1,
      "cpm": 9.5,
      "ctr": 2.3
    },
    "adset_a_couper": {
      "nom": "Lookalike 2%",
      "roas": 0.6,
      "depense_jour": 18.0,
      "jours_consecutifs_mauvais": 3
    },
    "adset_a_scaler": {
      "nom": "Broad FR",
      "roas": 2.8,
      "budget_actuel": 12.0,
      "budget_recommande": 14.0
    }
  },
  "shopify": {
    "revenus": 86.0,
    "commandes": 4,
    "aov": 21.5,
    "taux_conversion": 1.8,
    "top_produits": [
      {"nom": "Soutien-gorge Dentelle Noir", "revenus": 43.0}
    ]
  },
  "pinterest": {
    "impressions": 12400,
    "ctr": 0.8,
    "depense": 4.2,
    "top_pin": "Shooting été 2026"
  }
}
```
````

- [ ] **Step 2 : Tester l'agent Performance**

```bash
cd /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce
claude -p agents/prompts/02-performance.md --output-format json > agents/outputs/performance.json
cat agents/outputs/performance.json | jq '.meta.roas_global'
```

Expected : un nombre (ton ROAS réel du jour).

---

### Task 3 : Agent Hook & Virality

**Files:**
- Create: `agents/prompts/03-hook-virality.md`

- [ ] **Step 1 : Créer le prompt Hook & Virality**

Créer `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/agents/prompts/03-hook-virality.md` :

````markdown
# Hook & Virality Analyst — Elva Lingerie

Tu es un expert en analyse créative publicitaire pour Elva Lingerie.

## Objectif
Analyser les créatifs vidéo actifs via Higgsfield pour obtenir leurs scores de performance créative.

## Instructions
1. Via le MCP Meta Ads, récupère les URLs des 3 créatifs vidéo actuellement actifs en campagne
2. Pour chaque vidéo, utilise le MCP Higgsfield pour obtenir :
   - Hook score (0-100) : qualité de l'accroche dans les 3 premières secondes
   - Hold rate (%) : % des spectateurs qui regardent jusqu'à la fin
   - Diagnostic textuel : pourquoi le score est-il bon ou mauvais ?
3. Compare avec les hooks des winneuses concurrentes (angle, ton, rythme)

## Output
Réponds UNIQUEMENT avec ce JSON valide :

```json
{
  "date": "YYYY-MM-DD",
  "creatifs": [
    {
      "nom": "Soutien-gorge dentelle vidéo",
      "hook_score": 71,
      "hold_rate": 42,
      "diagnostic": "Bon hook visuel mais perte d'attention à 4 secondes. Le produit apparaît trop tard.",
      "recommandation": "Montrer le produit dans les 2 premières secondes"
    }
  ],
  "meilleur_hook_concurrent": {
    "score": 78,
    "angle": "confort_quotidien",
    "pattern": "Question rhétorique + démonstration immédiate du produit"
  }
}
```
````

- [ ] **Step 2 : Tester Hook & Virality**

```bash
cd /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce
claude -p agents/prompts/03-hook-virality.md --output-format json > agents/outputs/hook.json
cat agents/outputs/hook.json | jq '.creatifs[0].hook_score'
```

Expected : un entier entre 0 et 100.

---

### Task 4 : Agent Budget Optimizer

**Files:**
- Create: `agents/prompts/04-budget-optimizer.md`

- [ ] **Step 1 : Créer le prompt Budget Optimizer**

Créer `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/agents/prompts/04-budget-optimizer.md` :

````markdown
# Budget Optimizer — Elva Lingerie

Tu es un media buyer expert spécialisé en optimisation de budget Meta Ads.

## Données disponibles
Le fichier `agents/outputs/performance.json` contient les métriques du jour.

## Règles d'optimisation
- **Couper** : tout adset avec ROAS < 1.5 depuis 3 jours consécutifs
- **Scaler** : tout adset avec ROAS > 2.5 stable sur 5+ jours → augmenter budget de 20%
- **Tester** : si un adset a ROAS 1.5-2.5 → garder, surveiller
- **Budget total** : ne jamais dépasser 55€/jour Meta

## Instructions
1. Lis les données de performance du fichier JSON
2. Applique les règles ci-dessus
3. Génère 3 actions maximum, les plus impactantes en premier

## Output
Réponds UNIQUEMENT avec ce JSON valide :

```json
{
  "date": "YYYY-MM-DD",
  "budget_actuel": 50.0,
  "budget_recommande": 50.0,
  "actions": [
    {
      "priorite": 1,
      "type": "couper",
      "adset": "Lookalike 2%",
      "raison": "ROAS 0.6 depuis 3 jours. Perte de 18€/jour.",
      "impact_estime": "+18€/jour économisés",
      "instruction_exacte": "Dans Meta Ads Manager > Campagnes > [nom campagne] > Adsets > Lookalike 2% > Désactiver"
    },
    {
      "priorite": 2,
      "type": "scaler",
      "adset": "Broad FR",
      "raison": "ROAS 2.8 stable sur 5 jours. Prêt à scaler.",
      "impact_estime": "+20% de revenus potentiels sur cet adset",
      "instruction_exacte": "Dans Meta Ads Manager > ... > Budget journalier : 12€ → 14€"
    }
  ]
}
```
````

- [ ] **Step 2 : Tester Budget Optimizer**

```bash
cd /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce
claude -p agents/prompts/04-budget-optimizer.md --output-format json > agents/outputs/budget.json
cat agents/outputs/budget.json | jq '.actions | length'
```

Expected : 1, 2 ou 3.

---

### Task 5 : Agent Brief Créatif

**Files:**
- Create: `agents/prompts/05-brief-creatif.md`

- [ ] **Step 1 : Créer le prompt Brief Créatif**

Créer `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/agents/prompts/05-brief-creatif.md` :

````markdown
# Brief Créatif — Elva Lingerie

Tu es un creative strategist expert en contenu vidéo pour marques de lingerie DTC.

## Identité Elva Lingerie
- Ton : intimiste, confiant, naturel (pas vulgaire)
- Audience : femmes 25-40 ans, France
- Format privilégié : lip sync vidéo 9:16 vertical, 15-30 secondes
- Style : authentique, pas trop produit

## Données disponibles
- `agents/outputs/spy.json` : winneuses concurrentes avec leurs angles
- `agents/outputs/hook.json` : scores de tes créatifs actuels et gaps identifiés

## Instructions
1. Identifie l'angle concurrent le plus performant non encore exploité par Elva
2. Génère 1 brief lip sync actionnable pour cette semaine
3. Le hook doit être dans les 3 premières secondes, formulé en "je" (voix off)
4. Le script doit faire 15 secondes maximum (environ 40 mots)

## Output
Réponds UNIQUEMENT avec ce JSON valide :

```json
{
  "date": "YYYY-MM-DD",
  "semaine": 20,
  "brief": {
    "titre": "Brief #3 — Confort quotidien",
    "angle": "confort_quotidien",
    "inspiration": "Concurrent A (52 jours actif, hook score 78)",
    "hook_ouverture": "Le seul soutien-gorge que je remets tous les jours...",
    "script_complet": "Le seul soutien-gorge que je remets tous les jours. Depuis que j'ai découvert Elva, je ne supporte plus les autres. Le confort, la dentelle, et il tient toute la journée. Lien dans la bio.",
    "format": "9:16 vertical",
    "duree": "15 secondes",
    "elements_visuels": "Commencer avec le soutien-gorge à l'écran, montrer en train de le mettre, plan rapproché dentelle, sourire naturel",
    "cta": "Lien dans la bio",
    "notes_realisateur": "Voix naturelle, pas récitée. Fond neutre clair ou chambre. Pas de filtre excessif."
  }
}
```
````

- [ ] **Step 2 : Tester Brief Créatif**

```bash
cd /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce
claude -p agents/prompts/05-brief-creatif.md --output-format json > agents/outputs/brief.json
cat agents/outputs/brief.json | jq '.brief.hook_ouverture'
```

Expected : une phrase d'accroche en français.

---

### Task 6 : Agent Media Buyer Expert (synthèse finale)

**Files:**
- Create: `agents/prompts/06-media-buyer.md`

- [ ] **Step 1 : Créer le prompt Media Buyer Expert**

Créer `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/agents/prompts/06-media-buyer.md` :

````markdown
# Media Buyer Expert — Elva Lingerie

Tu es le meilleur media buyer e-commerce de France, spécialisé dans les marques lingerie DTC. Tu as 10 ans d'expérience sur Meta Ads. Tu es direct, concis, et tes recommandations sont toujours actionnables.

## Données disponibles (lire dans cet ordre)
1. `agents/outputs/performance.json` — métriques du jour
2. `agents/outputs/budget.json` — recommandations budget
3. `agents/outputs/spy.json` — winneuses concurrentes
4. `agents/outputs/hook.json` — scores créatifs
5. `agents/outputs/brief.json` — brief créatif de la semaine

## Instructions
1. Lis tous les fichiers JSON
2. Synthétise en un rapport de media buyer senior
3. Explique le "pourquoi" derrière chaque recommandation
4. Sois direct : si quelque chose ne va pas, dis-le clairement
5. Maximum 3 actions prioritaires

## Output
Réponds UNIQUEMENT avec ce JSON valide :

```json
{
  "date": "YYYY-MM-DD",
  "heure_rapport": "08:15",
  "verdict_global": "⚠️ ROAS sous la cible",
  "resume_executif": "Ton CPM élevé vient d'un créatif principal avec un hook score faible (71/100). Pendant ce temps, les concurrents exploitent l'angle confort avec des hooks à 78. La priorité : couper le budget gaspillé sur Lookalike 2% et tester l'angle confort cette semaine.",
  "kpis": {
    "roas": 1.8,
    "roas_cible": 2.5,
    "cpm": 14.2,
    "revenus": 86.0,
    "depense": 48.0
  },
  "alerte": {
    "active": true,
    "message": "Adset Lookalike 2% — ROAS 0.6 depuis 3 jours · 18€/jour gaspillés",
    "urgence": "haute"
  },
  "actions_prioritaires": [
    {
      "rang": 1,
      "action": "Couper l'adset Lookalike 2%",
      "pourquoi": "ROAS 0.6 depuis 3 jours = Meta dépense sans retour. 18€/jour économisés immédiatement.",
      "comment": "Meta Ads Manager > [Campagne] > Adsets > Lookalike 2% > Désactiver",
      "impact": "Économie 18€/jour, réallocation possible vers Broad FR",
      "tag": "urgent"
    },
    {
      "rang": 2,
      "action": "Scaler Broad FR de +20%",
      "pourquoi": "ROAS 2.8 stable sur 5 jours. Meta a trouvé une audience qui convertit.",
      "comment": "Meta Ads Manager > Broad FR > Budget journalier : 12€ → 14€",
      "impact": "+20% revenus potentiels sur cet adset",
      "tag": "opportunite"
    },
    {
      "rang": 3,
      "action": "Tourner le brief lip sync #3 cette semaine",
      "pourquoi": "Ton meilleur créatif a un hook score de 71. Les concurrents sont à 78 sur l'angle confort. Ce gap coûte du CPM.",
      "comment": "Voir brief dans le dashboard",
      "impact": "Potentiel -15% CPM si hook score > 75",
      "tag": "creatif"
    }
  ],
  "winneuse_semaine": {
    "marque": "Concurrent A",
    "jours_actif": 52,
    "hook": "Le seul soutien-gorge que je remets tous les jours...",
    "hook_score": 78,
    "angle": "confort_quotidien",
    "lecon": "Question rhétorique + démonstration immédiate"
  },
  "brief_semaine": {
    "titre": "Brief #3 — Confort quotidien",
    "hook": "Le seul soutien-gorge que je remets tous les jours...",
    "format": "9:16, 15s, lip sync",
    "cta": "Lien dans la bio"
  }
}
```
````

- [ ] **Step 2 : Tester Media Buyer Expert**

```bash
cd /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce
claude -p agents/prompts/06-media-buyer.md --output-format json > agents/outputs/report.json
cat agents/outputs/report.json | jq '.actions_prioritaires | length'
```

Expected : 3

---

### Task 7 : Orchestrateur run_daily.sh

**Files:**
- Create: `scripts/run_daily.sh`

- [ ] **Step 1 : Créer l'orchestrateur**

Créer `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/scripts/run_daily.sh` :

```bash
#!/bin/bash
set -e

ROOT="/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce"
OUTPUTS="$ROOT/agents/outputs"
PROMPTS="$ROOT/agents/prompts"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

echo "🚀 [$TIMESTAMP] Démarrage des agents Elva..."

# Charger les variables d'environnement
source "$ROOT/.env"

mkdir -p "$OUTPUTS"

echo "🔍 [1/6] Spy Concurrent..."
claude -p "$PROMPTS/01-spy-concurrent.md" --output-format json > "$OUTPUTS/spy.json"
echo "✅ spy.json généré"

echo "📈 [2/6] Analyse Performance..."
claude -p "$PROMPTS/02-performance.md" --output-format json > "$OUTPUTS/performance.json"
echo "✅ performance.json généré"

echo "🧠 [3/6] Hook & Virality..."
claude -p "$PROMPTS/03-hook-virality.md" --output-format json > "$OUTPUTS/hook.json"
echo "✅ hook.json généré"

echo "💰 [4/6] Budget Optimizer..."
claude -p "$PROMPTS/04-budget-optimizer.md" --output-format json > "$OUTPUTS/budget.json"
echo "✅ budget.json généré"

echo "✍️  [5/6] Brief Créatif..."
claude -p "$PROMPTS/05-brief-creatif.md" --output-format json > "$OUTPUTS/brief.json"
echo "✅ brief.json généré"

echo "🎯 [6/6] Media Buyer Expert..."
claude -p "$PROMPTS/06-media-buyer.md" --output-format json > "$OUTPUTS/report.json"
echo "✅ report.json généré"

echo "📊 Génération du dashboard..."
python3 "$ROOT/scripts/generate_dashboard.py"
echo "✅ dashboard/index.html généré"

echo "🚀 Push vers GitHub Pages..."
cd "$ROOT"
git add dashboard/index.html
git commit -m "dashboard: rapport du $(date '+%Y-%m-%d')"
git push origin main

echo "✅ [$TIMESTAMP] Rapport terminé. Dashboard mis à jour."
```

- [ ] **Step 2 : Rendre le script exécutable**

```bash
chmod +x /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/scripts/run_daily.sh
```

- [ ] **Step 3 : Commit agents et scripts**

```bash
cd /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce
git add agents/prompts/ scripts/
git commit -m "feat: add 6 agent prompts and daily orchestrator"
git push origin main
```

---

### Task 8 : Cron journalier 08h00

**Files:**
- Modify: crontab système

- [ ] **Step 1 : Configurer le cron**

```bash
crontab -e
```

Ajouter cette ligne :
```
0 8 * * * /bin/bash /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/scripts/run_daily.sh >> /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/logs/cron.log 2>&1
```

- [ ] **Step 2 : Créer le dossier logs**

```bash
mkdir -p /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/logs
echo "logs/" >> /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/.gitignore
```

- [ ] **Step 3 : Tester le cron manuellement**

```bash
/bin/bash /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/scripts/run_daily.sh
```

Expected : tous les agents tournent, `report.json` est généré, aucune erreur.

---

## Validation finale Plan 2

- [ ] Chaque agent tourne seul et génère un JSON valide
- [ ] `run_daily.sh` tourne sans erreur en bout en bout
- [ ] Les 6 fichiers JSON sont dans `agents/outputs/`
- [ ] Le cron est configuré (`crontab -l` le confirme)
