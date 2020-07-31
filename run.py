import sys
from final import all_operations

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Błędna liczba argumentów")
        exit()
    # in #liczba #out
    input_dir = sys.argv[1]
    images_num = int(sys.argv[2])
    output_dir = sys.argv[3]

    print(input_dir, images_num, output_dir)
    all_operations(input_dir, images_num, output_dir)
