from src.utils import DataAnalyzer
from src.utils import Parser

def main():
    args = Parser().parse()
    analyzer = DataAnalyzer(args.file_name)
    analyzer.analyze()

if __name__ == "__main__":
    main()