#!/usr/bin/env python3
import sqlite3
import json

class GroupBuilder:
    def __init__(self, db_path="src/data/species.db"):
        self.db_path = db_path
    
    def _search_plants(self, search_term):
        """Fuzzy search across all plant names"""
        conn = sqlite3.connect(self.db_path)
        plants = conn.execute(
            "SELECT latin_name, english_name, spanish_name FROM species"
        ).fetchall()
        conn.close()
        
        matches = []
        search_term = search_term.lower().strip()
        
        for latin, english, spanish in plants:
            if (search_term in english.lower() or 
                search_term in spanish.lower() or 
                search_term in latin.lower()):
                matches.append((latin, english, spanish))
        
        return matches
    
    def _display_matches(self, matches):
        """Show search results clearly"""
        if not matches:
            print("❌ No matches found")
            return
        
        print(f"\n🔍 Found {len(matches)} matches:")
        for i, (latin, english, spanish) in enumerate(matches, 1):
            print(f"{i}. {english} ({spanish}) - {latin}")
    
    def build_groups(self):
        """Smart search-based group building"""
        print("🌱 SMART PLANT SELECTION")
        print("==================================================")
        print("🔍 Type plant names to search (partial names work)")
        print("   'list' - show all plants")
        print("   'done' - finish group")
        print("   'view' - show current groups")
        print("   'finish' - complete all grouping")
        print("==================================================")
        
        groups = []
        current_group = []
        all_used_plants = set()
        
        while True:
            print(f"\nCurrent group: {[p[1] for p in current_group] if current_group else 'Empty'}")
            print(f"Total groups: {len(groups)}")
            
            search_term = input("\nSearch for plant: ").strip()
            
            if search_term.lower() == 'finish':
                if current_group:
                    groups.append(current_group)
                break
            
            elif search_term.lower() == 'done':
                if current_group:
                    groups.append(current_group)
                    print(f"✅ Group {len(groups)} completed!")
                    current_group = []
                else:
                    print("ℹ️ Current group is empty")
            
            elif search_term.lower() == 'view':
                print("\n📊 CURRENT GROUPS:")
                for i, group in enumerate(groups, 1):
                    plants = [f"{english} ({latin})" for latin, english, spanish in group]
                    print(f"Group {i}: {', '.join(plants)}")
            
            elif search_term.lower() == 'list':
                conn = sqlite3.connect(self.db_path)
                all_plants = conn.execute(
                    "SELECT latin_name, english_name, spanish_name FROM species ORDER BY english_name"
                ).fetchall()
                conn.close()
                
                print("\n📋 ALL PLANTS:")
                for latin, english, spanish in all_plants:
                    print(f"  - {english} ({spanish}) - {latin}")
            
            else:
                matches = self._search_plants(search_term)
                if matches:
                    self._display_matches(matches)
                    
                    try:
                        choice = input("Select number (or Enter to search again): ").strip()
                        if choice.isdigit():
                            index = int(choice) - 1
                            if 0 <= index < len(matches):
                                selected_plant = matches[index]
                                
                                # Check if plant already in current group
                                if selected_plant[0] in [p[0] for p in current_group]:
                                    print(f"ℹ️ {selected_plant[1]} already in current group")
                                else:
                                    current_group.append(selected_plant)
                                    all_used_plants.add(selected_plant[0])
                                    print(f"✅ Added: {selected_plant[1]}")
                            else:
                                print("❌ Invalid selection")
                    except ValueError:
                        print("❌ Please enter a number")
                else:
                    print("❌ No plants found. Try different search terms.")
        
        # Convert to the format expected by the main application
        final_groups = []
        for group in groups:
            plant_group = [f"{latin} ({english})" for latin, english, spanish in group]
            final_groups.append(plant_group)
        
        return final_groups

if __name__ == "__main__":
    builder = GroupBuilder()
    print("Testing smart group builder...")
    groups = builder.build_groups()
    print(f"\n🎉 Final groups: {groups}")
