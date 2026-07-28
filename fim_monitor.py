import os
import time
import hashlib
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class FIMSentinel:
    def __init__(self, target_dir: str, baseline_file: str = "baseline.json"):
        self.target_dir = target_dir
        self.baseline_file = baseline_file
        self.baseline_data = {}

    def calculate_hash(self, filepath: str) -> str:
        hasher = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                buf = f.read()
                hasher.update(buf)
            return hasher.hexdigest()
        except FileNotFoundError:
            return None

    def generate_baseline(self):
        logging.info(f"Generating baseline for directory: {self.target_dir}")
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                filepath = os.path.join(root, file)
                self.baseline_data[filepath] = self.calculate_hash(filepath)
        
        with open(self.baseline_file, 'w') as f:
            json.dump(self.baseline_data, f, indent=4)
        logging.info("Baseline generated and saved securely.")

    def load_baseline(self):
        if not os.path.exists(self.baseline_file):
            self.generate_baseline()
        else:
            with open(self.baseline_file, 'r') as f:
                self.baseline_data = json.load(f)
            logging.info("Baseline loaded successfully.")

    def monitor(self, interval: int = 5):
        self.load_baseline()
        logging.info("FIM-Sentinel is now actively monitoring for file changes...")
        
        try:
            while True:
                time.sleep(interval)
                current_files = set()
                
                for root, _, files in os.walk(self.target_dir):
                    for file in files:
                        filepath = os.path.join(root, file)
                        current_files.add(filepath)
                        
                        current_hash = self.calculate_hash(filepath)
                        saved_hash = self.baseline_data.get(filepath)

                        if not saved_hash:
                            logging.warning(f"NEW FILE DETECTED: {filepath}")
                            self.baseline_data[filepath] = current_hash
                        elif current_hash != saved_hash:
                            logging.error(f"INTEGRITY COMPROMISED - MODIFICATION DETECTED: {filepath}")
                            self.baseline_data[filepath] = current_hash
                            
                for saved_filepath in list(self.baseline_data.keys()):
                    if saved_filepath not in current_files and saved_filepath.startswith(self.target_dir):
                        logging.critical(f"FILE DELETED: {saved_filepath}")
                        del self.baseline_data[saved_filepath]
                        
                with open(self.baseline_file, 'w') as f:
                    json.dump(self.baseline_data, f, indent=4)

        except KeyboardInterrupt:
            logging.info("FIM-Sentinel monitoring terminated by user.")

if __name__ == "__main__":
    target_directory = "./secure_data"
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        
    sentinel = FIMSentinel(target_dir=target_directory)
    sentinel.monitor(interval=3)