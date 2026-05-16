# Elva Agent Team — Plan 1 : Infrastructure

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mettre en place le repo Git, GitHub Pages, et configurer les 4 MCPs (Meta Ads, Shopify, Pinterest, Higgsfield) pour que les agents puissent lire les données réelles.

**Architecture:** Repo Git dans `E-commerce/`, GitHub Pages sur la branche `gh-pages`, MCPs configurés dans `.claude/settings.json` avec credentials stockés dans des variables d'environnement.

**Tech Stack:** Git, GitHub CLI, Claude Code MCPs, zsh

---

## Structure de fichiers

```
E-commerce/
├── .claude/
│   └── settings.json          ← config MCPs (à créer)
├── agents/
│   ├── prompts/               ← prompts des agents (Plan 2)
│   └── outputs/               ← JSON outputs (Plan 2)
├── dashboard/
│   └── index.html             ← dashboard généré (Plan 3)
├── scripts/
│   └── run_daily.sh           ← orchestrateur (Plan 2)
├── docs/
│   └── superpowers/
│       ├── specs/
│       └── plans/
└── .env.example               ← template credentials
```

---

### Task 1 : Initialiser le repo Git et GitHub Pages

**Files:**
- Create: `E-commerce/.gitignore`
- Create: `E-commerce/.env.example`
- Create: `E-commerce/dashboard/index.html` (placeholder)

- [ ] **Step 1 : Initialiser Git dans E-commerce/**

```bash
cd /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce
git init
git branch -M main
```

Expected: `Initialized empty Git repository in .../E-commerce/.git/`

- [ ] **Step 2 : Créer .gitignore**

Créer le fichier `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/.gitignore` :

```
.env
agents/outputs/*.json
.superpowers/
node_modules/
*.log
```

- [ ] **Step 3 : Créer .env.example**

Créer `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/.env.example` :

```bash
# Meta Ads MCP — obtenir sur https://developers.facebook.com/apps
META_ACCESS_TOKEN=your_meta_access_token_here
META_AD_ACCOUNT_ID=act_XXXXXXXXX

# Shopify MCP — obtenir dans Shopify Admin > Apps > API
SHOPIFY_STORE_URL=elva-lingerie.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_XXXXXXXXX

# Pinterest MCP
PINTEREST_ACCESS_TOKEN=your_pinterest_token_here

# Higgsfield MCP
HIGGSFIELD_API_KEY=your_higgsfield_key_here

# GitHub (pour le déploiement dashboard)
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=ton-username/elva-dashboard
```

- [ ] **Step 4 : Créer le placeholder dashboard**

Créer `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/dashboard/index.html` :

```html
<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><title>Elva Dashboard</title></head>
<body>
  <h1>Elva Dashboard — En cours de configuration</h1>
  <p>Le dashboard sera disponible après la première exécution des agents.</p>
</body>
</html>
```

- [ ] **Step 5 : Premier commit**

```bash
cd /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce
git add .gitignore .env.example dashboard/index.html docs/
git commit -m "feat: init elva agent team project structure"
```

Expected: `[main (root-commit) xxxxxxx] feat: init elva agent team project structure`

---

### Task 2 : Créer le repo GitHub et configurer GitHub Pages

**Files:**
- Aucun fichier local — opération GitHub CLI

- [ ] **Step 1 : Créer le repo GitHub (public pour GitHub Pages gratuit)**

```bash
cd /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce
gh repo create elva-dashboard --public --source=. --remote=origin --push
```

Si `gh` n'est pas installé :
```bash
brew install gh
gh auth login
```

- [ ] **Step 2 : Créer la branche gh-pages**

```bash
cd /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce
git checkout --orphan gh-pages
git rm -rf .
cp dashboard/index.html index.html
git add index.html
git commit -m "init: github pages placeholder"
git push origin gh-pages
git checkout main
```

- [ ] **Step 3 : Activer GitHub Pages dans les settings**

```bash
gh api repos/:owner/elva-dashboard/pages \
  --method POST \
  --field source='{"branch":"gh-pages","path":"/"}'
```

Expected output :
```json
{"url": "https://ton-username.github.io/elva-dashboard/", ...}
```

- [ ] **Step 4 : Vérifier que la page est accessible**

Ouvrir dans le navigateur : `https://ton-username.github.io/elva-dashboard/`
Expected : page "En cours de configuration" visible.

- [ ] **Step 5 : Créer le workflow GitHub Actions pour le déploiement auto**

Créer `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/.github/workflows/deploy-dashboard.yml` :

```yaml
name: Deploy Dashboard

on:
  push:
    branches: [main]
    paths: [dashboard/index.html]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dashboard
          publish_branch: gh-pages
```

```bash
git add .github/
git commit -m "ci: add github pages auto-deploy workflow"
git push origin main
```

---

### Task 3 : Configurer le MCP Meta Ads (officiel)

**Files:**
- Create/Modify: `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/.claude/settings.json`

- [ ] **Step 1 : Obtenir les credentials Meta**

1. Aller sur https://developers.facebook.com/apps
2. Créer une app ou utiliser une existante
3. Ajouter le produit "Marketing API"
4. Générer un User Access Token avec les permissions : `ads_read`, `ads_management`
5. Récupérer l'Ad Account ID depuis Meta Ads Manager (format : `act_XXXXXXXXX`)

- [ ] **Step 2 : Créer le fichier .env local**

```bash
cd /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce
cp .env.example .env
```

Éditer `.env` avec les vraies valeurs Meta :
```bash
META_ACCESS_TOKEN=EAAxxxxxxx...
META_AD_ACCOUNT_ID=act_123456789
```

- [ ] **Step 3 : Ajouter le MCP Meta Ads dans les settings Claude Code**

Créer/modifier `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/.claude/settings.json` :

```json
{
  "mcpServers": {
    "meta-ads": {
      "command": "npx",
      "args": ["-y", "@pipeboard/meta-ads-mcp"],
      "env": {
        "META_ACCESS_TOKEN": "${META_ACCESS_TOKEN}",
        "META_AD_ACCOUNT_ID": "${META_AD_ACCOUNT_ID}"
      }
    }
  }
}
```

- [ ] **Step 4 : Tester la connexion Meta MCP**

Dans Claude Code, lancer une nouvelle session dans le dossier E-commerce et tester :

```
Liste mes campagnes Meta Ads actives avec leur budget et ROAS
```

Expected : Claude liste les campagnes réelles depuis ton compte Meta.

---

### Task 4 : Configurer le MCP Shopify

**Files:**
- Modify: `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/.claude/settings.json`

- [ ] **Step 1 : Obtenir le token Shopify Admin API**

1. Shopify Admin → Settings → Apps and sales channels → Develop apps
2. Create an app → "Elva Agent"
3. Configure Admin API scopes : `read_orders`, `read_products`, `read_analytics`, `read_reports`
4. Install app → copier le "Admin API access token" (shpat_...)

- [ ] **Step 2 : Ajouter dans .env**

```bash
SHOPIFY_STORE_URL=elva-lingerie.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_XXXXXXXXX
```

- [ ] **Step 3 : Installer le MCP Shopify officiel**

```bash
claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest
```

Ou manuellement dans `.claude/settings.json` :

```json
{
  "mcpServers": {
    "meta-ads": { "...": "..." },
    "shopify": {
      "command": "npx",
      "args": ["-y", "@shopify/dev-mcp@latest"],
      "env": {
        "SHOPIFY_STORE_URL": "${SHOPIFY_STORE_URL}",
        "SHOPIFY_ACCESS_TOKEN": "${SHOPIFY_ACCESS_TOKEN}"
      }
    }
  }
}
```

- [ ] **Step 4 : Tester la connexion Shopify MCP**

Dans Claude Code :

```
Quels sont mes 5 produits les plus vendus cette semaine sur Shopify avec leur revenu total ?
```

Expected : Claude retourne les vrais produits et chiffres de ton store.

---

### Task 5 : Configurer le MCP Pinterest

**Files:**
- Modify: `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/.claude/settings.json`

- [ ] **Step 1 : Obtenir le token Pinterest**

1. Aller sur https://developers.pinterest.com/apps/
2. Créer une app → demander accès à `ads:read`
3. Générer un access token OAuth
4. Récupérer l'Ad Account ID dans Pinterest Ads Manager

- [ ] **Step 2 : Ajouter dans .env**

```bash
PINTEREST_ACCESS_TOKEN=your_token
PINTEREST_AD_ACCOUNT_ID=549755813XXX
```

- [ ] **Step 3 : Ajouter Pinterest MCP (InsightfulPipe)**

Dans `.claude/settings.json` :

```json
{
  "mcpServers": {
    "meta-ads": { "...": "..." },
    "shopify": { "...": "..." },
    "pinterest": {
      "command": "npx",
      "args": ["-y", "@insightfulpipe/pinterest-ads-mcp"],
      "env": {
        "PINTEREST_ACCESS_TOKEN": "${PINTEREST_ACCESS_TOKEN}",
        "PINTEREST_AD_ACCOUNT_ID": "${PINTEREST_AD_ACCOUNT_ID}"
      }
    }
  }
}
```

- [ ] **Step 4 : Tester Pinterest MCP**

Dans Claude Code :

```
Quelles sont mes campagnes Pinterest actives avec leur CTR et dépense de cette semaine ?
```

Expected : données réelles Pinterest.

---

### Task 6 : Configurer le MCP Higgsfield (Hook Score)

**Files:**
- Modify: `/Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce/.claude/settings.json`

- [ ] **Step 1 : Créer un compte Higgsfield**

Aller sur https://higgsfield.ai → créer un compte → récupérer l'API key dans les settings.

- [ ] **Step 2 : Ajouter dans .env**

```bash
HIGGSFIELD_API_KEY=hf_XXXXXXXXX
```

- [ ] **Step 3 : Ajouter Higgsfield MCP**

Dans `.claude/settings.json` :

```json
{
  "mcpServers": {
    "meta-ads": { "...": "..." },
    "shopify": { "...": "..." },
    "pinterest": { "...": "..." },
    "higgsfield": {
      "command": "npx",
      "args": ["-y", "@higgsfield/mcp-server"],
      "env": {
        "HIGGSFIELD_API_KEY": "${HIGGSFIELD_API_KEY}"
      }
    }
  }
}
```

- [ ] **Step 4 : Tester Higgsfield**

Dans Claude Code, soumettre une vidéo courte (15s) de test :

```
Analyse cette vidéo et donne-moi le hook score, le hold rate et le brain heatmap : [URL vidéo]
```

Expected : score entre 0-100, hold rate en %, description heatmap.

- [ ] **Step 5 : Commit final infrastructure**

```bash
cd /Users/timothe.jousse/Documents/SUPERPOUVOIRS/E-commerce
git add .claude/settings.json .github/ agents/ scripts/ dashboard/
git commit -m "feat: configure all MCPs and project structure"
git push origin main
```

---

## Validation finale Plan 1

Checklist avant de passer au Plan 2 :

- [ ] `git status` → repo propre sur main
- [ ] GitHub Pages accessible à l'URL publique
- [ ] Meta MCP : liste les campagnes réelles
- [ ] Shopify MCP : liste les vrais produits/ventes
- [ ] Pinterest MCP : liste les campagnes actives
- [ ] Higgsfield MCP : retourne un hook score
- [ ] `.env` local rempli, `.env.example` commité (sans valeurs)
