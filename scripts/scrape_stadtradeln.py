#!/usr/bin/env python3
"""
STADTRADELN Data Scraper
Fetches team and municipality rankings from STADTRADELN API and generates JSON files.
"""

import requests
import json
import re
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup

# API Configuration
API_BASE = "https://api.stadtradeln.de/v1/results"
API_KEY = "aeKie7iiv6ei"
REGION_ID = "2545"  # Rhein-Neckar-Kreis

# API Endpoints
TEAMS_URL = f"{API_BASE}/city/{REGION_ID}/html"
MUNICIPALITIES_URL = f"{API_BASE}/lk/{REGION_ID}/html"

# Output Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"  # Hugo data directory
STATIC_DATA_DIR = PROJECT_ROOT / "static" / "data"  # Static files for direct access

# Ensure output directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DATA_DIR.mkdir(parents=True, exist_ok=True)


def fetch_api_data(url, params):
    """
    Fetch data from STADTRADELN API endpoint.

    Args:
        url: API endpoint URL
        params: Query parameters

    Returns:
        Parsed JSON response or None if error
    """
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://www.stadtradeln.de',
        'Referer': 'https://www.stadtradeln.de/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None


def parse_german_number(text):
    """
    Parse German-formatted number (e.g., '9.331' -> 9331, '0,35' -> 0.35).

    Args:
        text: String containing a German-formatted number

    Returns:
        Numeric value (int or float)
    """
    if not text:
        return 0

    # Remove spaces and extract number
    text = text.strip().replace(' ', '')

    # Handle km/percentage formats
    text = re.sub(r'[^0-9.,\-]', '', text)

    # German format: . = thousands separator, , = decimal separator
    if ',' in text:
        # Has decimal
        text = text.replace('.', '').replace(',', '.')
        return float(text)
    else:
        # Integer with optional thousands separator
        text = text.replace('.', '')
        return int(text) if text else 0


def parse_teams_html(html_content):
    """
    Parse team rankings from HTML table.

    Args:
        html_content: HTML string from API response

    Returns:
        List of team dictionaries
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    teams = []

    # Find all team rows in the table
    rows = soup.select('tbody tr')

    for row in rows:
        try:
            # Extract rank (first visible td with data-order)
            rank_cells = row.select('td[data-order]')
            if not rank_cells:
                continue
            rank = int(rank_cells[0].get('data-order', 0)) + 1  # data-order is 0-indexed

            # Extract team name
            team_name_cell = row.select_one('.teamname')
            if not team_name_cell:
                continue
            team_name = team_name_cell.get_text(strip=True)

            # Extract kilometers
            km_cell = row.select('td[data-order]')[4]  # 5th td with data-order is km
            km_text = km_cell.select_one('.bar_text')
            if km_text:
                km_raw = km_text.get_text(strip=True).replace('km', '').strip()
                km = parse_german_number(km_raw)
                km_formatted = f"{km:,} km".replace(',', '.')
            else:
                km = 0
                km_formatted = "0 km"

            # Extract CO2 savings from popover
            co2_saved = "0 kg"
            co2_attr = km_cell.select_one('[data-content]')
            if co2_attr:
                co2_text = co2_attr.get('data-content', '')
                co2_match = re.search(r'([\d.,]+\s*kg)', co2_text)
                if co2_match:
                    co2_saved = co2_match.group(1)

            # Extract trips
            trips_cell = row.select_one('[data-column="tracks-column"]')
            trips = 0
            if trips_cell:
                trips_text = trips_cell.select_one('.tracks')
                if trips_text:
                    trips = parse_german_number(trips_text.get_text(strip=True))

            # Extract active riders
            radelnde_cell = row.select_one('.radelnde')
            active_riders = 0
            if radelnde_cell:
                # Use the hidden-xs span which contains the count
                hidden_span = radelnde_cell.select_one('.hidden-xs')
                if hidden_span:
                    riders_text = hidden_span.get_text(strip=True)
                    active_riders = parse_german_number(riders_text)
                else:
                    # Fallback: get data-order attribute
                    data_order = radelnde_cell.get('data-order')
                    if data_order:
                        active_riders = int(data_order)

            # Extract km per head
            km_per_head = 0
            hidden_cells = row.select('td.hidden-xs')
            if len(hidden_cells) >= 2:
                # Second hidden-xs td should be km per head
                km_per_head_text = hidden_cells[1].get_text(strip=True)
                km_per_head = parse_german_number(km_per_head_text)

            teams.append({
                'rank': rank,
                'name': team_name,
                'km': km,
                'kmFormatted': km_formatted,
                'activeRiders': active_riders,
                'trips': trips,
                'kmPerHead': km_per_head,
                'co2Saved': co2_saved
            })

        except Exception as e:
            print(f"Error parsing team row: {e}")
            continue

    return teams


def parse_municipalities_html(html_content):
    """
    Parse municipality rankings from HTML table.

    Args:
        html_content: HTML string from API response

    Returns:
        List of municipality dictionaries
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    municipalities = []

    # Find all municipality rows in the table
    rows = soup.select('tbody tr')

    for row in rows:
        try:
            # Extract rank
            rank_cells = row.select('td[data-order]')
            if not rank_cells:
                continue
            rank = int(rank_cells[0].get('data-order', 0)) + 1  # data-order is 0-indexed

            # Extract municipality name and URL
            name_cell = row.select_one('.teamname a')
            if not name_cell:
                continue
            municipality_name = name_cell.get_text(strip=True)
            municipality_url = name_cell.get('href', '')

            # Extract kilometers
            km_cell = row.select('td[data-order]')[4]  # 5th td with data-order is km
            km_text = km_cell.select_one('.bar_text.hidden-sm')
            if not km_text:
                # Try alternative selector for mobile view
                km_text = km_cell.select_one('.hidden-xs.hidden-md.hidden-lg')
            if km_text:
                km_raw = km_text.get_text(strip=True).replace('km', '').strip()
                km = parse_german_number(km_raw)
                km_formatted = f"{km:,} km".replace(',', '.')
            else:
                km = 0
                km_formatted = "0 km"

            # Extract trips
            trips_cell = row.select_one('[data-column="tracks-column"]')
            trips = 0
            if trips_cell:
                trips_text = trips_cell.select_one('.tracks')
                if trips_text:
                    trips = parse_german_number(trips_text.get_text(strip=True))

            # Extract km per inhabitant
            km_per_inhabitant = 0.0
            km_per_inh_cells = row.select('td.hidden-xs')
            if len(km_per_inh_cells) >= 2:
                # Second hidden-xs td is km per inhabitant
                km_per_inh_text = km_per_inh_cells[1].get_text(strip=True)
                km_per_inhabitant = parse_german_number(km_per_inh_text)

            # Extract population
            population = 0
            pop_cells = row.select('td[data-order]')
            if len(pop_cells) >= 5:
                # Last data-order td is population
                population = int(pop_cells[-1].get('data-order', 0))

            municipalities.append({
                'rank': rank,
                'name': municipality_name,
                'km': km,
                'kmFormatted': km_formatted,
                'trips': trips,
                'kmPerInhabitant': km_per_inhabitant,
                'population': population,
                'url': municipality_url
            })

        except Exception as e:
            print(f"Error parsing municipality row: {e}")
            continue

    return municipalities


def save_json(data, filename):
    """
    Save data to JSON files in both data/ and static/data/ directories.

    Args:
        data: Dictionary to save
        filename: Filename (e.g., 'stadtradeln_teams.json')
    """
    # Save to Hugo data directory
    data_file = DATA_DIR / filename
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {data_file}")

    # Also save to static directory for direct access
    static_file = STATIC_DATA_DIR / filename
    with open(static_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {static_file}")


def main():
    """
    Main scraping workflow.
    """
    print("STADTRADELN Data Scraper")
    print("=" * 50)

    timestamp = datetime.now().astimezone().replace(microsecond=0).isoformat()
    source_url = "https://www.stadtradeln.de/rhein-neckar-kreis"

    # Fetch and parse team rankings
    print("\nFetching team rankings...")
    teams_params = {
        'sr_api_key': API_KEY,
        'L': '0'
    }
    teams_response = fetch_api_data(TEAMS_URL, teams_params)

    if teams_response and 'html' in teams_response:
        teams = parse_teams_html(teams_response['html'])
        teams_data = {
            'lastUpdate': timestamp,
            'source': source_url,
            'teams': teams
        }
        save_json(teams_data, 'stadtradeln_teams.json')
        print(f"  Found {len(teams)} teams")

        # Highlight Eschelbronn team
        eschelbronn_team = next((t for t in teams if 'Eschelbronn' in t['name']), None)
        if eschelbronn_team:
            print(f"  Eschelbronn: Rank {eschelbronn_team['rank']} - {eschelbronn_team['kmFormatted']}")
    else:
        print("  Failed to fetch team data")

    # Fetch and parse municipality rankings
    print("\nFetching municipality rankings...")
    muni_params = {
        'sr_api_key': API_KEY,
        'sr_population_min': '-1',
        'sr_population_max': '-1',
        'L': '0'
    }
    muni_response = fetch_api_data(MUNICIPALITIES_URL, muni_params)

    if muni_response and 'html' in muni_response:
        municipalities = parse_municipalities_html(muni_response['html'])
        muni_data = {
            'lastUpdate': timestamp,
            'source': source_url,
            'municipalities': municipalities
        }
        save_json(muni_data, 'stadtradeln_municipalities.json')
        print(f"  Found {len(municipalities)} municipalities")

        # Highlight Eschelbronn if present
        eschelbronn_muni = next((m for m in municipalities if 'Eschelbronn' in m['name']), None)
        if eschelbronn_muni:
            print(f"  Eschelbronn: Rank {eschelbronn_muni['rank']} - {eschelbronn_muni['kmFormatted']}")
    else:
        print("  Failed to fetch municipality data")

    print("\n" + "=" * 50)
    print("Scraping complete!")


if __name__ == '__main__':
    main()
