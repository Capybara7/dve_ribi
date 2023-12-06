from Twofish import Twofish
from Twofish_ECB import TwofishECB
from Twofish_CBC import TwofishCBC
from PIL import Image

def image_to_bytes(path):
    img = Image.open(path).convert('RGBA')
    byte_img = img.tobytes()
    return [img.mode, img.size, byte_img]

def bytes_to_image(data, output_path):
    mode, size, byte_blocks = data
    image = Image.frombytes(mode, size, byte_blocks)
    image.save(output_path)
    return image

def bytes_to_img_not_save(data):
    mode, size, byte_blocks = data
    image = Image.frombytes(mode, size, byte_blocks)
    return image

def key_to_bytes(key):
    return bytes(key, 'utf-8')

#key = 'djut68bf6k2lx03m'
#key_bytes = bytes(key, 'utf-8')

##ECB

##SHIFR
#img = image_to_bytes('Картинки\\1.png')
#shifr_kartina = [img[0], img[1], TwofishECB(key_bytes).encrypt(img[2])]


#bytes_to_image(shifr_kartina, 'Картинки\\1_ecb_enc.png')

##DESHIFR
#img = image_to_bytes('Картинки\\1_ecb_enc.png')
#deshifr_kartina = [img[0], img[1], TwofishECB(key_bytes).decrypt(img[2])]

#bytes_to_image(deshifr_kartina, 'Картинки\\1_ecb_dec.png')

##CBC

##SHIFR
#img = image_to_bytes('Картинки\\1.png')
#iv = b"Initialization V"
#shifr_kartina = [img[0], img[1], TwofishCBC(key_bytes, iv).encrypt(img[2])]

#bytes_to_image(shifr_kartina, 'Картинки\\1_cbc_enc.png')

##DESHIFR
#img = image_to_bytes('Картинки\\1_cbc_enc.png')
#iv = b"Initialization V"
#deshifr_kartina = [img[0], img[1], TwofishCBC(key_bytes, iv).decrypt(img[2])]

#bytes_to_image(deshifr_kartina, 'Картинки\\1_cbc_dec.png')
