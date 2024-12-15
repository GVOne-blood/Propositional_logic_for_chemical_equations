import pandas as pd
from collections import deque
import re

class dieuCheHoaHoc:
    def __init__(self, file_path):
        self.file_path = file_path
        self.facts, self.rules = self.preprocess_reactions()

    def preprocess_reactions(self):
        df = pd.read_excel(self.file_path)
        reactions = df.iloc[:, 0].tolist()
        
        facts = set()
        rules = []

        for reaction in reactions:
            reactants, products = reaction.split("⟶")
            
            reactants = [re.sub(r'^\d+', '', x.strip()) for x in reactants.split("+")]
            products = [re.sub(r'^\d+', '', x.strip()) for x in products.split("+")]
            
            facts.update(reactants)
            
            rules.append({
                "if": set(reactants),
                "then": set(products),
                "reaction": reaction.strip()
            })
        return facts, rules

    def forward_chaining(self, initial_facts, target):
        queue = deque(initial_facts)
        inferred = set(initial_facts)
        reaction_sequence = []
        visited = set()

        while queue:
            current_fact = queue.popleft()

            for rule in sorted(self.rules, key=lambda r: target in r["then"], reverse=True):
                if rule["if"].issubset(inferred):
                    new_products = rule["then"] - inferred

                    if not new_products:
                        continue

                    if rule["reaction"] in visited:
                        continue

                    inferred.update(new_products)
                    queue.extend(new_products)
                    reaction_sequence.append(rule["reaction"])
                    visited.add(rule["reaction"])

                    if target in inferred:
                        return True, reaction_sequence

        return False, reaction_sequence

    def run_inference(self, initial_facts, target):
        initial_facts = set(x.strip() for x in initial_facts)
        result, reactions = self.forward_chaining(initial_facts, target)
        
        if result:
            print(f"Có thể tạo ra {target} từ các chất ban đầu.")
            print("Thứ tự các phản ứng:")
            for idx, reaction in enumerate(reactions, 1):
                print(f"{idx}. {reaction}")
        else:
            print(f"Không thể tạo ra {target} từ các chất ban đầu.")

        return result, reactions

# Ví dụ sử dụng:
if __name__ == "__main__":
    file_path = "F:\Document\AI_SIC\Chemical_reactions_crawling\Chemical reactions datasetV2.xlsx"
    inference_engine = dieuCheHoaHoc(file_path)
    
    initial_facts = input("Nhập các chất ban đầu (cách nhau bởi dấu phẩy): ").split(",")
    target = input("Nhập chất sản phẩm: ").strip()
    
    inference_engine.run_inference(initial_facts, target)