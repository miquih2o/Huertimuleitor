#!/usr/bin/env python3
from group_builder import GroupBuilder
from calculator import OrchardCalculator

class Huertimuleitor:
    def __init__(self):
        self.group_builder = GroupBuilder()
        self.calculator = OrchardCalculator()
    
    def get_demand_input(self, plants_in_groups):
        """Get demand using English names"""
        demand = {}
        print("\n📊 ENTER PRODUCTION NEEDS (kg/week)")
        print("Only for plants you want to grow:")
        print("=" * 40)
        
        # Get plant mapping
        plant_map = {}
        for plant_str in plants_in_groups:
            for plant in plant_str:
                latin, english = plant.split(" (")
                english = english[:-1]  # Remove closing parenthesis
                plant_map[english] = latin
        
        for english_name in sorted(plant_map.keys()):
            while True:
                try:
                    kg = input(f"kg/week for {english_name} (or Enter for 0): ").strip()
                    if kg == "":
                        break
                    kg = float(kg)
                    if kg > 0:
                        demand[plant_map[english_name]] = kg
                        break
                    print("Please enter a positive number.")
                except ValueError:
                    print("Please enter a valid number.")
        
        return demand
    
    def run(self):
        """Main application flow"""
        print("🌱 HUERTIMULEITOR - Farmer-Led Orchard Simulator")
        print("=" * 50)
        
        # Step 1: Farmer builds groups
        farmer_groups = self.group_builder.build_groups()
        
        # Step 2: Farmer enters production needs
        demand = self.get_demand_input(farmer_groups)
        
        if not demand:
            print("❌ No production needs entered. Exiting.")
            return
        
        # Step 3: System calculates space requirements
        total_area, group_areas = self.calculator.calculate_total_space(farmer_groups, demand)
        
        # Step 4: Show final results
        print("\n" + "=" * 50)
        print("🎉 FINAL RESULTS")
        print("=" * 50)
        print(f"📍 Total area required: {total_area:.1f} m²")
        print(f"🌿 Number of plant groups: {len(farmer_groups)}")
        print(f"📦 Total production: {sum(demand.values()):.1f} kg/week")
        
        return total_area, farmer_groups, demand

if __name__ == "__main__":
    app = Huertimuleitor()
    app.run()
