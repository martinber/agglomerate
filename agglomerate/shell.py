import argparse

def main():
    print("Hola")
    
    parser = argparse.ArgumentParser(description="Simple texture packer.")
    
    parser.add_argument("-a", "--algorithm", default="simple",
                        help="specify packing algorithm")
    parser.add_argument("-f", "--format", default="simplejson",
                        help="specify output format for coordinates file")
    
    args = parser.parse_args();
    
    print(args.algorithm)
