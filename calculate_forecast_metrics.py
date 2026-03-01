import json
import pandas as pd

def load_data():
    with open('data-charts.json', 'r', encoding='utf-8') as f:
        charts_data = json.load(f)['chartData']
    with open('data-forecasts.json', 'r', encoding='utf-8') as f:
        forecasts_data = json.load(f)['forecasts']
    with open('data-facilities.json', 'r', encoding='utf-8') as f:
        fac_data = json.load(f)
    return charts_data, forecasts_data, fac_data

def process_metrics():
    charts, forecasts, fac_data = load_data()
    original_metrics = fac_data.get('modelMetrics', {})
    
    results = []
    
    for f_key, forecast_records in forecasts.items():
        parts = f_key.split('_', 1)
        if len(parts) != 2: continue
        fac_id, metric_name = parts[0], parts[1]
        
        if fac_id not in charts or metric_name not in charts[fac_id]: continue
        actual_records = charts[fac_id][metric_name]
        
        # 1. Train Points = Total number of historical records available
        train_points = len(actual_records)
        
        df_actual = pd.DataFrame(actual_records)
        df_actual.rename(columns={'t': 'timestamp', 'v': 'actual_value'}, inplace=True)
        df_actual['timestamp'] = pd.to_datetime(df_actual['timestamp'])
        
        # 2. Test Points = Last 24 hours of data that the model uses as a validation holdout
        latest_time = df_actual['timestamp'].max()
        cutoff_time = latest_time - pd.Timedelta(hours=24)
        
        df_test = df_actual[df_actual['timestamp'] > cutoff_time]
        test_points = len(df_test)
        
        # Recover true validation MAE/MAPE from the original trained models
        true_mae = 0.0
        true_mape = 0.0
        if f_key in original_metrics:
            true_mae = original_metrics[f_key].get('mae', 0.0)
            true_mape = original_metrics[f_key].get('mape', 0.0)
            
        results.append({
            'metric_key': f_key,
            'mae': true_mae,
            'mape': true_mape,
            'trainSize': train_points,
            'testSize': test_points
        })

    df_results = pd.DataFrame(results).set_index('metric_key')
    print("Forecast Metrics Summary (Restored True Accuracy + Dynamic Counters):")
    print("-" * 65)
    print(df_results)
        
    for row in results:
        fac_data['modelMetrics'][row['metric_key']] = {
            'mae': row['mae'],
            'mape': row['mape'],
            'trainSize': row['trainSize'],
            'testSize': row['testSize']
        }
        
    with open('data-facilities.json', 'w', encoding='utf-8') as f:
        json.dump(fac_data, f, indent=4)
        
    print("\nSuccessfully updated `modelMetrics` in data-facilities.json!")

if __name__ == "__main__":
    process_metrics()
