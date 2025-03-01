import sys
import os
from PIL import Image, ImageSequence

def split_gif(input_path, output_dir="gif_frames"):
    try:
        with Image.open(input_path) as gif:
            os.makedirs(output_dir, exist_ok=True)
            print(f"Splitting {input_path} into frames...")
            
            # Initialize canvas and disposal state
            canvas = None
            previous_frame = None
            frame_count = 0
            
            for i, frame in enumerate(ImageSequence.Iterator(gif)):
                # Initialize canvas with first frame
                if canvas is None:
                    canvas = Image.new("RGBA", frame.size)
                
                # Update canvas with current frame
                canvas.paste(frame, (0, 0), frame.convert("RGBA"))
                
                # Save frame with sequential numbering
                canvas.save(os.path.join(output_dir, f"frame_{i:03d}.png"))
                frame_count += 1
                
                # Handle frame disposal
                disposal = frame.info.get('disposal', 0)
                if disposal == 2:  # Restore to background
                    canvas = Image.new("RGBA", frame.size)
                elif disposal == 1:  # Keep frame content
                    previous_frame = canvas.copy()
                elif disposal == 3:  # Restore previous frame
                    if previous_frame:
                        canvas = previous_frame.copy()

            print(f"Successfully saved {frame_count} frames to {output_dir}/")
            
    except FileNotFoundError:
        print(f"Error: File {input_path} not found!")
    except Exception as e:
        print(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python split_gif_to_frames.py [GIF_FILE]")
        sys.exit(1)
        
    split_gif(sys.argv[1])
