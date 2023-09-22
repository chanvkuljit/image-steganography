from PIL import Image

def encode_image(image_path, message):
    image = Image.open(image_path)
    width, height = image.size
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(image.getpixel((x, y)))
            for color_channel in range(3):  # R, G, B channels
                if index < len(binary_message):
                    pixel[color_channel] &= ~1  # Clear the LSB
                    pixel[color_channel] |= int(binary_message[index])
                    index += 1
            image.putpixel((x, y), tuple(pixel))

    encoded_image_path = "encoded_image.png"
    image.save(encoded_image_path)
    print("Image encoded successfully!")
    return encoded_image_path

def decode_image(encoded_image_path):
    image = Image.open(encoded_image_path)
    width, height = image.size
    binary_message = []

    for y in range(height):
        for x in range(width):
            pixel = [image.getpixel((x, y))[color_channel] & 1 for color_channel in range(3)]
            binary_message.extend(pixel)

    decoded_message = []
    byte_buffer = []

    for bit in binary_message:
        byte_buffer.append(str(bit))
        if len(byte_buffer) == 8:
            byte = ''.join(byte_buffer)
            decoded_message.append(chr(int(byte, 2)))
            byte_buffer = []

    return ''.join(decoded_message)
# Example usage
cover_image_path = "D:\Image steganography\skull.jpg"
secret_message = "aryan have laptop "

encoded_image_path = encode_image(cover_image_path, secret_message)

decoded_message = decode_image(encoded_image_path)

with open("decoded_message.txt", "w", encoding="utf-8") as file:
    file.write(decoded_message)

print("Decoded message saved to decoded_message.txt")