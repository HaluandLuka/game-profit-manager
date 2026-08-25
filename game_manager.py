
         
import json              
from pathlib import Path
from datetime import datetime


DATA_FILE = Path(__file__).with_name("items.json")
              
def save_items(items: list[dict]) -> None:               
    with open(DATA_FILE, "w", encoding="utf-8") as file:               
        json.dump(items, file, ensure_ascii=False, indent=4)               

def backup_corrupted_file() -> None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = DATA_FILE.with_name(
        f"items_backup_{timestamp}.json"
    )

    DATA_FILE.rename(backup_file)

    print(f"壊れたデータをバックアップしました: {backup_file.name}")
              
def load_items() -> list[dict]:              
    try:              
        with open(DATA_FILE, "r", encoding="utf-8") as file:              
            return json.load(file)   
                   
    except FileNotFoundError:              
        return []  
    
    except json.JSONDecodeError:
        print("保存データが壊れています") 
        backup_corrupted_file()
        print("空の状態で起動します")
        return []           
    
def get_next_id(items: list[dict]) -> int:    
    if not items:    
        return 1    
    
    return max(item["id"] for item in items) + 1   
  
def find_item_by_id(items: list[dict], item_id: int) -> dict | None:   
    for item in items:  
        if item["id"] == item_id:  
            return item  
  
    return None  

def input_non_negative_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt)) 

            if value < 0:
                print("金額は0以上で入力してください")
                continue

            return value

        except ValueError:
            print("金額は数字で入力してください")

def calc_profit(
    price: int,
    cost: int,
    parts: int,
    shipping: int,
    fee: int
) -> int:
                          
    profit = price - cost - parts - shipping - fee             
    return profit                      
                      
def judge_profit(profit: int) -> str:                      
    if profit >= 3000:                      
        return "利益十分"             
    elif profit > 0:                      
        return "利益あり" 
    elif profit == 0:
        return "収支ゼロ"              
    else:                      
        return "赤字"                 
       
def register_item(items: list[dict]) -> None:                
    print("商品登録")                    
       
    name = input("商品名: ").strip()                   

    if not name:
        print("商品名を入力してください")
        return            

    cost = input_non_negative_int("仕入れ価格: ")
    parts = input_non_negative_int("部品代: ")
    shipping = input_non_negative_int("送料: ")
    fee = input_non_negative_int("販売手数料: ")
    price = input_non_negative_int("販売価格: ")

    profit = calc_profit(
        price,
        cost,
        parts,
        shipping,
        fee
    )                       
    judge = judge_profit(profit)                       
    new_id = get_next_id(items)    
                  
    item = {                       
        "id": new_id,    
        "name": name,                       
        "cost": cost,                       
        "parts": parts,      
        "shipping": shipping,
        "fee": fee,                 
        "price": price,                       
        "profit": profit,                       
        "judge": judge                       
    }                       
                      
    items.append(item)                      
    save_items(items)          
          
    print("商品を登録しました")          
       
def show_items(items: list[dict]) -> None:       
    print("商品一覧")                    
                  
    if not items:                    
        print("登録商品がありません")                    
    else:                    
        for item in items:                 
            print(f"ID: {item['id']}")      
            print(f"商品: {item['name']}") 
            print(f"仕入れ価格: {item['cost']}円")
            print(f"部品代: {item['parts']}円")
            print(f"送料: {item['shipping']}円")
            print(f"販売手数料: {item['fee']}円")
            print(f"販売価格: {item['price']}円")                     
            print(f"利益: {item['profit']}円")                      
            print(f"判定: {item['judge']}")         
            print("-----")  
  
def edit_item(items: list[dict]) -> None:        
    if not items:         
        print("編集できる商品がありません")         
    else:           
        for item in items:          
            print(f"ID: {item['id']} / 商品: {item['name']}")               
             
        try:         
            edit_id = int(input("編集する商品ID: "))           
         
            item = find_item_by_id(items, edit_id) 
 
            if item is None:         
                print("そのIDの商品は存在しません")         
                return                
               
            new_name = input("商品名: ").strip()   

            if not new_name:
                print("商品名を入力してください")
                return
                    
            new_cost = input_non_negative_int("仕入れ価格: ")
            new_parts = input_non_negative_int("部品代: ") 
            new_shipping = input_non_negative_int("送料: ")
            new_fee = input_non_negative_int("販売手数料: ")
            new_price = input_non_negative_int("販売価格: ")
          
            new_profit = calc_profit(     
                new_price,     
                new_cost,     
                new_parts,
                new_shipping,
                new_fee     
            )     
     
            new_judge = judge_profit(new_profit)         
     
            item["name"] = new_name     
            item["cost"] = new_cost     
            item["parts"] = new_parts
            item["shipping"] = new_shipping
            item["fee"] = new_fee     
            item["price"] = new_price     
            item["profit"] = new_profit     
            item["judge"] = new_judge     
     
            save_items(items)          
          
            print("商品情報を更新しました")      
    
        except ValueError:         
            print("商品ID・金額は数字で入力してください")              
       
def delete_item(items: list[dict]) -> None:       
    if not items:               
        print("削除できる商品がありません")               
    else:               
        for item in items:               
            print(f"ID: {item['id']} / 商品: {item['name']}")               
               
        try:              
            delete_id = int(input("削除する商品ID: "))               
            
            item = find_item_by_id(items, delete_id)
                   
            if item is None:               
                print("そのIDの商品は存在しません")               
                return               
               
            items.remove(item)              
            save_items(items)             
             
            print(f"{item['name']}を削除しました")               
                
        except ValueError:              
            print("商品IDは数字で入力してください")          
        

def main() -> None:        
    print("=== ゲーム機 利益計算 ===")                       
                       
    items = load_items()               
                       
    while True:                     
        print("=== メニュー ===")                     
        print("1. 商品を登録")                     
        print("2. 商品一覧")            
        print("3. 商品を編集")                   
        print("4. 商品を削除")                  
        print("5. 終了")                 
                       
        choice = input("選択: ")                     
                     
        if choice == "1":         
            register_item(items)          
         
        elif choice == "2":            
            show_items(items)                       
              
        elif choice == "3":          
            edit_item(items)        
                
        elif choice == "4":           
            delete_item(items)              
                               
        elif choice == "5":                                           
            print("終了します")                        
            break                        
        else:                        
            print("1～5を入力してください")
        
if __name__ == "__main__":                
    main()                        
                        
                        
 