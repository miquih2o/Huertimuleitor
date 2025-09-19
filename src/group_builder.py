#!/usr/bin/env python3
import sqlite3
import os

class GroupBuilder:
    def __init__(self, db_path="src/data/species.db"):
        self.db_path = db_path
    
    def get_all_plants(self):
        """Get all plants with fixed numbering"""
        conn = sqlite3.connect(self.db_path)
        plants = []
        try:
            result = conn.execute("SELECT latin_name, english_name FROM species ORDER BY english_name")
            plants = [(row[0], row[1]) for row in result]
        except:
            plants = [("Solanum_lycopersicum", "Tomato"), ("Ocimum_basilicum", "Basil")]
        conn.close()
        return plants
    
    def show_plant_catalog(self, all_plants):
        """Clear screen and show plant catalog"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("🌱 FARMER GROUP BUILDER")
        print("Create companion groups using fixed plant numbers")
        print("=" * 50)
        print("\n📋 PLANT CATALOG (Always same numbers):")
        for i, (latin, english) in enumerate(all_plants, 1):
            print(f"{i:2d}. {english}")
        print("=" * 50)
    
    def build_groups(self):
        """Fixed-list group building with always-visible catalog"""
        all_plants = self.get_all_plants()
        
        groups = []
        current_group = []
        
        while True:
            self.show_plant_catalog(all_plants)
            
            print(f"Current group: {[all_plants[i-1][1] for i in current_group] if current_group else 'Empty'}")
            print(f"Total groups: {len(groups)}")
            print("\nOptions:")
            print("  [1-8]    - Add plant to current group")
            print("  'done'   - Finish current group")
            print("  'remove' - Remove last plant")  
            print("  'clear'  - Clear current group")
            print("  'view'   - Show all groups")
            print("  'finish' - Complete grouping")
            
            choice = input("\nYour choice: ").strip().lower()
            
            if choice == 'finish':
                if current_group:
                    groups.append(current_group)
                break
            elif choice == 'done':
                if current_group:
                    groups.append(current_group)
                    current_group = []
                continue
            elif choice == 'remove':
                if current_group:
                    current_group.pop()
                continue
            elif choice == 'clear':
                current_group = []
                continue
            elif choice == 'view':
                print("\n📊 ALL GROUPS:")
                for i, group in enumerate(groups, 1):
                    plants = [all_plants[idx-1][1] for idx in group]
                    print(f"Group {i}: {', '.join(plants)}")
                input("\nPress Enter to continue...")
                continue
            
            # Process plant numbers
            try:
                numbers = [int(x.strip()) for x in choice.split(",")]
                for num in numbers:
                    if 1 <= num <= len(all_plants) and num not in current_group:
                        current_group.append(num)
            except ValueError:
                continue
        
        # Convert to plant format
        final_groups = []
        for group in groups:
            plant_group = []
            for plant_num in group:
                latin, english = all_plants[plant_num-1]
                plant_group.append(f"{latin} ({english})")
            final_groups.append(plant_group)
        
        return final_groups

if __name__ == "__main__":
    builder = GroupBuilder()
    groups = builder.build_groups()
    print(f"\n🎉 Final groups: {groups}")
