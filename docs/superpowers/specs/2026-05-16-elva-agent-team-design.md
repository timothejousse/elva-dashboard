# Elva Lingerie — Agent Team Design
**Date :** 2026-05-16  
**Statut :** Approuvé  

---

## Contexte

Elva Lingerie (elva-lingerie.com) est une marque de lingerie DTC sur Shopify. Budget ads ~1 500€/mois (50€/jour) sur Meta (CBO broad) + Pinterest. Problème : CPM élevé, ROAS cible non atteint. Levier principal identifié : qualité et pertinence des créatifs.

L'objectif est de construire une team d'agents IA qui génère chaque matin un rapport actionnable. Le fondateur garde la main sur tous les changements dans Meta Ads Manager.

---

## Architecture : Hybrid Hub & Spoke

6 agents spécialisés + 5 connecteurs MCP + 1 dashboard web.

### Connecteurs MCP

| Connecteur | Source | Usage |
|---|---|---|
| Meta Ads MCP | Officiel Meta (29 avril 2026) | Campagnes, adsets, CPM, ROAS, budgets |
| Shopify MCP | Officiel Shopify (9 avril 2026) | Ventes, conversion, AOV, top produits |
| Pinterest MCP | InsightfulPipe (gratuit) | Campagnes, pins, CTR |
| Meta Ad Library API | Meta (gratuit) | Surveillance ads concurrents |
| Higgsfield MCP | Higgsfield (9 mai 2026) | Hook score, hold rate, brain heatmap |

### Les 6 Agents

**1. Spy Concurrent**
- Surveille 10-15 marques lingerie via Meta Ad Library API
- Repère les ads actives depuis 30j+ (= rentables prouvées)
- Classe par format, hook d'ouverture, angle marketing
- Output : top 5 winneuses de la semaine avec analyse

**2. Analyse Performance**
- Pull Meta : CPM, CTR, ROAS, fréquence par adset/créatif
- Pull Shopify : revenus, taux conversion, AOV, top produits
- Pull Pinterest : impressions, CTR, coût par clic
- Identifie top créatifs vs créatifs à couper

**3. Hook & Virality**
- Analyse créatifs actifs + winneuses concurrents via Higgsfield
- Output : hook score (0-100), hold rate, brain heatmap par créatif
- Diagnostic textuel ("hook trop mou", "perte attention à 3s")

**4. Budget Optimizer**
- Basé sur les données de Analyse Performance
- Recommande : où couper (ROAS < seuil), où scaler (ROAS stable)
- Toujours en mode recommandation — jamais d'action directe

**5. Brief Créatif**
- Combine winneuses Spy + angles qui convertissent + identité Elva
- Génère 2-3 briefs lip sync par semaine
- Format : hook d'ouverture, script 15s/30s, format 9:16, CTA

**6. Media Buyer Expert**
- Cerveau de synthèse finale
- Raisonne comme un media buyer senior
- Produit le rapport journalier avec 3 actions claires priorisées

### Flux quotidien

```
08:00  Spy Concurrent + Analyse Perf + Hook & Virality (parallèle)
08:10  Budget Optimizer + Brief Créatif
08:15  Media Buyer Expert → rapport final
08:15  Push dashboard → GitHub Pages
```

---

## Dashboard Web

- **Style :** Glassmorphisme Apple, fond blanc, accent orange #F97316
- **Hébergement :** GitHub Pages (gratuit, accessible partout)
- **Mise à jour :** automatique chaque matin par les agents

### Sections du dashboard

1. **KPIs** : ROAS, CPM, Revenus Shopify, Dépense Meta
2. **Alerte** : notification si ROAS < seuil ou CPM en hausse
3. **Actions du jour** : 3 actions prioritaires avec cases à cocher
4. **Winneuses concurrentes** : top 2 avec hook score
5. **Brief créatif** : hook + format + CTA de la semaine

---

## Principes clés

- **Lecture seule** : les agents ne modifient jamais les comptes Meta/Shopify
- **Advisory** : toutes les recommandations sont validées par le fondateur
- **Journalier** : rapport automatique chaque matin à 08h15
- **Gratuit** : hébergement GitHub Pages, MCPs officiels gratuits

---

## Stack technique

- Claude Code + Superpowers skills
- MCPs : Meta Ads, Shopify, Pinterest, Ad Library, Higgsfield
- Dashboard : HTML/CSS statique généré par les agents
- Déploiement : GitHub Actions → GitHub Pages
- Scheduling : cron via Claude Code
