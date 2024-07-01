def get_coordinates():
    """Function to get coordinates from the user."""
    x1, y1 = map(float, input("Enter the first point (x1 y1): ").split())
    x2, y2 = map(float, input("Enter the second point (x2 y2): ").split())
    return (x1, y1), (x2, y2)

def calculate_slope_intercept(point1, point2):
    """Function to calculate the slope (m) and y-intercept (b) of the line."""
    x1, y1 = point1
    x2, y2 = point2

    if x1 == x2:
        raise ValueError("The two points must have different x-coordinates for a non-vertical line.")

    # Calculate the slope (m)
    m = (y2 - y1) / (x2 - x1)
    # Calculate the y-intercept (b)
    b = y1 - m * x1

    return m, b

def main():
    # Get coordinates from the user

    while True:
        point1, point2 = get_coordinates()
    
        try:
            # Calculate slope and intercept
            m, b = calculate_slope_intercept(point1, point2)
    
            # Format and print the line equation
            if b >= 0:
                print("The equation of the line is: y = {:.2f}x + {:.2f}".format(m, b))
            else:
                print("The equation of the line is: y = {:.2f}x - {:.2f}".format(m, abs(b)))
    
        except ValueError as e:
            print(e)

        if input("Try again? (Y/N): ").upper() != "Y":
            break

main()
