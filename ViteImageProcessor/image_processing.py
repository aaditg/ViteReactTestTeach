from PIL import Image, ImageFilter
import os

def delete_existing_txt_files():
    txt_files = [file for file in os.listdir() if file.endswith(".txt")]
    for txt_file in txt_files:
        try:
            os.remove(txt_file)
            print("Deleted existing file")
        except Exception as e:
            print("Could not delete file")

def load_image(image_path):
    try:
        image = Image.open(image_path)
        print("Image loaded successfully")
        return image
    except Exception as e:
        print("Error loading image")
        raise

def get_color_input():
    #Change colors here and below
    colors = ["red", "blue", "yellow", "green", "orange", "purple"]


    print("Enter a primary or secondary color from the following list:")
    print(", ".join(colors))
    
    while True:
        color = input("Color: ").strip().lower()
        if color in colors:
            print("Color selected: " + color)
            return color
        else:
            print("Invalid color. Please choose from: "+ ', '.join(colors))

def save_image_and_color(image, color):

    #Save the loaded image and the selected color for other files
    
    image.save("loaded_image.png")
    with open("selected_color.txt", "w") as color_file:
        color_file.write(color)



def delete_existing_output():

    output_file = "isolated_subject.png"
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
        except Exception as e:
            print("Could not delete file, check naming")

def load_color():
    try:
        with open("selected_color.txt", "r") as color_file:
            return color_file.read().strip().lower()
    except Exception as e:
        print("Error loading color file")
        raise

def is_within_range(pixel_color, min_color, max_color):
   
    r, g, b = pixel_color
    min_r, min_g, min_b = min_color
    max_r, max_g, max_b = max_color

    return (
        min_r <= r <= max_r and
        min_g <= g <= max_g and
        min_b <= b <= max_b
    )

def reduce_noise(image):
    return image.filter(ImageFilter.MedianFilter(size=7))  # Adjust filter size for different levels of noise reduction

def isolate_color(image, target_color_name):
    #add colors here, view range sizes for description
    color_ranges = {
        "red": ((120, 0, 0), (255, 130, 130)),       # Slightly smaller Red range
        "blue": ((0, 0, 120), (130, 130, 255)),      # Slightly smaller Blue range
        "yellow": ((120, 120, 0), (255, 255, 120)),  # Slightly smaller Yellow range
        "green": ((0, 120, 0), (130, 255, 130)),     # Slightly smaller Green range
        "orange": ((120, 60, 0), (255, 180, 90)),    # Slightly smaller Orange range
        "purple": ((90, 0, 90), (190, 110, 190)),    # Slightly smaller Purple range
    }

    if target_color_name not in color_ranges:
        raise ValueError("Invalid color")

    min_color, max_color = color_ranges[target_color_name]
    img = image.convert("RGBA")
    pixels = img.load()

    subject_found = False
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y] #a is alpha, alpha is opacity, if alpha is zero, it messes with selection

            # Check if the pixel is within the color range is not transparent (needed for certain filetypes)
            if a > 0 and is_within_range((r, g, b), min_color, max_color):
                subject_found = True
            else:
                pixels[x, y] = (0, 0, 0, 0)  # Set background to white transparent (alpha of zero)

    if not subject_found:
        print("No subject detected based on the selected color")
        #if there is a subject in the color, change the ranges above
    
    img = reduce_noise(img)
    

    return img



def calculate_average_hex(image_path):
    
    try:
        image = Image.open(image_path).convert("RGBA")
        pixels = image.load()
        total_r, total_g, total_b, pixel_count = 0, 0, 0, 0

        for y in range(image.height):
            for x in range(image.width):
                r, g, b, a = pixels[x, y]
                if a > 0:
                    total_r += r
                    total_g += g
                    total_b += b
                    pixel_count += 1

        if pixel_count == 0:
            raise ValueError("No subject detected")
        
        avg_r = total_r // pixel_count
        avg_g = total_g // pixel_count
        avg_b = total_b // pixel_count

        return "#{:02x}{:02x}{:02x}".format(avg_r, avg_g, avg_b).upper()

    except Exception as e:
        print("Error calculating average hex color")
        raise

def save_average_color(avg_hex):

    #Save the average color to a text file for use in other files and display

    with open("average_color.txt", "w") as output_file:
        output_file.write(avg_hex)

