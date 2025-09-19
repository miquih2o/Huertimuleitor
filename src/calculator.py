#!/usr/bin/env python3
import sqlite3
import math

class OrchardCalculator:
    def __init__(self, db_path="src/data/species.db"):
        self.db_path = db_path
    
    def calculate_total_space(self, farmer_groups, demand_kg):
        """Simple calculation with plants and expected output"""
        print("\n" + "="*50)
        print("🎉 FINAL RESULTS")
        print("="*50)
        
        total_area = 0
        total_production = sum(demand_kg.values())
        group_areas = []
        
        for i, group in enumerate(farmer_groups, 1):
            group_area = 0
            group_plants = []
            
            for plant_info in group:
                latin_name = plant_info.split(" (")[0]
                english_name = plant_info.split(" (")[1][:-1]
                
                if latin_name in demand_kg and demand_kg[latin_name] > 0:
                    conn = sqlite3.connect(self.db_path)
                    result = conn.execute(
                        "SELECT weekly_kg, weekly_area FROM species WHERE latin_name = ?",
                        (latin_name,)
                    ).fetchone()
                    conn.close()
                    
                    if result:
                        weekly_kg, weekly_area = result
                        plant_area = (demand_kg[latin_name] / weekly_kg) * weekly_area
                        group_area = max(group_area, plant_area)
                        
                        # Calculate plants (1 plant per 0.1 m²)
                        plants_needed = math.ceil(plant_area / 0.1)
                        group_plants.append((english_name, plants_needed, demand_kg[latin_name]))
            
            if group_plants:
                total_area += group_area
                group_areas.append(group_area)
                print(f"Group {i}\t{group_area:.1f} m²")
                for english_name, plants, expected_kg in group_plants:
                    print(f"{english_name}: {plants} plants → {expected_kg} kg/week")
                print()
        
        print(f"📍 Total area required: {total_area:.1f} m²")
        print(f"🌿 Number of plant groups: {len(farmer_groups)}")
        print(f"📦 Total production: {total_production:.1f} kg/week")
        
        return total_area, group_areas  # Fixed: return both values

if __name__ == "__main__":
    calculator = OrchardCalculator()
    
    # Example
    demand = {"Solanum_lycopersicum": 5.0, "Ocimum_basilicum": 2.0}
    example_groups = [["Solanum_lycopersicum (Tomato)", "Ocimum_basilicum (Basil)"]]
    
    print("Testing simple calculator...")
    calculator.calculate_total_space(example_groups, demand)
