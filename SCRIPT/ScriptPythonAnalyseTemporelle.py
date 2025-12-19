-- SCRIPT PYTHON pour l'analyse du fait (commandes livrées/ non livrées) par rapport au temps 

# ANALYSE Y EN FONCTION DE X - VERSION CORRIGÉE

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# ============================================
# 1. PAR PÉRIODE (id_temps) - VOTRE EXEMPLE
# ============================================

# Vérification des colonnes
print("Colonnes disponibles:", list(dataset.columns))

# Analyse par période SI id_temps présent
if 'id_temps' in dataset.columns:
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig1.suptitle('ANALYSE PAR PÉRIODE (id_temps)', fontweight='bold')
    
    # Group by id_temps
    par_temps = dataset.groupby('id_temps').agg({
        'nbr_commande_livrees': 'sum',
        'nbr_commande_non_livrees': 'sum'
    }).reset_index()
    
    # Graphique 1: Barres groupées
    x = range(len(par_temps))
    width = 0.35
    
    ax1.bar(x, par_temps['nbr_commande_livrees'], width, 
            label='Livrées', color='green', alpha=0.7)
    ax1.bar([i + width for i in x], par_temps['nbr_commande_non_livrees'], width,
            label='Non-livrées', color='red', alpha=0.7)
    
    ax1.set_xlabel('Période (id_temps)')
    ax1.set_ylabel('Nombre de commandes')
    ax1.set_title('Commandes livrées/non-livrées par période')
    ax1.set_xticks([i + width/2 for i in x])
    ax1.set_xticklabels(par_temps['id_temps'], rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Graphique 2: Taux de livraison par période
    par_temps['taux_livraison'] = (par_temps['nbr_commande_livrees'] / 
                                  (par_temps['nbr_commande_livrees'] + 
                                   par_temps['nbr_commande_non_livrees'])) * 100
    
    ax2.plot(par_temps['id_temps'], par_temps['taux_livraison'], 
             marker='o', linewidth=2, color='blue')
    ax2.set_xlabel('Période (id_temps)')
    ax2.set_ylabel('Taux de livraison (%)')
    ax2.set_title('Taux de livraison par période')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim([0, 100])
    
    plt.tight_layout()
    plt.show()

# ============================================
# 2. PAR CLIENT (SI JOINTURE DISPONIBLE)
# ============================================

# Pour analyser par client, on a besoin de CompanyName
# Si pas dans dataset, on utilise id_seqClient
if 'id_seqClient' in dataset.columns:
    fig2, ax = plt.subplots(figsize=(12, 6))
    
    par_client = dataset.groupby('id_seqClient').agg({
        'nbr_commande_livrees': 'sum',
        'nbr_commande_non_livrees': 'sum'
    }).nlargest(10, 'nbr_commande_livrees')  # Top 10 clients
    
    # Graphique barres empilées
    x_pos = range(len(par_client))
    
    ax.bar(x_pos, par_client['nbr_commande_livrees'], 
           label='Livrées', color='lightgreen', alpha=0.8)
    ax.bar(x_pos, par_client['nbr_commande_non_livrees'],
           bottom=par_client['nbr_commande_livrees'],
           label='Non-livrées', color='salmon', alpha=0.8)
    
    ax.set_xlabel('Client (id_seqClient)')
    ax.set_ylabel('Nombre de commandes')
    ax.set_title('Top 10 Clients - Commandes livrées/non-livrées')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(par_client.index, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.show()

# ============================================
# 3. PAR EMPLOYÉ (SI JOINTURE DISPONIBLE)
# ============================================

if 'id_seqEmployee' in dataset.columns:
    fig3, ax = plt.subplots(figsize=(12, 6))
    
    par_employe = dataset.groupby('id_seqEmployee').agg({
        'nbr_commande_livrees': 'sum',
        'nbr_commande_non_livrees': 'sum'
    })
    
    # Graphique scatter: livrées vs non-livrées
    ax.scatter(par_employe['nbr_commande_livrees'], 
               par_employe['nbr_commande_non_livrees'],
               s=100, alpha=0.6, color='purple')
    
    # Ajouter labels pour chaque point
    for idx, row in par_employe.iterrows():
        ax.annotate(f'Emp{idx}', 
                   (row['nbr_commande_livrees'], row['nbr_commande_non_livrees']),
                   fontsize=9)
    
    ax.set_xlabel('Commandes livrées')
    ax.set_ylabel('Commandes non-livrées')
    ax.set_title('Performance des employés')
    ax.grid(True, alpha=0.3)
    
    # Ligne de ratio idéal (45°)
    max_val = max(par_employe['nbr_commande_livrees'].max(),
                  par_employe['nbr_commande_non_livrees'].max())
    ax.plot([0, max_val], [0, max_val], 'r--', alpha=0.5, label='Ratio 1:1')
    ax.legend()
    
    plt.tight_layout()
    plt.show()

# ============================================
# 4. TABLEAU SYNTHÈSE
# ============================================

print("\n" + "="*60)
print("TABLEAU SYNTHÈSE - ANALYSE MULTIDIMENSIONNELLE")
print("="*60)

# Par période
if 'id_temps' in dataset.columns:
    print("\n1. PAR PÉRIODE:")
    print("-"*40)
    for _, row in par_temps.iterrows():
        total = row['nbr_commande_livrees'] + row['nbr_commande_non_livrees']
        print(f"Période {row['id_temps']}: {total} commandes totales")
        print(f"  → Livrées: {row['nbr_commande_livrees']} ({row['taux_livraison']:.1f}%)")
        print(f"  → Non-livrées: {row['nbr_commande_non_livrees']}")

# Par client
if 'id_seqClient' in dataset.columns:
    print("\n2. TOP 5 CLIENTS:")
    print("-"*40)
    top_clients = dataset.groupby('id_seqClient').agg({
        'nbr_commande_livrees': 'sum'
    }).nlargest(5, 'nbr_commande_livrees')
    
    for client_id, cmd_livrees in top_clients.iterrows():
        print(f"Client {client_id}: {cmd_livrees['nbr_commande_livrees']} commandes livrées")

print("\n" + "="*60)
print("ANALYSE TERMINÉE")
print("="*60)
