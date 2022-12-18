# run_spider_chrome_webstore.py
import subprocess
import os


def run_spider(rel_path):
    os.chdir(os.path.join(os.getcwd(), rel_path))
    print("Attention: Wait process begin soon...")
    subprocess.run([
        "scrapy", 
        "crawl", 
        "chrome_webstore_spider", 
        "-O", 
        "../result1.csv"])


if __name__ == "__main__":
    run_spider()
