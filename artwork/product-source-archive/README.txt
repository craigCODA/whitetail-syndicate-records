Whitetail Shopify Product Archive
=================================

This archive is the source-of-truth set for future artwork.

Scope:
- Hats & Beanies collection
- Gear & Accessories collection

What is included here:
- manifest_all.json
- hats-beanies/products.json
- gear-accessories/products.json
- archive_gallery.html
- download_product_images.py
- download_product_images.ps1
- empty downloads/ folders where the originals should be saved

Important:
The current runtime could not download Shopify CDN images directly because DNS resolution to cdn.shopify.com failed in this environment.
So I created the archive structure plus direct original image URLs and ready-to-run download scripts.

Recommended next step:
Run either download_product_images.py or download_product_images.ps1 on a machine with normal internet access.
That will populate:
  downloads/hats-beanies/
  downloads/gear-accessories/

After that, use only those downloaded originals for future design work.
