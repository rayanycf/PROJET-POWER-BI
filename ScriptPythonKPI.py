import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("="*60)
print("DASHBOARD KPI - ANALYSE DES COMMANDES NORTHWIND")
print("="*60)

# Diagnostic initial
print(f"📊 Données reçues : {len(dataset)} lignes")
print(f"📋 Colonnes disponibles : {list(dataset.columns)}")

# ============================================
# 1. CALCUL DES KPI PRINCIPAUX
# ============================================
print("\n🧮 CALCUL DES INDICATEURS CLÉS...")

# KPI 1 : Taux de livraison global
total_livrees = dataset['nbr_commande_livrees'].sum()
total_non_livrees = dataset['nbr_commande_non_livrees'].sum()
total_commandes = total_livrees + total_non_livrees
taux_livraison = (total_livrees / total_commandes * 100) if total_commandes > 0 else 0

# KPI 2 : Distribution par statut
pourcentage_livrees = (total_livrees / total_commandes * 100) if total_commandes > 0 else 0
pourcentage_non_livrees = (total_non_livrees / total_commandes * 100) if total_commandes > 0 else 0

# KPI 3 : Si id_temps présent, tendance mensuelle
tendance_amelioration = "Stable"
if 'id_temps' in dataset.columns:
    mensuel = dataset.groupby('id_temps').agg({
        'nbr_commande_livrees': 'sum',
        'nbr_commande_non_livrees': 'sum'
    }).reset_index()
    if len(mensuel) > 1:
        premier_mois = (mensuel.iloc[0]['nbr_commande_livrees'] / 
                       (mensuel.iloc[0]['nbr_commande_livrees'] + 
                        mensuel.iloc[0]['nbr_commande_non_livrees']) * 100)
        dernier_mois = (mensuel.iloc[-1]['nbr_commande_livrees'] / 
                       (mensuel.iloc[-1]['nbr_commande_livrees'] + 
                        mensuel.iloc[-1]['nbr_commande_non_livrees']) * 100)
        if dernier_mois > premier_mois + 5:
            tendance_amelioration = "↗ Amélioration"
        elif dernier_mois < premier_mois - 5:
            tendance_amelioration = "↘ Baisse"
        else:
            tendance_amelioration = "➡ Stable"

# ============================================
# 2. CRÉATION DU DASHBOARD KPI
# ============================================
fig = plt.figure(figsize=(16, 10))
fig.suptitle('TABLEAU DE BORD KPI - PERFORMANCES COMMANDES', 
             fontsize=18, fontweight='bold', y=0.98)

# --------------------------
# GRAPHIQUE 1 : GAUGE TAUX DE LIVRAISON
# --------------------------
ax1 = plt.subplot(2, 3, 1)
ax1.set_title('TAUX DE LIVRAISON', fontweight='bold', fontsize=14)

# Création d'un gauge chart simplifié
angles = np.linspace(0, 180, 100)
ax1.fill_betweenx(angles, 0, 1, color='lightgray', alpha=0.3)
ax1.fill_betweenx(angles[:int(taux_livraison/100*len(angles))], 
                  0, 1, color='#2ecc71', alpha=0.7)

ax1.set_xlim(0, 1)
ax1.set_ylim(0, 180)
ax1.axis('off')

# Valeur au centre
ax1.text(0.5, 90, f'{taux_livraison:.1f}%', 
         ha='center', va='center', fontsize=32, fontweight='bold', color='#2ecc71')
ax1.text(0.5, 60, 'Objectif: >90%', ha='center', va='center', fontsize=10, color='gray')

# --------------------------
# GRAPHIQUE 2 : CAMEMBERT DISTRIBUTION
# --------------------------
ax2 = plt.subplot(2, 3, 2)
ax2.set_title('DISTRIBUTION DES COMMANDES', fontweight='bold', fontsize=14)

labels = ['Livrées', 'Non-livrées']
sizes = [total_livrees, total_non_livrees]
colors = ['#2ecc71', '#e74c3c']
explode = (0.05, 0)

wedges, texts, autotexts = ax2.pie(sizes, explode=explode, labels=labels, colors=colors,
                                   autopct='%1.1f%%', startangle=90, shadow=False)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

ax2.axis('equal')

# --------------------------
# GRAPHIQUE 3 : BARRES VOLUME TOTAL
# --------------------------
ax3 = plt.subplot(2, 3, 3)
ax3.set_title('VOLUME DE COMMANDES', fontweight='bold', fontsize=14)

categories = ['Total', 'Livrées', 'Non-livrées']
values = [total_commandes, total_livrees, total_non_livrees]
colors_bar = ['#3498db', '#2ecc71', '#e74c3c']

bars = ax3.bar(categories, values, color=colors_bar, alpha=0.8)
ax3.set_ylabel('Nombre de commandes')
ax3.grid(True, alpha=0.3, axis='y')

# Ajouter les valeurs sur les barres
for bar, value in zip(bars, values):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.02,
             f'{int(value)}', ha='center', va='bottom', fontweight='bold')

# --------------------------
# GRAPHIQUE 4 : CARTES KPI
# --------------------------
ax4 = plt.subplot(2, 3, 4)
ax4.axis('off')

# Création de "cartes" visuelles
card_data = [
    {'title': 'COMMANDES TOTALES', 'value': f'{int(total_commandes)}', 'color': '#3498db'},
    {'title': 'TAUX LIVRAISON', 'value': f'{taux_livraison:.1f}%', 'color': '#2ecc71'},
    {'title': 'TENDANCE', 'value': tendance_amelioration, 'color': '#9b59b6'}
]

for i, card in enumerate(card_data):
    y_pos = 0.7 - i * 0.3
    ax4.add_patch(plt.Rectangle((0.1, y_pos), 0.8, 0.25, 
                               color=card['color'], alpha=0.2, ec='black'))
    ax4.text(0.5, y_pos + 0.17, card['value'], 
             ha='center', va='center', fontsize=24, fontweight='bold', color=card['color'])
    ax4.text(0.5, y_pos + 0.07, card['title'], 
             ha='center', va='center', fontsize=11, color='gray')

# --------------------------
# GRAPHIQUE 5 : TABLEAU SYNTHÈSE
# --------------------------
ax5 = plt.subplot(2, 3, 5)
ax5.axis('off')

table_data = [
    ['KPI', 'Valeur', 'Statut'],
    ['Commandes totales', f'{int(total_commandes)}', '✅'],
    ['Taux livraison', f'{taux_livraison:.1f}%', '✅' if taux_livraison > 90 else '⚠️'],
    ['Commandes livrées', f'{int(total_livrees)}', '✅'],
    ['Commandes non-livrées', f'{int(total_non_livrees)}', '⚠️' if pourcentage_non_livrees > 10 else '✅'],
    ['Ratio livraison', f'1:{total_livrees/total_non_livrees:.1f}' if total_non_livrees > 0 else 'N/A', '✅']
]

table = ax5.table(cellText=table_data, cellLoc='center', 
                  colWidths=[0.3, 0.3, 0.1], loc='center')
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2)

# Colorer les cellules
for i in range(1, len(table_data)):
    if '⚠️' in table_data[i][2]:
        table[(i, 2)].set_facecolor('#f1c40f')
    elif '✅' in table_data[i][2]:
        table[(i, 2)].set_facecolor('#2ecc71')

# --------------------------
# GRAPHIQUE 6 : JAUGE SIMPLE
# --------------------------
ax6 = plt.subplot(2, 3, 6)
ax6.set_title('PERFORMANCE GLOBALE', fontweight='bold', fontsize=14)

# Score sur 10
score = min(10, taux_livraison / 10)
ax6.barh([0], [10], color='lightgray', alpha=0.3, height=0.5)
ax6.barh([0], [score], color='#9b59b6', alpha=0.7, height=0.5)
ax6.set_xlim(0, 10)
ax6.set_yticks([])
ax6.set_xlabel('Score /10')

ax6.text(score + 0.5, 0, f'{score:.1f}/10', 
         va='center', fontsize=16, fontweight='bold', color='#9b59b6')

# Légende du score
if score >= 9:
    evaluation = "EXCELLENT"
    color_eval = "#27ae60"
elif score >= 7:
    evaluation = "BON"
    color_eval = "#f39c12"
else:
    evaluation = "À AMÉLIORER"
    color_eval = "#e74c3c"

ax6.text(5, -0.5, evaluation, ha='center', va='center', 
         fontsize=12, fontweight='bold', color=color_eval)

# ============================================
# 3. AFFICHAGE DES RÉSULTATS
# ============================================
plt.tight_layout()
plt.show()

# Affichage console
print("\n" + "="*60)
print("📈 SYNTHÈSE DES KPI")
print("="*60)
print(f"📦 Commandes totales    : {int(total_commandes):,}")
print(f"✅ Commandes livrées    : {int(total_livrees):,} ({pourcentage_livrees:.1f}%)")
print(f"❌ Commandes non-livrées: {int(total_non_livrees):,} ({pourcentage_non_livrees:.1f}%)")
print(f"🎯 Taux de livraison    : {taux_livraison:.1f}%")
print(f"📊 Tendance            : {tendance_amelioration}")
print("="*60)

if taux_livraison >= 90:
    print("🎉 EXCELLENTE PERFORMANCE ! Taux de livraison > 90%")
elif taux_livraison >= 80:
    print("👍 BONNE PERFORMANCE. Objectif 90% à atteindre.")
else:
    print("⚠️  ATTENTION : Taux de livraison en dessous de 80%")
    
print("="*60)