"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from Twofish_CBC import TwofishCBC
from Twofish_ECB import TwofishECB
from Rabota import *
from force import *

def encrypt_photo(request):
    if request.method == 'POST':
        photo = image_to_bytes(request.FILES.get('photo'))
        img = bytes_to_img_not_save(photo)
        bytes_to_image(photo, 'app\\static\\img.png')
        encryption_key = bytes(request.POST.get('encryption-key'), 'utf-8')
        encryption_mode = request.POST.get('encryption-mode')
        cipher_mode = request.POST.get('cipher-mode')
        if encryption_mode == 'ecb' and cipher_mode == 'enc':
            shifr_img = [photo[0], photo[1], TwofishECB(encryption_key).encrypt(photo[2])]
        if encryption_mode == 'cbc' and cipher_mode == 'enc':
            iv = b"Initialization V"
            shifr_img = [photo[0], photo[1], TwofishCBC(encryption_key, iv).encrypt(photo[2])]
        if encryption_mode == 'ecb' and cipher_mode == 'dec':
            deshifr_img = [photo[0], photo[1], TwofishECB(encryption_key).decrypt(photo[2])]
        if encryption_mode == 'cbc' and cipher_mode == 'dec':
            iv = b"Initialization V"
            deshifr_img = [photo[0], photo[1], TwofishCBC(encryption_key, iv).decrypt(photo[2])]

        if cipher_mode == 'enc':
            cipher_mode = True
            output = 'app\\static\\enc.png'
            sh_img = bytes_to_image(shifr_img, output)
        if cipher_mode == 'dec':
            cipher_mode = False
            output = 'app\\static\\dec.png'
            bytes_to_image(deshifr_img, output)

        #Криптостойкость
        if cipher_mode == True:
            res = []
            res.append({})
        
            coefs = calc_coefs_of_correlations(img)
            res[0]['src_entropy'] = round(img.entropy(),4)
            res[0]['src_covar_h'] = round(coefs['horizontal'], 4)
            res[0]['src_covar_v'] = round(coefs['vertical'], 4)
            res[0]['src_covar_d'] = round(coefs['diagonal'], 4)

            coefs = calc_coefs_of_correlations(sh_img)
            res[0]['enc_entropy'] = round(sh_img.entropy(),4)
            res[0]['enc_covar_h'] = round(coefs['horizontal'], 4)
            res[0]['enc_covar_v'] = round(coefs['vertical'], 4)
            res[0]['enc_covar_d'] = round(coefs['diagonal'], 4)

            changed_pixel_image = get_img_with_changed_random_pixel(img)
            if encryption_mode == 'cbc':
                changed_pixel_enc_bytes = TwofishCBC(encryption_key, iv).encrypt(changed_pixel_image.tobytes())
            else:
                changed_pixel_enc_bytes = TwofishECB(encryption_key).encrypt(changed_pixel_image.tobytes())
            changed_pixel_enc = Image.frombytes(changed_pixel_image.mode, changed_pixel_image.size, changed_pixel_enc_bytes)
            if changed_pixel_image.mode == "P":
                changed_pixel_enc.putpalette(changed_pixel_image.palette)

            npcr = get_npcr(changed_pixel_enc, sh_img)
            uaci = get_uaci(changed_pixel_enc, sh_img)

            context = {
                'cipher_mode': cipher_mode,  # Зашифрованные данные
                'res_src_entropy': res[0]['src_entropy'],
                'res_src_covar_h': res[0]['src_covar_h'],
                'res_src_covar_v': res[0]['src_covar_v'],
                'res_src_covar_d': res[0]['src_covar_d'],

                'res_enc_entropy': res[0]['enc_entropy'],
                'res_enc_covar_h': res[0]['enc_covar_h'],
                'res_enc_covar_v': res[0]['enc_covar_v'],
                'res_enc_covar_d': res[0]['enc_covar_d'],

                'npcr_label': npcr,
                'uaci_label': uaci

            }
            return render(request, 'app/result.html', context)
        else:
            context = {
                'cipher_mode': cipher_mode  # Зашифрованные данные
            }
            return render(request, 'app/result.html', context)

    return render(request, 'app/encryption.html')

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/encryption.html'
    )