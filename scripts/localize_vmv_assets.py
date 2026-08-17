from __future__ import annotations

from io import BytesIO
from pathlib import Path

import requests
from PIL import Image, ImageOps

OUT = Path('public/images/vmv')
OUT.mkdir(parents=True, exist_ok=True)

ASSETS = {
    'hero.webp': 'https://static.wixstatic.com/media/848e8e_2c685d962aab4a86815a203555883f57~mv2.jpg/v1/fill/w_1960,h_1110,al_c,q_90/848e8e_2c685d962aab4a86815a203555883f57~mv2.jpg',
    'about.webp': 'https://static.wixstatic.com/media/848e8e_9ede2a8a803b40c2ae6567507e4ab095~mv2.jpg/v1/crop/x_16,y_0,w_992,h_1024/fill/w_1200,h_1250,al_c,q_88/_97dd01a7-c8f6-4924-abb3-682d8ca6c89c.jpg',
    'service-5g.webp': 'https://static.wixstatic.com/media/848e8e_0173110926684b0eac2cf782a32d48e1~mv2.jpg/v1/fill/w_1400,h_788,al_c,q_88/848e8e_0173110926684b0eac2cf782a32d48e1~mv2.jpg',
    'service-cybersecurity.webp': 'https://static.wixstatic.com/media/848e8e_f50af09545234818b00e33b1ae1e1971~mv2.jpg/v1/fill/w_1200,h_1200,al_c,q_88/848e8e_f50af09545234818b00e33b1ae1e1971~mv2.jpg',
    'service-forensics.webp': 'https://static.wixstatic.com/media/848e8e_84141102acff4bf9ba9bd2d2569a8bea~mv2.jpg/v1/fill/w_1400,h_970,al_c,q_88/848e8e_84141102acff4bf9ba9bd2d2569a8bea~mv2.jpg',
    'team-yarnike-washington.webp': 'https://static.wixstatic.com/media/bb3534_75a76d2902b44372bff2fb6baba67367~mv2.jpg/v1/crop/x_0,y_52,w_328,h_347/fill/w_844,h_868,al_c,q_88/Page-1-Image-1.jpg',
    'team-amit-srivastava.webp': 'https://static.wixstatic.com/media/bb3534_f8ad8338978d4dce8c576d7cc4ce986d~mv2.jpg/v1/crop/x_0,y_1,w_362,h_363/fill/w_864,h_868,al_c,q_88/Page-1-Image-3.jpg',
    'team-shailesh-jain.webp': 'https://static.wixstatic.com/media/848e8e_444dd6339b054efbbc5d3c86bf92bd23~mv2.jpg/v1/crop/x_9,y_21,w_395,h_348/fill/w_900,h_820,al_c,q_88/Shailesh-Pic_edited.jpg',
    'team-jennifer-jones-elhag.webp': 'https://static.wixstatic.com/media/848e8e_9411748ce5dc48b0823a98b797a56cf1~mv2.jpg/v1/crop/x_0,y_0,w_270,h_302/fill/w_756,h_792,al_c,q_88/Jennifer.jpg',
    'team-tiffany-childs.webp': 'https://static.wixstatic.com/media/848e8e_b078b3e8154e466ea410e524043fea21~mv2.jpg/v1/crop/x_119,y_25,w_895,h_958/fill/w_756,h_760,al_c,q_88/Tiffanypic.jpg',
    'team-deleep-george.webp': 'https://static.wixstatic.com/media/848e8e_ca47adf95873476fb3bfc39f58ef123a~mv2.jpeg/v1/crop/x_0,y_9,w_413,h_398/fill/w_756,h_728,al_c,q_88/Deleep.jpeg',
    'team-sandeep-katore.webp': 'https://static.wixstatic.com/media/848e8e_3a11f6e1e03b4eee885ee18992432757~mv2.jpg/v1/crop/x_1867,y_743,w_1902,h_1910/fill/w_692,h_696,al_c,q_88/Sandeep%20Profile_JPG.jpg',
    'team-shweta-singh.webp': 'https://static.wixstatic.com/media/848e8e_26c1dbe49a864a6e9d77e07d23880e26~mv2.jpg/v1/crop/x_77,y_0,w_261,h_263/fill/w_660,h_664,al_c,q_88/Shweta%20Singh.jpg',
    'team-arsh-t.webp': 'https://static.wixstatic.com/media/848e8e_322ba84c83fc46b0b3dd14208a409804~mv2.jpg/v1/crop/x_151,y_173,w_877,h_881/fill/w_684,h_688,al_c,q_88/Arsh%20T.jpg',
    'team-kiran-tarlekar.webp': 'https://static.wixstatic.com/media/848e8e_f68eab8e75d6452087921aec000c2762~mv2.jpg/v1/crop/x_0,y_10,w_452,h_478/fill/w_724,h_716,al_c,q_88/KIRAN_PHOTO_edited.jpg',
    'team-jerlene-treherne.webp': 'https://static.wixstatic.com/media/848e8e_474449568c1544009835c5849001eec4~mv2.png/v1/crop/x_50,y_28,w_329,h_329/fill/w_656,h_656,al_c,q_88/44_PNG.png',
}

headers = {'User-Agent': 'Mozilla/5.0 VMV asset migration'}

for filename, url in ASSETS.items():
    target = OUT / filename
    if target.exists():
        print(f'skip {filename}')
        continue

    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()

    image = Image.open(BytesIO(response.content))
    image = ImageOps.exif_transpose(image)
    if image.mode not in ('RGB', 'RGBA'):
        image = image.convert('RGB')
    if image.mode == 'RGBA':
        background = Image.new('RGB', image.size, 'white')
        background.paste(image, mask=image.getchannel('A'))
        image = background

    image.save(target, 'WEBP', quality=84, method=6)
    print(f'wrote {target} {image.width}x{image.height}')
