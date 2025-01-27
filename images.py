import os
import re
import shutil

# Define paths
md_directory = r"C:\Users\lambo\Documents\Obsidian_Vault\posts"  # Directory containing all .md files
obsidian_image_dir = r"C:\Users\lambo\Documents\Obsidian_Vault\images"  # Location of images inside the Obsidian vault
new_image_dir = r"C:\Users\lambo\Documents\blog-master\static\images"  # Destination for images

# Ensure the new image directory exists
os.makedirs(new_image_dir, exist_ok=True)

# Regex pattern to match ![[/images/example.png]]
image_pattern = re.compile(r'!\[\[\s*(/images/[^]]+\.(?:png|jpg|jpeg|gif|bmp|webp|tiff|svg))\s*\]\]')

# Process each Markdown file in the directory
for file in os.listdir(md_directory):
    if file.endswith(".md"):
        md_file_path = os.path.join(md_directory, file)

        with open(md_file_path, "r", encoding="utf-8") as md_file:
            content = md_file.read()

        # Find all image references
        matches = image_pattern.findall(content)

        if matches:
            updated_content = content

            for image_path in matches:
                # Convert `/images/...` to the actual path
                relative_image_path = image_path.lstrip("/")  # Remove leading `/`
                abs_image_path = os.path.join(obsidian_image_dir, os.path.basename(relative_image_path))

                if os.path.exists(abs_image_path):
                    # Move (or copy) the image to the new directory
                    new_image_path = os.path.join(new_image_dir, os.path.basename(abs_image_path))
                    shutil.copy2(abs_image_path, new_image_path)  # Use copy instead of move

                    # Update Markdown link to point to the new location
                    new_md_path = f"![[{os.path.basename(new_image_path)}]]"
                    updated_content = updated_content.replace(f"![[{image_path}]]", new_md_path)
                    print(f"Copied: {abs_image_path} → {new_image_path}")

            # Write updated content back to the Markdown file
            with open(md_file_path, "w", encoding="utf-8") as md_file:
                md_file.write(updated_content)
            print(f"Updated Markdown: {md_file_path}")

print("✅ Process completed.")
