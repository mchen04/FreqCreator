import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, vfx
from pathlib import Path
import math
import colorsys
from typing import Dict

def cleanup_directories(except_dir="generated_frequencies"):
    """
    Clean up all directories except the specified one.
    """
    current_dir = Path.cwd()
    
    for item in current_dir.iterdir():
        if item.is_dir() and item.name != except_dir:
            try:
                shutil.rmtree(item)
                print(f"+ Cleaned directory: {item.name}")
            except Exception as e:
                print(f"- Error cleaning {item.name}: {e}")

class FrequencyVideoGenerator:
    def __init__(
        self,
        audio_folder: str = "generated_frequencies",
        output_folder: str = "output_videos",
        font_path: str = "Roboto-Light.ttf",
        video_duration: int = 300,
        image_size: tuple = (1080, 1920)  # TikTok vertical format
    ):
        self.audio_folder = Path(audio_folder)
        self.output_folder = Path(output_folder)
        self.font_path = font_path
        self.video_duration = video_duration
        self.image_size = image_size
        
        # Create fresh output directories
        self.images_dir = self.output_folder / "images"
        self.descriptions_dir = self.output_folder / "descriptions"
        self.videos_dir = self.output_folder / "videos"
        
        for directory in [self.images_dir, self.descriptions_dir, self.videos_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        print("+ Created fresh output directories")

    def get_frequency_category(self, freq: float) -> str:
        if freq < 4:
            return "Delta waves (0.5-4 Hz): Deep meditation and healing frequency"
        elif freq < 8:
            return "Theta waves (4-8 Hz): Deep relaxation and spiritual connection"
        elif freq < 14:
            return "Alpha waves (8-14 Hz): Relaxation and stress reduction"
        elif freq < 30:
            return "Beta waves (14-30 Hz): Focus and concentration"
        elif freq < 100:
            return "Low frequency: Physical and emotional healing"
        elif freq < 400:
            return "Medium frequency: Balancing and harmonizing"
        else:
            return "High frequency: Spiritual awakening and transformation"

    def generate_description(self, frequency: float) -> str:
        special_frequencies = {
            7.83: "Schumann Resonance: Earth's natural heartbeat frequency. Aligns you with nature's rhythm and promotes deep grounding.",
            174: "Natural Pain Relief: Known to reduce physical and energetic pain. Supports natural healing processes.",
            285: "Energy Field Healing: Influences cellular memory and tissue regeneration.",
            396: "Liberation Frequency: Releases trauma and negative patterns. Grounds and strengthens.",
            417: "Facilitating Change: Clears past trauma and initiates positive transformation.",
            432: "Universal Frequency: Nature's healing frequency. Brings harmony and peace.",
            444: "DNA Healing: Supports cellular repair and spiritual awakening.",
            528: "Miracle Tone: Love frequency. Repairs DNA and brings transformation.",
            639: "Heart Chakra: Enhances love, harmony, and emotional healing.",
            741: "Expression: Awakens intuition and spiritual awareness.",
            852: "Third Eye: Connects to spiritual guidance and inner wisdom.",
            963: "Crown Chakra: Pure divine connection and enlightenment."
        }

        if frequency in special_frequencies:
            description = special_frequencies[frequency]
        else:
            category = self.get_frequency_category(frequency)
            description = f"{frequency} Hz\n\n{category}\n\nThis sacred frequency promotes harmony, balance, and healing. Experience deep transformation through sound."

        description_path = self.descriptions_dir / f"{frequency}Hz_description.txt"
        with open(description_path, 'w', encoding='utf-8') as f:
            f.write(description)
        
        return description

    def generate_image(self, frequency: float) -> str:
        img = Image.new('RGB', self.image_size, 'black')
        draw = ImageDraw.Draw(img)
        
        # Generate color scheme based on frequency
        hue = (frequency % 360) / 360.0
        golden_ratio = 0.618033988749895
        main_hue = (hue + golden_ratio) % 1
        complement_hue = (main_hue + 0.5) % 1
        
        main_color = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(main_hue, 0.8, 0.9))
        complement_color = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(complement_hue, 0.7, 0.8))
        
        center_x, center_y = self.image_size[0] // 2, self.image_size[1] // 2
        max_radius = min(center_x, center_y) * 1.8
        
        num_layers = 100
        for i in range(num_layers):
            phase = (i / num_layers) * 2 * math.pi
            radius = max_radius * (0.2 + 0.8 * (i / num_layers))
            points = []
            
            num_points = 360
            frequency_factor = min(frequency / 200, 5)
            
            for angle in range(num_points):
                rad = math.radians(angle)
                r = radius * (1 + 0.15 * math.sin(frequency_factor * rad + phase))
                r *= (1 + 0.1 * math.cos(3 * frequency_factor * rad + phase))
                r *= (1 + 0.05 * math.sin(5 * frequency_factor * rad + phase))
                
                x = center_x + r * math.cos(rad)
                y = center_y + r * math.sin(rad)
                points.append((x, y))
            
            fade = 1 - (i / num_layers) ** 1.5
            color = main_color if i % 2 == 0 else complement_color
            color = tuple(int(c * fade) for c in color)
            
            if len(points) > 2:
                draw.line(points + [points[0]], fill=color, width=3)
        
        img = img.filter(ImageFilter.GaussianBlur(radius=2))
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.2)
        
        image_path = self.images_dir / f"{frequency}Hz_base_image.jpg"
        img.save(image_path, quality=95)
        return str(image_path)

    def create_text_overlay(self, image_path: str, frequency: float, description: str) -> str:
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        
        try:
            title_font = ImageFont.truetype(self.font_path, 140)
            desc_font = ImageFont.truetype(self.font_path, 80)
        except OSError:
            print("Warning: Using default font")
            title_font = desc_font = ImageFont.load_default()
        
        # Add gradient overlays
        gradient_height = 400
        for y in range(gradient_height):
            alpha = int(180 * (1 - y / gradient_height))
            draw.rectangle(
                [(0, y), (self.image_size[0], y)],
                fill=(0, 0, 0, alpha)
            )
        
        for y in range(gradient_height):
            alpha = int(180 * (y / gradient_height))
            y_pos = self.image_size[1] - gradient_height + y
            draw.rectangle(
                [(0, y_pos), (self.image_size[0], y_pos)],
                fill=(0, 0, 0, alpha)
            )
        
        freq_text = f"{frequency} Hz"
        bbox = draw.textbbox((0, 0), freq_text, font=title_font)
        text_width = bbox[2] - bbox[0]
        x_position = (self.image_size[0] - text_width) // 2
        y_position = 100
        
        # Glow effect
        glow_color = (255, 255, 255, 30)
        for offset in [-2, -1, 1, 2]:
            draw.text((x_position + offset, y_position), freq_text, font=title_font, fill=glow_color)
            draw.text((x_position, y_position + offset), freq_text, font=title_font, fill=glow_color)
        
        draw.text((x_position, y_position), freq_text, font=title_font, fill=(255, 255, 255, 255))
        
        lines = []
        current_line = []
        words = description.split()
        max_width = self.image_size[0] - 120
        
        for word in words:
            current_line.append(word)
            bbox = draw.textbbox((0, 0), " ".join(current_line), font=desc_font)
            if bbox[2] > max_width:
                current_line.pop()
                lines.append(" ".join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(" ".join(current_line))
        
        y_position = self.image_size[1] - (len(lines) * (desc_font.size + 20)) - 150
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=desc_font)
            text_width = bbox[2] - bbox[0]
            x_position = (self.image_size[0] - text_width) // 2
            
            for offset in [-1, 1]:
                draw.text((x_position + offset, y_position), line, font=desc_font, fill=(255, 255, 255, 30))
                draw.text((x_position, y_position + offset), line, font=desc_font, fill=(255, 255, 255, 30))
            
            draw.text((x_position, y_position), line, font=desc_font, fill=(255, 255, 255, 255))
            y_position += desc_font.size + 20
        
        output_path = self.images_dir / f"{frequency}Hz_with_text.jpg"
        image.save(output_path, quality=95)
        return str(output_path)

    def create_transparent_text_overlay(self, frequency: float, description: str) -> str:
        # Create a transparent image for text
        img = Image.new('RGBA', self.image_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        try:
            title_font = ImageFont.truetype(self.font_path, 140)
            desc_font = ImageFont.truetype(self.font_path, 80)
        except OSError:
            print("Warning: Using default font")
            title_font = desc_font = ImageFont.load_default()
        
        # Add gradient overlays
        gradient_height = 400
        for y in range(gradient_height):
            alpha = int(180 * (1 - y / gradient_height))
            draw.rectangle(
                [(0, y), (self.image_size[0], y)],
                fill=(0, 0, 0, alpha)
            )
        
        for y in range(gradient_height):
            alpha = int(180 * (y / gradient_height))
            y_pos = self.image_size[1] - gradient_height + y
            draw.rectangle(
                [(0, y_pos), (self.image_size[0], y_pos)],
                fill=(0, 0, 0, alpha)
            )
        
        # Draw frequency text with glow
        freq_text = f"{frequency} Hz"
        bbox = draw.textbbox((0, 0), freq_text, font=title_font)
        text_width = bbox[2] - bbox[0]
        x_position = (self.image_size[0] - text_width) // 2
        y_position = 100
        
        # Glow effect
        for offset in [-2, -1, 1, 2]:
            draw.text((x_position + offset, y_position), freq_text, font=title_font, fill=(255, 255, 255, 30))
            draw.text((x_position, y_position + offset), freq_text, font=title_font, fill=(255, 255, 255, 30))
        
        draw.text((x_position, y_position), freq_text, font=title_font, fill=(255, 255, 255, 255))
        
        # Draw description with word wrap
        lines = []
        current_line = []
        words = description.split()
        max_width = self.image_size[0] - 120
        
        for word in words:
            current_line.append(word)
            bbox = draw.textbbox((0, 0), " ".join(current_line), font=desc_font)
            if bbox[2] > max_width:
                current_line.pop()
                lines.append(" ".join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(" ".join(current_line))
        
        y_position = self.image_size[1] - (len(lines) * (desc_font.size + 20)) - 150
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=desc_font)
            text_width = bbox[2] - bbox[0]
            x_position = (self.image_size[0] - text_width) // 2
            
            for offset in [-1, 1]:
                draw.text((x_position + offset, y_position), line, font=desc_font, fill=(255, 255, 255, 30))
                draw.text((x_position, y_position + offset), line, font=desc_font, fill=(255, 255, 255, 30))
            
            draw.text((x_position, y_position), line, font=desc_font, fill=(255, 255, 255, 255))
            y_position += desc_font.size + 20
        
        text_overlay_path = self.images_dir / f"{frequency}Hz_text_overlay.png"
        img.save(text_overlay_path, format='PNG')
        return str(text_overlay_path)

    def create_video(self, frequency: float, audio_path: str, image_path: str) -> str:
        audio_clip = AudioFileClip(audio_path).set_duration(self.video_duration)
        
        # Create base image without text
        base_image_path = self.generate_image(frequency)
        base_clip = ImageClip(base_image_path).set_duration(self.video_duration)
        
        # Create text overlay
        description = self.generate_description(frequency)
        text_overlay_path = self.create_transparent_text_overlay(frequency, description)
        text_clip = ImageClip(text_overlay_path).set_duration(self.video_duration)
        
        # Apply pulse effect only to base image
        def modify_time(t):
            pulse = 1 + 0.02 * math.sin(2 * math.pi * t / 10)  # Subtle pulse
            return pulse
        
        # Create pulsing background
        pulsing_clip = base_clip.fx(vfx.resize, modify_time)
        
        # Composite the stable text over the pulsing background
        final_clip = CompositeVideoClip([pulsing_clip, text_clip]).set_audio(audio_clip)
        
        video_path = self.videos_dir / f"{frequency}Hz_video.mp4"
        
        final_clip.write_videofile(
            str(video_path),
            fps=30,
            codec="libx264",
            audio_codec="aac",
            bitrate="8000k",
            threads=4
        )
        
        return str(video_path)

    def process_frequency(self, frequency: float) -> Dict[str, str]:
        print(f"\nProcessing {frequency} Hz...")
        
        try:
            description = self.generate_description(frequency)
            print(f"+ Generated description")
            
            image_path = self.generate_image(frequency)
            print(f"+ Generated image")
            
            image_with_text = self.create_text_overlay(image_path, frequency, description)
            print(f"+ Added text overlay")
            
            audio_path = self.audio_folder / f"{frequency}Hz.mp3"
            if not audio_path.exists():
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
                
            video_path = self.create_video(frequency, str(audio_path), image_with_text)
            print(f"+ Created video: {video_path}")
            
            return {
                "description": str(self.descriptions_dir / f"{frequency}Hz_description.txt"),
                "image": image_path,
                "image_with_text": image_with_text,
                "video": video_path
            }
        except Exception as e:
            print(f"Error processing {frequency} Hz: {str(e)}")
            raise

def main():
    print("\nCleaning up directories...")
    cleanup_directories()

    if not Path("generated_frequencies").exists():
        print("Error: 'generated_frequencies' folder not found!")
        print("Please make sure your audio files are in the 'generated_frequencies' folder.")
        return

    frequencies = [
        174, 285, 396, 417, 432, 444, 528, 639, 741, 852,
        963, 100, 111, 120, 144, 174, 200, 210, 222, 285,
        300, 333, 350, 396, 417, 432, 444, 480, 500, 528,
        540, 555, 582, 600, 639, 693, 700, 741, 777, 800,
        852, 888, 900, 936, 963, 1000, 1020, 1111, 1200, 1222,
        136.1, 150, 174, 194, 210, 285, 324, 417, 528, 600,
        639, 852, 963, 7.83, 3, 6, 8, 10, 12, 15,
        20, 25, 30, 40, 50, 60, 70, 80, 90, 100,
        150, 200, 250, 300, 350, 400, 450, 500, 550, 600
    ]
    
    print("\nInitializing video generator...")
    
    generator = FrequencyVideoGenerator(
        audio_folder="generated_frequencies",
        output_folder="output_videos",
        video_duration=300
    )
    
    print("\nStarting video generation process...")
    
    for freq in frequencies:
        try:
            results = generator.process_frequency(freq)
            print(f"\nSuccessfully processed {freq} Hz:")
            for key, path in results.items():
                print(f"  + {key}: {path}")
        except Exception as e:
            print(f"- Failed to process {freq} Hz: {str(e)}")
            continue

if __name__ == "__main__":
    try:
        print("\n=== Frequency Video Generator for TikTok ===")
        print("Initializing with cleanup...")
        main()
        print("\nProcess completed!")
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
        print("Partial results have been saved")
    except Exception as e:
        print(f"\n\nAn error occurred: {str(e)}")
        print("Please check your input files and try again")
    finally:
        print("\n=== Summary ===")
        print("- Check the output_videos folder for your generated content")
        print("- Each frequency has its own video file")
        print("- Videos are optimized for TikTok (1080x1920)")
        print("\nThank you for using the Frequency Video Generator!")