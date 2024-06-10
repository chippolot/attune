import subprocess


def is_font_installed(font_family):
    try:
        # Run the fc-list command to check installed fonts
        result = subprocess.run(
            ["fc-list", ":family"], capture_output=True, text=True, check=True
        )

        # Check the output
        fonts = result.stdout.strip().split("\n")
        for font in fonts:
            if font_family.lower() in font.lower():
                return True
        return False
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return False
