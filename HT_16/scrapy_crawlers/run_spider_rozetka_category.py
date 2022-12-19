# run_spider_rozetka_category.py
import subprocess
import os


def run_spider(rel_path, category):
    os.chdir(os.path.join(os.getcwd(), rel_path))
    print("Attention: Wait process begin soon...")

    try:
        sub_category, category_code, *_ = category.split("/")
    except ValueError:
        raise (f"Sorry passed input parameter: {category} is not valid, "
              f"sample: mobile-phones/c80003/")

    subprocess.run([
        "scrapy",
        "crawl",
        "rozetka_category_spider",
        "-O",
        f"../{category_code}_products.csv"],
        "-a",
        "relative_url={sub_category}/{category_code}/")


if __name__ == "__main__":
    run_spider()
