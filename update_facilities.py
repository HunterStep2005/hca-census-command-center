import json
from datetime import datetime, timedelta

def iso_to_datetime(dt_str):
    return datetime.fromisoformat(dt_str)

def main():
    try:
        with open('data-charts.json', 'r', encoding='utf-8') as f:
            charts_data = json.load(f)
    except Exception as e:
        print(f"Error reading data-charts.json: {e}")
        return

    try:
        with open('data-facilities.json', 'r', encoding='utf-8') as f:
            fac_data = json.load(f)
    except Exception as e:
        print(f"Error reading data-facilities.json: {e}")
        return

    if 'chartData' not in charts_data:
        print("chartData structure not found.")
        return
        
    for fac_id, chart in charts_data['chartData'].items():
        if fac_id not in fac_data['facilities']:
            continue
            
        fac = fac_data['facilities'][fac_id]
        
        # update latest metrics directly
        def get_latest_stat(series_name):
            series = chart.get(series_name, [])
            return series[-1]['v'] if series else 0

        latest_admissions = get_latest_stat('Admissions')
        latest_births = get_latest_stat('Births')
        latest_discharges = get_latest_stat('Discharges')
        latest_icu = get_latest_stat('ICU Occupancy')
        latest_census = get_latest_stat('Total Census')
        
        fac['latestAdmissions'] = latest_admissions
        fac['latestBirths'] = latest_births
        fac['latestDischarges'] = latest_discharges
        fac['latestICU'] = latest_icu
        fac['latestCensus'] = latest_census
        
        beds = fac.get('beds', 0)
        icu_max = fac.get('icuMax', 0)
        
        # update percentages
        if icu_max > 0:
            fac['icuPct'] = round((latest_icu / icu_max) * 100, 1)
        if beds > 0:
            fac['occupancyPct'] = round((latest_census / beds) * 100, 1)
            
        def calculate_delta_24h(series_name, latest_val):
            series = chart.get(series_name, [])
            if not series: return 0
            
            latest_time_str = series[-1]['t']
            latest_time = iso_to_datetime(latest_time_str)
            target_time = latest_time - timedelta(hours=24)
            
            # Find closest historical point
            prior_val = series[-1]['v']
            for point in reversed(series):
                pt_time = iso_to_datetime(point['t'])
                if pt_time <= target_time:
                    prior_val = point['v']
                    break
            
            return latest_val - prior_val

        fac['icuDelta24h'] = calculate_delta_24h('ICU Occupancy', latest_icu)
        fac['censusDelta24h'] = calculate_delta_24h('Total Census', latest_census)

    # Write back
    try:
        with open('data-facilities.json', 'w', encoding='utf-8') as f:
            json.dump(fac_data, f, indent=4)
        print("Successfully updated data-facilities.json")
    except Exception as e:
        print(f"Error writing data-facilities.json: {e}")

if __name__ == "__main__":
    main()
