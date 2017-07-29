import cs50

def main():
    # Prompt user for height of pyramid until it's valid.
    while True:
        print("Height: ", end="")
        height = cs50.get_int()
        if height <= 23 and height >= 0:
            break
    print_pyramid(height)

def print_pyramid(height):
    for i in range(height):
        # Left side of pyramid.
        print(" " * (height-i-1), end="")
        print("#" * (i+2), end="")
        # Gap between pyramid.
        print("  ", end="")
        # Right side of pyramid.
        print("#" * (i+2), end="")
        # Start new row.
        print()
    
if __name__ == "__main__":
    main()