from PIL import Image, ImageDraw, ImageFont

# Define colors for each tier
tier_colors = {
    1: 'red',
    2: 'orange',
    3: 'yellow',
    4: 'green',
    5: 'blue',
    6: 'indigo',
    7: 'violet'
}

# Create an empty Image with PIL
img = Image.new('RGB', (600, 400), color = (73, 109, 137))
d = ImageDraw.Draw(img)

# Load a true type or open type font file
font = ImageFont.truetype('arial.ttf', 15)

# Example data
data = {
    'name': 'Exa-qvq',
    'steamid': '123456789',
    'steamid64': '1234567891011121314',
    'total_pts': 299628,
    'total_avg_pts': 597,
    'tp_tier_maps': [0, 11, 41, 239, 148, 50, 13, 0],  # T1 to T7
    'maps': {'tier': [121, 272, 239, 150, 65, 63, 23]},
    'tp_avg_tier_pts': [745, 700, 665, 516, 458, 349, 0]
}

# Draw title and stats
d.text((10,10), f"{data['name']} - {data['steamid']} | {data['steamid64']}", fill="white", font=font)
d.text((10, 30), f"Total Points: {data['total_pts']} Average: {data['total_avg_pts']}", fill="white", font=font)
d.text((10, 50), "TP Stats", fill="white", font=font)

# Draw the tier stats
bar_width = 200
bar_height = 20
x = 10
y = 70

for i in range(1, 7):
    tier_key = f'tier{i}'
    percentage = data['tp_tier_maps'][i] / data['maps']['tier'][i]
    color = tier_colors[i]

    # Draw the background bar
    d.rectangle([x, y, x + bar_width, y + bar_height], outline="white", fill=color)

    # Draw the text
    tier_text = f"T{i} {data['tp_tier_maps'][i]}/{data['maps']['tier'][i]} Avg: {data['tp_avg_tier_pts'][i]}"
    d.text((x + 5, y), tier_text, fill="white", font=font)

    y += 30  # Increment y position for the next bar

# Save the image to a file
img.save('updated_stats_image.png')

# Show the image
img.show()
