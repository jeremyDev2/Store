import urllib.request
import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Category, Product

PHONES = [
    {
        "name": "Apple iPhone 16 Pro Max 256GB Black Titanium",
        "slug": "apple-iphone-16-pro-max-256gb-black",
        "price": "62999.00",
        "stock": 8,
        "description": (
            "Apple iPhone 16 Pro Max. Display: 6.9\" Super Retina XDR OLED, 2868×1320, 460 ppi, ProMotion 120Hz. "
            "Chip: Apple A18 Pro (3nm, 6-core CPU, 6-core GPU). "
            "Camera: 48MP main (Fusion), 48MP ultrawide, 12MP 5x telephoto. Front: 12MP TrueDepth. "
            "Storage: 256GB. RAM: 8GB. Battery: 4685 mAh, MagSafe 25W. "
            "5G, Wi-Fi 7, Bluetooth 5.3, USB-C 3 (USB 3.2). Face ID. IP68. "
            "Color: Black Titanium. iOS 18."
        ),
        "image_url": "https://img.jabko.ua/image/cache/catalog/Apple/iPhone/iPhone-16-Pro-Max/Black-Titanium/apple-iphone-16-pro-max-black-titanium-500x500.jpg",
        "category": "Smartphones",
    },
    {
        "name": "Apple iPhone 16 128GB Ultramarine",
        "slug": "apple-iphone-16-128gb-ultramarine",
        "price": "38999.00",
        "stock": 15,
        "description": (
            "Apple iPhone 16. Display: 6.1\" Super Retina XDR OLED, 2556×1179, 460 ppi, 60Hz. "
            "Chip: Apple A18 (3nm, 6-core CPU, 5-core GPU). "
            "Camera: 48MP main (Fusion), 12MP ultrawide. Front: 12MP TrueDepth. "
            "Storage: 128GB. RAM: 8GB. Battery: 3561 mAh, MagSafe 25W. "
            "Camera Control button. 5G, Wi-Fi 7, Bluetooth 5.3, USB-C 2. Face ID. IP68. "
            "Color: Ultramarine. iOS 18."
        ),
        "image_url": "https://img.jabko.ua/image/cache/catalog/Apple/iPhone/iPhone-16/Ultramarine/apple-iphone-16-ultramarine-500x500.jpg",
        "category": "Smartphones",
    },
    {
        "name": "Apple iPhone 15 128GB Black",
        "slug": "apple-iphone-15-128gb-black",
        "price": "29999.00",
        "stock": 20,
        "description": (
            "Apple iPhone 15. Display: 6.1\" Super Retina XDR OLED, 2556×1179, 460 ppi, 60Hz. "
            "Chip: Apple A16 Bionic (4nm, 6-core CPU, 5-core GPU). "
            "Camera: 48MP main, 12MP ultrawide. Front: 12MP TrueDepth. "
            "Storage: 128GB. RAM: 6GB. Battery: 3349 mAh, MagSafe 15W. "
            "Dynamic Island. 5G, Wi-Fi 6, Bluetooth 5.3, USB-C 2. Face ID. IP68. "
            "Color: Black. iOS 17, upgradable to iOS 18."
        ),
        "image_url": "https://img.jabko.ua/image/cache/catalog/Apple/iPhone/iPhone-15/Black/apple-iphone-15-black-500x500.jpg",
        "category": "Smartphones",
    },
]

PRODUCTS = [
    {
        "name": "Gaming PC RTX 5090 Core Ultra 9 285K 64GB",
        "slug": "gaming-pc-rtx-5090-core-ultra9-285k-64gb",
        "price": "350515.00",
        "stock": 3,
        "description": (
            "Top-tier gaming PC. GPU: GeForce RTX 5090 32GB. "
            "CPU: Intel Core Ultra 9 285K (24 cores). "
            "RAM: 64GB DDR5. Storage: 2TB SSD. "
            "PSU: 1200W. Case: Gamemax Infinity Pro Black. "
            "Includes Windows 10/11, drivers, stress testing."
        ),
        "image_url": "https://it-blok.com.ua/image/cache/catalog/Cases/Gamemax-Infinity-Pro-Black/Gamemax-Infinity-Pro-Black-500x500.png",
        "category": "Gaming PCs",
    },
    {
        "name": "Gaming PC RTX 5080 i9 13900KF 64GB",
        "slug": "gaming-pc-rtx-5080-i9-13900kf-64gb",
        "price": "161549.00",
        "stock": 4,
        "description": (
            "High-end gaming PC. GPU: GeForce RTX 5080 16GB. "
            "CPU: Intel Core i9-13900KF (24 cores, 32 threads, 5.8 GHz boost). "
            "RAM: 64GB DDR4. Storage: 2TB SSD. "
            "Motherboard: Gigabyte B760 DS3H DDR4. PSU: Cougar GEX X2 1000W PCIe5. "
            "Case: Gamemax Infinity Pro Black."
        ),
        "image_url": "https://it-blok.com.ua/image/cache/catalog/Cases/Gamemax-Infinity-Pro-Black/Gamemax-Infinity-Pro-Black-500x500.png",
        "category": "Gaming PCs",
    },
    {
        "name": "Gaming PC RX 9070 XT R9 7900X 32GB",
        "slug": "gaming-pc-rx-9070-xt-r9-7900x-32gb",
        "price": "113747.00",
        "stock": 5,
        "description": (
            "AMD flagship gaming PC. GPU: Radeon RX 9070 XT 16GB GDDR7. "
            "CPU: AMD Ryzen 9 7900X (12 cores, 24 threads, 5.6 GHz boost). "
            "RAM: 32GB DDR5. Storage: 1TB SSD. "
            "PSU: 750W. Case: GameMax Defender Mesh Black. "
            "Excellent for 4K gaming and Ray Tracing."
        ),
        "image_url": "https://it-blok.com.ua/image/cache/catalog/Cases/Gamemax-Defender-Mesh-Black/Gamemax-Defender-Mesh-Black-500x500.png",
        "category": "Gaming PCs",
    },
    {
        "name": "Gaming PC RTX 5070 Ti R7 9800X3D 32GB",
        "slug": "gaming-pc-rtx-5070-ti-r7-9800x3d-32gb",
        "price": "127949.00",
        "stock": 6,
        "description": (
            "Performance gaming PC. GPU: GeForce RTX 5070 Ti 16GB. "
            "CPU: AMD Ryzen 7 9800X3D (8 cores, 16 threads, 5.2 GHz boost). "
            "RAM: 32GB DDR5 6000 MHz. Storage: 1TB SSD. "
            "Motherboard: Asus PRIME B850M-K. PSU: Chieftec Vega M 850W PCIe5. "
            "Case: Gamemax Vista COC AB."
        ),
        "image_url": "https://it-blok.com.ua/image/cache/catalog/Cases/Gamemax-Vista-COC-AB/Gamemax-Vista-COC-AB-500x500.png",
        "category": "Gaming PCs",
    },
    {
        "name": "Gaming PC RTX 5060 Ti 16GB R9 7900X 32GB",
        "slug": "gaming-pc-rtx-5060-ti-r9-7900x-32gb",
        "price": "102413.00",
        "stock": 7,
        "description": (
            "Mid-high gaming PC. GPU: GeForce RTX 5060 Ti 16GB. "
            "CPU: AMD Ryzen 9 7900X (12 cores, 24 threads). "
            "RAM: 32GB DDR5. Storage: 1TB SSD. "
            "Motherboard: Gigabyte B850. PSU: 700W. "
            "Case: GameMax Defender Mesh Black."
        ),
        "image_url": "https://it-blok.com.ua/image/cache/catalog/Cases/Gamemax-Defender-Mesh-Black/Gamemax-Defender-Mesh-Black-500x500.png",
        "category": "Gaming PCs",
    },
    {
        "name": "Gaming PC RTX 5060 Ti 16GB R7 8700F 32GB",
        "slug": "gaming-pc-rtx-5060-ti-r7-8700f-32gb",
        "price": "81760.00",
        "stock": 8,
        "description": (
            "Mid-range gaming PC. GPU: GeForce RTX 5060 Ti 16GB. "
            "CPU: AMD Ryzen 7 8700F (8 cores, 16 threads). "
            "RAM: 32GB DDR5. Storage: 1TB SSD. "
            "Motherboard: Asus A620M-K. PSU: 700W. "
            "Case: PCCooler C3D310 ARGB."
        ),
        "image_url": "https://it-blok.com.ua/image/cache/catalog/Cases/PCCooler-C3D310-ARGB-Black/PCCooler-C3D310-ARGB-Black-367x367.png.pagespeed.ce.Mit9kQVurk.png",
        "category": "Gaming PCs",
    },
    {
        "name": "Gaming PC RTX 5060 8GB i5 12400F 16GB",
        "slug": "gaming-pc-rtx-5060-i5-12400f-16gb",
        "price": "48026.00",
        "stock": 10,
        "description": (
            "Entry gaming PC. GPU: GeForce RTX 5060 8GB GDDR6. "
            "CPU: Intel Core i5-12400F (6 cores, 12 threads, 4.4 GHz boost). "
            "RAM: 16GB DDR4. Storage: 1TB SSD. "
            "Motherboard: MSI H610M-E PRO. PSU: 600W. "
            "Case: GameMax Edge. Supports Full HD gaming with Ray Tracing and DLSS 3."
        ),
        "image_url": "https://it-blok.com.ua/image/cache/catalog/Cases/Gamemax-Edge/Gamemax-Edge-500x500.png",
        "category": "Gaming PCs",
    },
    {
        "name": "Gaming PC RTX 5050 i5 14400F 16GB",
        "slug": "gaming-pc-rtx-5050-i5-14400f-16gb",
        "price": "44710.00",
        "stock": 12,
        "description": (
            "Budget gaming PC. GPU: GeForce RTX 5050 8GB. "
            "CPU: Intel Core i5-14400F (10 cores, 16 threads). "
            "RAM: 16GB DDR4 3200 MHz. Storage: 480GB SSD. "
            "Motherboard: Gigabyte H610M K. PSU: 1stPlayer 600W. "
            "Case: Vinga Creep."
        ),
        "image_url": "https://it-blok.com.ua/image/cache/catalog/Cases/Vinga-Creep/vinga-creep-500x500.png",
        "category": "Gaming PCs",
    },
    {
        "name": "Optimal Gaming R5 5500 RTX 4060 16GB",
        "slug": "optimal-gaming-r5-5500-rtx-4060-16gb",
        "price": "43098.00",
        "stock": 15,
        "description": (
            "Affordable gaming PC. GPU: GeForce RTX 4060 8GB. "
            "CPU: AMD Ryzen 5 5500 (6 cores, 12 threads, 3.6-4.2 GHz). "
            "RAM: 16GB DDR4 3200 MHz. Storage: 1TB SSD. "
            "Motherboard: Asus PRIME A520M-R. PSU: 1stPlayer 600W. "
            "Case: 1stPlayer F3-A White."
        ),
        "image_url": "https://it-blok.com.ua/image/cache/catalog/Cases/1stPlayer-F3-A-4F1-WH-White/1stPlayer-F3-A-4F1-WH-White-500x500.png",
        "category": "Gaming PCs",
    },
    {
        "name": "Optimal Gaming i5 10400F RTX 4060 16GB",
        "slug": "optimal-gaming-i5-10400f-rtx-4060-16gb",
        "price": "44845.00",
        "stock": 14,
        "description": (
            "Affordable Intel gaming PC. GPU: GeForce RTX 4060 8GB. "
            "CPU: Intel Core i5-10400F (6 cores, 12 threads). "
            "RAM: 16GB DDR4. Storage: 1TB SSD. "
            "Motherboard: H510M-K. PSU: 600W. "
            "Case: Vinga Creep."
        ),
        "image_url": "https://it-blok.com.ua/image/cache/catalog/Cases/Vinga-Creep/vinga-creep-500x500.png",
        "category": "Gaming PCs",
    },
    {
        "name": "Progressive Gaming R7 5700X RTX 4070 32GB",
        "slug": "progressive-gaming-r7-5700x-rtx-4070-32gb",
        "price": "70112.00",
        "stock": 9,
        "description": (
            "Progressive gaming PC. GPU: GeForce RTX 4070 12GB. "
            "CPU: AMD Ryzen 7 5700X (8 cores, 16 threads). "
            "RAM: 32GB DDR4. Storage: 1TB SSD. "
            "Motherboard: Asus PRIME B550M-K. PSU: 700W. "
            "Case: 1stPlayer Mi2-A Black. Includes 3-year warranty."
        ),
        "image_url": "https://it-blok.com.ua/image/cache/catalog/Cases/1stPlayer-Mi2-A-BK-2F7R-1F7-Black/1stPlayer-Mi2-A-BK-2F7R-1F7-Black-367x367.png.pagespeed.ce.j0z0nCiiOa.png",
        "category": "Gaming PCs",
    },
]

class Command(BaseCommand):
    help = "Seed database with sample products"

    def handle(self, *args, **kwargs):
        gaming_category, _ = Category.objects.get_or_create(
            slug="gaming-pcs",
            defaults={"name": "Gaming PCs"},
        )
        phones_category, _ = Category.objects.get_or_create(
            slug="smartphones",
            defaults={"name": "Smartphones"},
        )
        self.stdout.write("Categories ready.")

        all_products = (
            [(data, phones_category) for data in PHONES] +
            [(data, gaming_category) for data in PRODUCTS]
        )

        for data, category in all_products:
            if Product.objects.filter(slug=data["slug"]).exists():
                self.stdout.write(f"  skip: {data['name']}")
                continue

            product = Product(
                name=data["name"],
                slug=data["slug"],
                price=data["price"],
                stock=data["stock"],
                description=data["description"],
                category=category,
                is_active=True,
            )

            try:
                req = urllib.request.Request(
                    data["image_url"],
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                with urllib.request.urlopen(req, timeout=10) as response:
                    image_data = response.read()
                filename = data["slug"] + ".png"
                product.image.save(filename, ContentFile(image_data), save=False)
            except Exception as e:
                self.stdout.write(f"  image failed for {data['name']}: {e}")

            product.save()
            self.stdout.write(f"  created: {data['name']}")

        self.stdout.write(self.style.SUCCESS("Done."))
