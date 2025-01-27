import os
import re
import shutil

# Define paths
md_directory = r"C:\Users\lambo\Documents\Obsidian_Vault\posts"  # Directory with .md files
obsidian_image_dir = r"C:\Users\lambo\Documents\Obsidian_Vault\images"  # Source images folder
new_image_dir = r"C:\Users\lambo\Documents\blog-master\static\images"  # Hugo's image location

# Ensure the new image directory exists
os.makedirs(new_image_dir, exist_ok=True)

# Regex to match ![[/images/image.png]]
image_pattern = re.compile(r'!\[\[\s*(/images/[^]]+\.(?:png|jpg|jpeg|gif|bmp|webp|tiff|svg))\s*\]\]')

# Process each Markdown file
for file in os.listdir(md_directory):
    if file.endswith(".md"):
        md_file_path = os.path.join(md_directory, file)

        with open(md_file_path, "r", encoding="utf-8") as md_file:
            content = md_file.read()

        # Find all image references
        matches = image_pattern.findall(content)
        updated_content = content

        for image_path in matches:
                # Convert /images/... to a real path
                relative_image_path = image_path.lstrip("/")  # Remove leading "/"
                abs_image_path = os.path.join(obsidian_image_dir, os.path.basename(relative_image_path))

                    # Copy the image to Hugo's directory
                new_image_path = os.path.join(new_image_dir, os.path.basename(abs_image_path))
                shutil.copy2(abs_image_path, new_image_path)  # Copy instead of move

                    # Convert to Hugo format: ![[/images/image.png]] → ![image](/images/image.png)
                hugo_image_syntax = f"![{os.path.basename(new_image_path)}](/images/{os.path.basename(new_image_path)})"
                hugo_image_syntax = hugo_image_syntax.replace(" ", "%20")
                updated_content = updated_content.replace(f"![[{image_path}]]", hugo_image_syntax)
                print(f"Copied: {abs_image_path} → {new_image_path}")

            # Write updated content back to the Markdown file
        with open(md_file_path, "w", encoding="utf-8") as md_file:
            md_file.write(updated_content)
            print(f"Updated Markdown: {md_file_path}")

print("✅ Process completed. Hugo-compatible Markdown is ready.")
