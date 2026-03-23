import json
import random
from pathlib import Path

def split_and_shuffle():
    ROOT = Path(__file__).parent.parent
    IN_FILE = ROOT / "data" / "processed" / "training_data.jsonl"
    TRAIN_FILE = ROOT / "data" / "processed" / "training_data.jsonl"
    GOLDEN_FILE = ROOT / "data" / "processed" / "golden_dataset.jsonl"

    if not IN_FILE.exists():
        print(f"Erro: {IN_FILE} não encontrado.")
        return

    # Lê todos os exemplos
    with open(IN_FILE, "r", encoding="utf-8") as f:
        entries = [json.loads(line) for line in f if line.strip()]

    print(f"Total de exemplos lidos: {len(entries)}")

    # Embaralha de forma aleatória
    random.seed(42) # Para reprodutibilidade se necessário, ou remova para ser 100% randômico
    random.shuffle(entries)

    # Seleciona 20 para o Golden Dataset
    golden_data = entries[:20]
    train_data = entries[20:]

    # Salva o Golden Dataset
    with open(GOLDEN_FILE, "w", encoding="utf-8") as f:
        for entry in golden_data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    # Sobrescreve o training_data com os restantes (82 no caso atual)
    with open(TRAIN_FILE, "w", encoding="utf-8") as f:
        for entry in train_data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Sucesso!")
    print(f"Golden Dataset: {len(golden_data)} exemplos em {GOLDEN_FILE.name}")
    print(f"Training Data: {len(train_data)} exemplos em {TRAIN_FILE.name}")

if __name__ == "__main__":
    split_and_shuffle()
