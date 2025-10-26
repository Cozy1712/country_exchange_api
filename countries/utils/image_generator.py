import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from countries.models import Country


def generate_summary_image():
    """
    Generates a summary image (cache/summary.png)
    showing total countries, top 5 by GDP, and last refresh time.
    """
    os.makedirs(os.path.join(settings.BASE_DIR, "cache"), exist_ok=True)
    img_path = os.path.join(settings.BASE_DIR, "cache", "summary.png")

    total = Country.objects.count()
    top_countries = Country.objects.order_by("-estimated_gdp")[:5]
    last_refresh = (
        Country.objects.order_by("-last_refreshed_at")
        .values_list("last_refreshed_at", flat=True)
        .first()
    )

    img = Image.new("RGB", (900, 600), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Font handling (fallback if truetype unavailable)
    try:
        font_title = ImageFont.truetype("arial.ttf", 36)
        font_body = ImageFont.truetype("arial.ttf", 24)
    except Exception:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()

    # Title
    draw.text((30, 30), "Country Summary Report", fill="black", font=font_title)

    draw.text(
        (30, 100),
        f"Total Countries: {total}",
        fill="blue",
        font=font_body,
    )

    draw.text((30, 150), "Top 5 Countries by Estimated GDP:", fill="black", font=font_body)
    y = 190
    for idx, c in enumerate(top_countries, start=1):
        line = f"{idx}. {c.name} - {c.estimated_gdp:,.2f}"
        draw.text((50, y), line, fill="darkgreen", font=font_body)
        y += 40

    draw.text(
        (30, y + 30),
        f"Last Refreshed: {last_refresh.strftime('%Y-%m-%d %H:%M:%S') if last_refresh else 'N/A'}",
        fill="gray",
        font=font_body,
    )

    draw.text(
        (30, y + 80),
        f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        fill="gray",
        font=font_body,
    )

    img.save(img_path)
    return img_path
