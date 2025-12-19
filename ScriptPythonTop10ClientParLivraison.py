# PAGE CLIENTS - TOP 10 CLIENTS SIMPLIFIÉ
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("="*50)
print("ANALYSE TOP 10 CLIENTS")
print("="*50)

# Diagnostic
print(f"📊 Données reçues: {len(dataset)} lignes")
print(f"🔤 Colonnes: {list(dataset.columns)}")

if 'id_seqClient' not in dataset.columns:
    print("❌ ERREUR: Colonne 'id_seqClient' manquante!")
    print("👉 Glissez 'id_seqClient' depuis la table 'fait'")
    plt.text(0.5, 0.5, "Colonne id_seqClient manquante!\nGlissez-la depuis 'fait'", 
             ha='center', va='center', fontsize=12)
    plt.show()
else:
    # 1. Calcul Top 10
    client_stats = dataset.groupby('id_seqClient').agg({
        'nbr_commande_livrees': 'sum',
        'nbr_commande_non_livrees': 'sum'
    })
    
    client_stats['total'] = client_stats['nbr_commande_livrees'] + client_stats['nbr_commande_non_livrees']
    client_stats['taux'] = (client_stats['nbr_commande_livrees'] / client_stats['total']) * 100
    
    top10 = client_stats.nlargest(10, 'total')
    
    print(f"\n🏆 TOP 10 CLIENTS SUR {len(client_stats)} CLIENTS:")
    for idx, (client_id, row) in enumerate(top10.iterrows(), 1):
        print(f"{idx:2}. Client {client_id}: {row['total']:3} cmd | " +
              f"Taux: {row['taux']:5.1f}%")
    
    # 2. Visualisation
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Graphique 1: Barres empilées
    x_pos = range(len(top10))
    bar_width = 0.6
    
    bars1 = ax1.bar(x_pos, top10['nbr_commande_livrees'], bar_width,
                    color='#2ecc71', alpha=0.8, label='Livrées')
    bars2 = ax1.bar(x_pos, top10['nbr_commande_non_livrees'], bar_width,
                    bottom=top10['nbr_commande_livrees'],
                    color='#e74c3c', alpha=0.8, label='Non-livrées')
    
    ax1.set_xlabel('Clients')
    ax1.set_ylabel('Nombre de commandes')
    ax1.set_title('TOP 10 CLIENTS - VOLUME DE COMMANDES', fontweight='bold')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels([f'C{id}' for id in top10.index], rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Ajouter les totaux sur les barres
    for i, (_, row) in enumerate(top10.iterrows()):
        total = row['total']
        ax1.text(i, total + 0.5, str(total), 
                ha='center', va='bottom', fontweight='bold')
    
    # Graphique 2: Taux de livraison + Score
    ax2_taux = ax2
    bars_taux = ax2_taux.bar(x_pos, top10['taux'], bar_width,
                            color='#3498db', alpha=0.7, label='Taux livraison')
    
    ax2_taux.set_xlabel('Clients')
    ax2_taux.set_ylabel('Taux de livraison (%)', color='#3498db')
    ax2_taux.set_title('TOP 10 CLIENTS - PERFORMANCE', fontweight='bold')
    ax2_taux.set_xticks(x_pos)
    ax2_taux.set_xticklabels([f'C{id}' for id in top10.index], rotation=45)
    ax2_taux.set_ylim([0, 105])
    ax2_taux.tick_params(axis='y', labelcolor='#3498db')
    ax2_taux.grid(True, alpha=0.3, axis='y')
    
    # Ajouter les valeurs de taux
    for i, taux in enumerate(top10['taux']):
        ax2_taux.text(i, taux + 2, f'{taux:.1f}%', 
                     ha='center', va='bottom', fontweight='bold', color='#3498db')
    
    # Second axe pour le volume (transparent)
    ax2_vol = ax2_taux.twinx()
    ax2_vol.plot(x_pos, top10['total'], 'o-', color='#e67e22', 
                linewidth=2, markersize=8, label='Volume total')
    ax2_vol.set_ylabel('Volume total (commandes)', color='#e67e22')
    ax2_vol.tick_params(axis='y', labelcolor='#e67e22')
    
    # Légende combinée
    lines_labels = [bars_taux, ax2_vol.lines[0]]
    labels = ['Taux livraison (%)', 'Volume total']
    ax2_taux.legend(lines_labels, labels, loc='upper right')
    
    plt.suptitle('ANALYSE COMPARATIVE DES TOP 10 CLIENTS', 
                fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.show()
    
    print("\n✅ Analyse clients terminée avec succès!")