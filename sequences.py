import random

TRAINING_RULES = ["Ligne", "Serpent"]

TEST_RULES = [
    "Carrés Concentriques",   
    "Spirale",                
    "Diagonale Glissante",    
    "ZigZag Diagonal",        
    "Sauts (+2)",             
    "Sauts (+3)",             
    "Sauts Incrémentaux",     
    "Irrégulier"              
]

def get_full_path(rule_name):
    if rule_name == "Ligne":
        return list(range(25))

    elif rule_name == "Serpent":
        path = []
        for r in range(5):
            row_indices = range(r*5, r*5 + 5)
            if r % 2 == 1: path.extend(reversed(row_indices))
            else: path.extend(row_indices)
        return path

    elif rule_name == "Diagonale Glissante":
        path = []
        curr = 0
        for _ in range(25):
            path.append(curr)
            curr = (curr + 4) % 25
        return path

    elif rule_name == "Carrés Concentriques":
        outer = [0, 1, 2, 3, 4, 9, 14, 19, 24, 23, 22, 21, 20, 15, 10, 5, 0]
        inner = [6, 7, 8, 13, 18, 17, 16, 11, 6]
        center = [12]
        return outer + inner + center

    elif rule_name == "Spirale":
        return [0, 1, 2, 3, 4, 9, 14, 19, 24, 23, 22, 21, 20, 15, 10, 5, 6, 7, 8, 13, 18, 17, 16, 11, 12]
        
    elif rule_name == "ZigZag Diagonal":
        return [0, 5, 1, 2, 6, 10, 15, 11, 7, 3, 4, 8, 12, 16, 20, 21, 17, 13, 9, 14, 18, 22, 23, 19, 24]

    elif rule_name == "Sauts (+2)":
        evens = list(range(0, 25, 2)) 
        odds = list(range(1, 25, 2))  
        return evens + odds

    elif rule_name == "Sauts (+3)":
        path = []
        curr = 0
        for _ in range(25):
            path.append(curr)
            curr = (curr + 3) % 25
        return path

    elif rule_name == "Irrégulier":
        rng = list(range(25))
        random.shuffle(rng)
        return rng

    return list(range(25))

def generate_sequence(rule_name):
    if rule_name == "Sauts Incrémentaux":
        seq = []
        curr = random.randint(0, 24)
        step = 0 
        
        for _ in range(12):
            seq.append(curr)
            curr = (curr + step) % 25
            step += 1
            
        return seq

    if rule_name == "Irrégulier":
        full_path = get_full_path(rule_name) 
        random.shuffle(full_path)
        return full_path[:12]

    full_path = get_full_path(rule_name)
    seq_len = 12
    max_start = len(full_path) - seq_len
    
    if rule_name == "Spirale":
        start_index = random.randint(8, 13)
        return full_path[start_index : start_index + seq_len]
    
    if max_start <= 0:
        return full_path[:seq_len]
        
    start_index = random.randint(0, max_start)
    return full_path[start_index : start_index + seq_len]