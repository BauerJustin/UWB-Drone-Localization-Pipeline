import sys
sys.path.append('.')
from src.utils import MeasurementAnalyzer
from src.utils import Parser

def main():
    args = Parser().parse()
    analyzer = MeasurementAnalyzer(args.file_name)
    analyzer.analyze()

if __name__ == "__main__":
    main()