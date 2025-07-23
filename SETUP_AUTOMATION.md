# 🤖 Configuration de l'Automatisation du Profil

## 🔑 **Secrets à configurer dans GitHub**

Allez dans **Settings** → **Secrets and variables** → **Actions** de votre repository et ajoutez :

### 1. `GH_TOKEN`
- Valeur : Votre Personal Access Token GitHub
- Comment l'obtenir :
  1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
  2. Generate new token (classic)
  3. Sélectionnez : `repo`, `read:user`, `user:email`
  4. Copiez le token généré

### 2. `WAKATIME_API_KEY` (Optionnel)
- Valeur : Votre clé API WakaTime
- Comment l'obtenir :
  1. Inscrivez-vous sur [wakatime.com](https://wakatime.com)
  2. Installez l'extension WakaTime dans VS Code
  3. Allez dans Settings → API Key
  4. Copiez votre clé

### 3. `EMAIL`
- Valeur : Votre email GitHub
- Exemple : `farytale54@gmail.com`

## 🏷️ **Étiquetage de vos repositories**

Pour que le script catégorise correctement vos projets, ajoutez des **topics** :

### Topics suggérés :
- **EFREI :** `efrei-project`, `school-assignment`, `education`
- **Jeux :** `game-development`, `godot`, `phaser`, `unity`
- **Personnel :** `personal-project`, `portfolio`, `creative`
- **Pro :** `professional`, `client-work`, `freelance`

### Comment ajouter des topics :
1. Allez sur votre repository
2. Cliquez sur l'icône ⚙️ à côté de "About"
3. Ajoutez les topics appropriés
4. Sauvegardez

## 🚀 **Test manuel**

Pour tester le script localement :

```bash
# Installer les dépendances
pip install requests python-dateutil

# Définir les variables d'environnement
set GITHUB_TOKEN=votre_token_ici
set WAKATIME_API_KEY=votre_cle_wakatime_ici

# Exécuter le script
python scripts/update_readme.py
```

## ⚡ **Déclenchement manuel**

Pour forcer une mise à jour :
1. Allez dans **Actions** de votre repository
2. Cliquez sur "🤖 Update Profile README"
3. Cliquez sur "Run workflow"

## 🎯 **Résultat attendu**

Le script va :
- ✅ Compter automatiquement vos projets par catégorie
- ✅ Afficher vos stats de code WakaTime
- ✅ Créer des sections organisées
- ✅ Mettre à jour le badge de nombre total de projets
- ✅ Conserver votre snake animation et le reste de votre contenu

## 🚨 **Troubleshooting - Problèmes courants**

### ⏰ **Le workflow prend trop de temps (> 5 minutes)**

**Causes possibles :**
1. **🔑 Token invalide/expiré** → Le script fait des retry en boucle
2. **🌐 Problème d'API** → Rate limiting GitHub ou WakaTime
3. **🐛 Bug dans le script** → Exception non gérée
4. **📊 Trop de repositories** → Pagination infinie

**Solutions :**
1. **Vérifiez le log du workflow** :
   - Actions → Workflow en cours → Cliquez dessus
   - Regardez quelle étape bloque

2. **Annulez et relancez** :
   - Cliquez "Cancel workflow" si > 10 minutes
   - Vérifiez vos secrets GitHub
   - Relancez avec "Run workflow"

3. **Test en local d'abord** :
   ```bash
   # Test rapide sans WakaTime
   set GITHUB_TOKEN=votre_token
   python scripts/update_readme.py
   ```

### 🔧 **Durée normale attendue :**
- ✅ **1-3 minutes** → Normal
- ⚠️ **5-8 minutes** → Lent mais acceptable  
- 🚨 **> 10 minutes** → Problème à résoudre

### 🏃‍♂️ **Version rapide du script**

Si le problème persiste, utilisez cette version allégée :

```python
# Version rapide - skip WakaTime si timeout
def get_wakatime_stats_fast(self) -> str:
    if not self.wakatime_key:
        return "<!-- Wakatime: Configure API key for stats -->"
        
    try:
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        session = requests.Session()
        retry = Retry(total=2, backoff_factor=0.3)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        response = session.get(
            'https://wakatime.com/api/v1/users/current/stats/last_7_days',
            headers={'Authorization': f'Bearer {self.wakatime_key}'},
            timeout=10  # 10 secondes max
        )
        
        if response.status_code == 200:
            # ... traitement normal
            pass
        else:
            return "<!-- Wakatime: API temporarily unavailable -->"
            
    except Exception:
        return "<!-- Wakatime: Skipped due to timeout -->"
```

### 🎯 **Actions immédiates si > 15 minutes :**

1. **ANNULEZ** le workflow immédiatement
2. **Vérifiez** vos secrets (GH_TOKEN surtout)
3. **Testez** en local d'abord
4. **Relancez** avec un token frais

---
