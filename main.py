import random
import json

def load_json(filename):
    try:
        with open(filename, "r") as f:
            latijn = json.load(f)
    except FileNotFoundError:
        print("latijn.json not found. Please ensure the file exists.")
        return
    except json.JSONDecodeError:
        print("Error decoding JSON from latijn.json.")
        return
    return latijn
    

def main():
    print("Hello from latijn!")

    latijn = load_json("latijn.json")
    if latijn is None:
        return
    
    # merge the dictionary ignoring the first level
    d = {}
    for k in list(latijn.keys()):
        for k2 in list(latijn[k].keys()):
            d[k2] = latijn[k][k2]
        
    latijn = d

    while True:
        e = random.randint(0, len(latijn) - 1)
        k = list(latijn.keys())
        my_answer = input(k[e]+ ": ").lower()
        if my_answer in latijn[k[e]]:
            print("Correct!")
            latijn.pop(k[e])
        else:
            print("Incorrect!", latijn[k[e]])


if __name__ == "__main__":
    main()
