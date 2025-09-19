#!/usr/bin/env python3
import sqlite3, os
def setup():
    os.makedirs('src/data', exist_ok=True)
    for db, schema in [('simulations', 'CREATE TABLE simulations (simulation_id TEXT, username TEXT, timestamp DATETIME, input_parameters TEXT, calculated_results TEXT, compatibility_groups TEXT, farmer_notes TEXT)'), ('varieties_local', 'CREATE TABLE varieties (base_species TEXT, variety_name TEXT, custom_params TEXT, added_by TEXT, created_at DATETIME)')]:
        conn = sqlite3.connect(f'src/data/{db}.db')
        conn.execute(schema)
        conn.commit()
        conn.close()
        print(f"✅ {db}.db")
    print("🎉 Setup complete!")
if __name__ == "__main__": setup()
