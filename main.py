import asyncio
from uuid import UUID

from PIL import Image
from bleak import BleakClient

from ESL import ESL
from tram_times import get_next_trams
from utils import make_tram_img, image2hex

ESL_MAC = "A4:C1:38:7D:43:A9"
PRIMARY_SERVICE_UUID = UUID("13187b10-eba9-a3ba-044e-83d3217d9a38")
WRITE_CHARACTERISTIC_UUID = UUID("4b646063-6264-f3a7-8941-e65356ea82fe")
MAX_CHUNK_SIZE = 480

img_hex="00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00008001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00048001ffffffc000008003ffffffff00010001ffffffc0003be003ffffffff00060001ffffffc0003b6003ffffffff00060001ffffffc0003b6003ffffffff00000001ffffffc0003a2003ffffffff00000001ffffffc0003e2003ffffffff00000001ffffffc0003e6003ffffffff00094001ffffffc000000003ffffffff00080001ffffffc000000003ffffffff00060001ffffffc000010003ffffffff00060001ffffffc000010003ffffffff00000001ffffffc000010003ffffffff00038001ffffffc000010003ffffffff00014001ffffffc0000fe003ffffffff00014001ffffffc000010003ffffffff00070001ffffffc000010003ffffffff00070001ffffffc000010003ffffffff00000001ffffffc000010003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00078001ffffffc000000003ffffffff00078001ffffffc000000003ffffffff00078001ffffffc000000003ffffffff003ff001ffffffc000000003ffffffff00401001ffffffc000000003ffffffff004fd001ffffffc000001803ffffffff004fd001ffffffc000004003ffffffff004fd001ffffffc000010003ffffffff004fd001ffffffc000060003ffffffff004fd001ffffffc000060003ffffffff004fd001ffffffc000080003ffffffff004fd001ffffffc000400003ffffffff004fd001ffffffc000000003ffffffff004fd001ffffffc001078003ffffffff004fd001ffffffc000800003ffffffff004fd001ffffffc000800003ffffffff004fd001ffffffc000700003ffffffff004fd001ffffffc0000c0003ffffffff004fd001ffffffc000020003ffffffff004fd001ffffffc000008003ffffffff00401001ffffffc000006003ffffffff003fe001ffffffc000001803ffffffff003fe001ffffffc000001803ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff01fff801ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff0003f801ffffffc000000003ffffffff000ff801ffffffc000000003ffffffff000ff801ffffffc000000003ffffffff000d1001ffffffc000000003ffffffff00390801ffffffc000000003ffffffff00390801ffffffc000000003ffffffff00398801ffffffc000000003ffffffff00399801ffffffc000000003ffffffff00399801ffffffc000000003ffffffff0008f001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff0007f801ffffffc000000003ffffffff000ff801ffffffc000000003ffffffff000ff801ffffffc000000003ffffffff00091001ffffffc000000003ffffffff00390801ffffffc000000003ffffffff00390801ffffffc000000003ffffffff00398801ffffffc000000003ffffffff0038f801ffffffc000000003ffffffff0038f801ffffffc000000003ffffffff0000f001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00380001ffffffc000000003ffffffff00380001ffffffc000000003ffffffff00080001ffffffc000000003ffffffff00080001ffffffc000000003ffffffff000c0001ffffffc000000003ffffffff000ff801ffffffc000000003ffffffff000ff801ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00380801ffffffc000000003ffffffff00380801ffffffc000000003ffffffff00380801ffffffc000000003ffffffff00381801fff03fc0000dc003fff03fff00fff001ffe03fc0003fe003ffe03fff00ffe001ffe69fc0003b2003ffe69fff00080001ffe6dfc0003b2003ffe6dfff00080001ffe6dfc0003b2003ffe6dfff00000001ffe0dfc000382003ffe0dfff00000001fff1ffc000002003fff1ffff000ff801ffffffc000000003ffffffff000c0001ffffdfc000002003ffffdfff00380001ffffdfc000006003ffffdfff00380001ffe01fc0003fe003ffe01fff00380001ffe01fc0003fe003ffe01fff00080001ffe01fc0003fe003ffe01fff000c0001ffe7dfc000386003ffe7dfff000ff801fff7dfc000082003fff7dfff000ff801ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001fff99fc000066003fff99fff00030001fff99fc000066003fff99fff00079801ffffffc000000003ffffffff00098801ffffffc000000003ffffffff00398801fff63fc00009c003fff63fff00398801ffec1fc0003be003ffec1fff00398801ffec1fc0003be003ffec1fff00398801ffe5dfc0003a2003ffe5dfff00099801ffe49fc0003b6003ffe49fff000ff001fff01fc0000fe003fff01fff0007e001fff87fc000078003fff87fff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffdfc000002003ffffdfff00c01001ffffdfc000006003ffffdfff01801801ffe01fc0003fe003ffe01fff01800801ffe01fc0003fe003ffe01fff01800801ffe7dfc000386003ffe7dfff01800801fff7dfc000082003fff7dfff01800801fff7dfc000082003fff7dfff01800801ffffffc000000003ffffffff01801801ffffffc000000003ffffffff00c03001ffffffc000000003ffffffff007ff001ffffffc000000003ffffffff003fc001ffffffc000000003ffffffff003fc001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001fffeffc000010003fffeffff00000001ff3ce1c001831c03ff3ce1ff000ff001fe30c1c0038f3c03fe30c1ff003ffe01fe018fc003fe7003fe018fff000c3301ff001fc001ffe003ff001fff000c3301ff001fc001ffe003ff001fff00381981ffc00fc0007ff003ffc00fff00380981ffe083c0003f7803ffe083ff00380981fff1e1c0000e1c03fff1e1ff00381981fff0f1c0000f0c03fff0f1ff000ff101fffdffc000020003fffdffff000ff101fffdffc000020003fffdffff0003e001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff000ff801ffffffc000000003ffffffff000d3001ffffffc000000003ffffffff000d3001ffffffc000000003ffffffff00391801ffffffc000000003ffffffff00390801ffffffc000000003ffffffff00398801ffffffc000000003ffffffff00399801ffffffc000000003ffffffff0008f801ffffffc000000003ffffffff0008f801ffffffc000000003ffffffff00006001fffe3fc00001c003fffe3fff00000001ffe41fc0003be003ffe41fff00000001ffe5dfc0003a2003ffe5dfff0003f801ffe5dfc0003a2003ffe5dfff000ff801ffe19fc0003e6003ffe19fff00091001ffff9fc000006003ffff9fff00091001ffff9fc000006003ffff9fff00390801ffffffc000000003ffffffff00390801ffffdfc000002003ffffdfff00398801ffff9fc000006003ffff9fff00399801ffe01fc0003fe003ffe01fff0008f001ffe01fc0003fe003ffe01fff0008f001ffe01fc0003fe003ffe01fff00000001ffe79fc000386003ffe79fff00000001fff7dfc000082003fff7dfff00000001ffffffc000000003ffffffff01fff801ffffffc000000003ffffffff01fff801fff99fc000066003fff99fff01fff801fff99fc000066003fff99fff00060001fff99fc000066003fff99fff00060001ffffffc000000003ffffffff00060001ffffffc000000003ffffffff00060001fff63fc00009c003fff63fff00060001ffe41fc0003be003ffe41fff00060001ffe5dfc0003a2003ffe5dfff00060001ffe5dfc0003a2003ffe5dfff01fff801ffe49fc0003b6003ffe49fff01fff801fff01fc0000fe003fff01fff00000001fff87fc000078003fff87fff00000001ffffffc000000003ffffffff00000001ffffdfc000002003ffffdfff00000001ffffdfc000002003ffffdfff00000001ffff9fc000006003ffff9fff00000001ffe01fc0003fe003ffe01fff00000001ffe01fc0003fe003ffe01fff00000001ffe79fc000386003ffe79fff00000001fff7dfc000082003fff7dfff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff000ff801ffffffc000000003ffffffff000c0001ffffffc000000003ffffffff00380001ffffffc000000003ffffffff00380001ffffffc000000003ffffffff00080001ffffffc000000003ffffffff00080001ffffffc000000003ffffffff000c0001ffc001c0007ffc03ffc001ff000ff801ffc001c0007ffc03ffc001ff000ff801ffc001c0007ffc03ffc001ff00000001ffc021c0007fdc03ffc021ff00000001ffc3a1c0007c5c03ffc3a1ff00030001ffc2e1c0007d1c03ffc2e1ff00030001ffc2e1c0007d1c03ffc2e1ff000f8801ffc261c0007d9c03ffc261ff00098801ffc001c0007ffc03ffc001ff00398801ffc001c0007ffc03ffc001ff00398801ffc001c0007ffc03ffc001ff00398801ffc001c0007ffc03ffc001ff00398801ffc001c0007ffc03ffc001ff00099801ffffffc000000003ffffffff000ff001ffffffc000000003ffffffff0003c001ffffffc000000003ffffffff00000001fef81fc00207e003fdf03fff00000001fcc00200067ffb83f9800c7f00000001fcc00200067ffb83f9800c7f000f8001fd8f304004f0cf03fb1e60ff007fe001fd9f314004c0cd03fb3e62ff00f03001fd9f014004c0fd03fb3e02ff00c01001fd9f014004c0fd03fb3e02ff00801801fc1f014007c0fd03f83e02ff00801801fd9f014004c0fd03fb3e02ff00801801fd9f014004c0fd03fb3e02ff01801801fd9f014004c0fd03fb3e02ff01801801fd9f314004c0cd03fb3e62ff01801801fd9f304004c0cf03fb3e60ff01fff801fcc00000067fff83f980007f01fff801fef00fc0020ff003fde01fff01fff801fef00fc0020ff003fde01fff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff00000001ffffffc000000003ffffffff"

async def main(img_hex: str):
    async with BleakClient(ESL_MAC, timeout=30) as client:
        if client.is_connected:
            esl = ESL(client, WRITE_CHARACTERISTIC_UUID)
            await esl.upload_image(img_hex, MAX_CHUNK_SIZE)
        else:
            print(f"Failed to connect to {ESL_MAC}")


if __name__ == "__main__":
    # next_trams = get_next_trams(3)
    # img: Image = make_tram_img(next_trams)
    # img_hex = image2hex(img)
    asyncio.run(main(img_hex))
