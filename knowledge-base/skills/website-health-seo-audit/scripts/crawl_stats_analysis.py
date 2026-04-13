#!/usr/bin/env python3
"""
crawl_stats_analysis.py — Analyse Google Search Console crawl stats CSV exports.

Usage:
    python crawl_stats_analysis.py <csv_dir> [output_dir]

Expected CSV files (from GSC > Settings > Crawl Stats > Export):
    Summarycrawlstatschart.csv
    Responsetable.csv
    Filetypetable.csv
    Purposetable.csv
    Googlebottypetable.csv
    Hoststable.csv

Outputs PNG charts to output_dir (default: ./crawl_report/)
"""
import sys
import os
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def load_csv(csv_dir, filename):
    p = Path(csv_dir) / filename
    if not p.exists():
        return None
    try:
        return pd.read_csv(p)
    except Exception:
        return None

def save_chart(fig, output_dir, name):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    fig.savefig(f'{output_dir}/{name}.png', bbox_inches='tight', dpi=150)
    plt.close(fig)
    print(f'  Saved: {output_dir}/{name}.png')

def plot_crawl_activity(df, output_dir):
    if df is None or df.empty:
        return
    df.columns = [c.strip() for c in df.columns]
    date_col = df.columns[0]
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col])
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    fig.suptitle('Googlebot Crawl Activity', fontsize=14, fontweight='bold')
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    labels = ['Total Requests', 'Download Size (KB)', 'Avg Response Time (ms)']
    colors = ['#2196F3', '#4CAF50', '#FF9800']
    for i, (col, label, color) in enumerate(zip(numeric_cols[:3], labels, colors)):
        axes[i].bar(df[date_col], df[col], color=color, alpha=0.8)
        axes[i].set_ylabel(label, fontsize=9)
        axes[i].tick_params(axis='x', rotation=45, labelsize=7)
    plt.tight_layout()
    save_chart(fig, output_dir, 'crawl_activity')

def plot_pie(df, output_dir, name, title):
    if df is None or df.empty:
        return
    df.columns = [c.strip() for c in df.columns]
    label_col = df.columns[0]
    value_col = df.select_dtypes(include='number').columns[0]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(df[value_col], labels=df[label_col], autopct='%1.1f%%', startangle=90)
    ax.set_title(title, fontsize=13, fontweight='bold')
    save_chart(fig, output_dir, name)

def main():
    csv_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './crawl_report'

    print(f'\nAnalysing crawl stats from: {csv_dir}')
    print(f'Output directory: {output_dir}\n')

    plot_crawl_activity(load_csv(csv_dir, 'Summarycrawlstatschart.csv'), output_dir)
    plot_pie(load_csv(csv_dir, 'Responsetable.csv'),      output_dir, 'response_codes',  'Response Codes')
    plot_pie(load_csv(csv_dir, 'Filetypetable.csv'),      output_dir, 'file_types',      'File Types Crawled')
    plot_pie(load_csv(csv_dir, 'Purposetable.csv'),       output_dir, 'crawl_purpose',   'Crawl Purpose')
    plot_pie(load_csv(csv_dir, 'Googlebottypetable.csv'), output_dir, 'bot_types',       'Googlebot Types')

    hosts = load_csv(csv_dir, 'Hoststable.csv')
    if hosts is not None:
        print('\nHosts Table:')
        print(hosts.to_string(index=False))

    print('\nDone. Open the PNG files in the output directory to review.')

if __name__ == '__main__':
    main()
