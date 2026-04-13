import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

OUT = Path('/home/ubuntu/crawl_report')
OUT.mkdir(exist_ok=True)

# Brand colours
SC_DARK   = '#1a2332'
SC_BLUE   = '#2563eb'
SC_GREEN  = '#16a34a'
SC_AMBER  = '#d97706'
SC_RED    = '#dc2626'
SC_LIGHT  = '#f1f5f9'
SC_GREY   = '#64748b'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.facecolor': SC_LIGHT,
    'figure.facecolor': 'white',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# ─── 1. CRAWL ACTIVITY OVER TIME ─────────────────────────────────────────────
dates = ['Apr 10', 'Apr 11']
requests = [22, 2]
sizes_kb = [66472/1024, 0]
resp_ms = [200, 63]

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
fig.suptitle('Googlebot Crawl Activity — southconsultants.biz', fontsize=14,
             fontweight='bold', color=SC_DARK, y=1.02)

ax = axes[0]
bars = ax.bar(dates, requests, color=[SC_BLUE, SC_GREY], width=0.4, zorder=3)
ax.set_title('Total Crawl Requests', fontweight='bold', color=SC_DARK)
ax.set_ylabel('Requests')
ax.bar_label(bars, fmt='%d', padding=3, fontweight='bold')
ax.set_ylim(0, 28)
ax.grid(axis='y', alpha=0.4, zorder=0)

ax = axes[1]
bars = ax.bar(dates, [66472/1024, 0], color=[SC_BLUE, SC_GREY], width=0.4, zorder=3)
ax.set_title('Download Size (KB)', fontweight='bold', color=SC_DARK)
ax.set_ylabel('KB')
ax.bar_label(bars, fmt='%.1f', padding=3, fontweight='bold')
ax.set_ylim(0, 80)
ax.grid(axis='y', alpha=0.4, zorder=0)

ax = axes[2]
bars = ax.bar(dates, resp_ms, color=[SC_GREEN, SC_GREEN], width=0.4, zorder=3)
ax.set_title('Avg Response Time (ms)', fontweight='bold', color=SC_DARK)
ax.set_ylabel('ms')
ax.bar_label(bars, fmt='%d ms', padding=3, fontweight='bold')
ax.set_ylim(0, 260)
ax.axhline(200, color=SC_AMBER, linestyle='--', alpha=0.6, label='200ms threshold')
ax.legend(fontsize=9)
ax.grid(axis='y', alpha=0.4, zorder=0)

plt.tight_layout()
plt.savefig(OUT / 'crawl_activity.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ crawl_activity.png")

# ─── 2. RESPONSE CODES ───────────────────────────────────────────────────────
resp_labels = ['200 OK\n(62.5%)', '301 Redirect\n(29.2%)', '404 Not Found\n(8.3%)']
resp_vals   = [0.6250, 0.2917, 0.0833]
resp_colors = [SC_GREEN, SC_AMBER, SC_RED]

fig, ax = plt.subplots(figsize=(6, 5))
wedges, texts, autotexts = ax.pie(
    resp_vals, labels=resp_labels, colors=resp_colors,
    autopct='%1.0f%%', startangle=90,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2},
    textprops={'fontsize': 10}
)
for at in autotexts:
    at.set_fontweight('bold')
    at.set_color('white')
ax.set_title('HTTP Response Codes\n(24 total requests)', fontweight='bold',
             color=SC_DARK, fontsize=13)
plt.tight_layout()
plt.savefig(OUT / 'response_codes.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ response_codes.png")

# ─── 3. CRAWL PURPOSE ────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(5, 4))
purposes = ['Refresh\n(known pages)', 'Discovery\n(new pages)']
p_vals = [0.75, 0.25]
p_colors = [SC_BLUE, SC_GREEN]
bars = ax.barh(purposes, p_vals, color=p_colors, height=0.4, zorder=3)
ax.set_xlim(0, 1)
ax.set_xlabel('Proportion of Crawl Requests')
ax.set_title('Crawl Purpose', fontweight='bold', color=SC_DARK, fontsize=13)
for bar, val in zip(bars, p_vals):
    ax.text(val + 0.02, bar.get_y() + bar.get_height()/2,
            f'{val*100:.0f}%', va='center', fontweight='bold', color=SC_DARK)
ax.grid(axis='x', alpha=0.4, zorder=0)
plt.tight_layout()
plt.savefig(OUT / 'crawl_purpose.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ crawl_purpose.png")

# ─── 4. BOT TYPE BREAKDOWN ───────────────────────────────────────────────────
bot_labels = ['Desktop', 'Other agent', 'Smartphone', 'Page resource', 'Image']
bot_vals   = [0.2917, 0.2500, 0.2083, 0.1667, 0.0833]
bot_colors = [SC_BLUE, SC_GREY, SC_GREEN, SC_AMBER, '#7c3aed']

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.barh(bot_labels[::-1], bot_vals[::-1], color=bot_colors[::-1], height=0.5, zorder=3)
ax.set_xlim(0, 0.4)
ax.set_xlabel('Proportion of Crawl Requests')
ax.set_title('Googlebot Type Breakdown', fontweight='bold', color=SC_DARK, fontsize=13)
for bar, val in zip(bars, bot_vals[::-1]):
    ax.text(val + 0.005, bar.get_y() + bar.get_height()/2,
            f'{val*100:.0f}%', va='center', fontweight='bold', color=SC_DARK)
ax.grid(axis='x', alpha=0.4, zorder=0)
plt.tight_layout()
plt.savefig(OUT / 'bot_types.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ bot_types.png")

# ─── 5. FILE TYPE BREAKDOWN ──────────────────────────────────────────────────
ft_labels = ['HTML', 'Other', 'JavaScript', 'CSS', 'Unknown\n(failed)']
ft_vals   = [0.3333, 0.2917, 0.1667, 0.1250, 0.0833]
ft_colors = [SC_BLUE, SC_GREY, SC_AMBER, '#7c3aed', SC_RED]

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.barh(ft_labels[::-1], ft_vals[::-1], color=ft_colors[::-1], height=0.5, zorder=3)
ax.set_xlim(0, 0.45)
ax.set_xlabel('Proportion of Crawl Requests')
ax.set_title('File Type Breakdown', fontweight='bold', color=SC_DARK, fontsize=13)
for bar, val in zip(bars, ft_vals[::-1]):
    ax.text(val + 0.005, bar.get_y() + bar.get_height()/2,
            f'{val*100:.0f}%', va='center', fontweight='bold', color=SC_DARK)
ax.grid(axis='x', alpha=0.4, zorder=0)
plt.tight_layout()
plt.savefig(OUT / 'file_types.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ file_types.png")

print("\nAll charts saved to", OUT)
