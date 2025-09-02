import cv2
import numpy as np
from pathlib import Path
import logging
import os
from typing import List

logger = logging.getLogger(__name__)

def create_timelapse_video(batch_id: str, output_format: str = 'mp4') -> str:
    """
    Create an MP4 timelapse video from images in a batch directory.
    
    Args:
        batch_id: The batch identifier
        output_format: Output format (only 'mp4' supported)
        
    Returns:
        str: Path to the generated MP4 file
    """
    if output_format != 'mp4':
        raise ValueError("Only MP4 format is supported")
        
    batch_dir = Path('output') / batch_id
    if not batch_dir.exists():
        raise FileNotFoundError(f"Batch directory not found: {batch_dir}")
    
    # Find all image files and sort by year
    image_files = list(batch_dir.glob('*.png'))
    if not image_files:
        raise FileNotFoundError(f"No images found in batch directory: {batch_dir}")
    
    # Extract year from filename and sort
    def extract_year(filepath):
        try:
            # Format: img_lat_lon_alt_year.png
            parts = filepath.stem.split('_')
            return int(parts[-1])
        except (ValueError, IndexError):
            return 0
    
    image_files.sort(key=extract_year)
    years = [extract_year(f) for f in image_files]
    
    logger.info(f"Creating MP4 timelapse for years: {years}")
    
    # Generate output filename
    output_filename = f"timelapse_{batch_id}.mp4"
    output_path = batch_dir / output_filename
    
    return create_mp4_timelapse(image_files, years, output_path)

def create_mp4_timelapse(image_files: List[Path], years: List[int], output_path: Path, fps: int = 1) -> str:
    """Create MP4 timelapse video"""
    
    # Read first image to get dimensions
    first_image = cv2.imread(str(image_files[0]))
    if first_image is None:
        raise ValueError(f"Could not read image: {image_files[0]}")
    
    height, width, channels = first_image.shape
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    
    try:
        for i, (image_file, year) in enumerate(zip(image_files, years)):
            # Read image
            img = cv2.imread(str(image_file))
            if img is None:
                logger.warning(f"Could not read image: {image_file}")
                continue
            
            # Resize if needed
            if img.shape[:2] != (height, width):
                img = cv2.resize(img, (width, height))
            
            # Add year overlay
            img_with_year = add_year_overlay(img, year, use_cv2=True)
            
            # Write frame multiple times for longer display (2 seconds per image at 1 fps)
            frame_duration = 2 if fps == 1 else max(1, fps // 2)
            for _ in range(frame_duration):
                video_writer.write(img_with_year)
        
    finally:
        video_writer.release()
    
    logger.info(f"Created MP4 timelapse: {output_path}")
    return str(output_path)

# Removed GIF and WebM functions - only MP4 supported now

def add_year_overlay(img: np.ndarray, year: int, use_cv2: bool = True) -> np.ndarray:
    """Add year overlay to image using OpenCV"""
    if use_cv2:
        # Create a copy to avoid modifying original
        img_copy = img.copy()
        
        # Add semi-transparent background for text
        overlay = img_copy.copy()
        cv2.rectangle(overlay, (10, 10), (200, 80), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, img_copy, 0.3, 0, img_copy)
        
        # Add year text
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2.0
        color = (255, 255, 255)  # White
        thickness = 3
        
        text = str(year)
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = 20
        text_y = 50
        
        cv2.putText(img_copy, text, (text_x, text_y), font, font_scale, color, thickness)
        
        return img_copy
    else:
        return img

# Removed PIL overlay function - only OpenCV version used for MP4

# Removed slideshow HTML function - only MP4 supported now

def get_batch_media_info(batch_id: str) -> dict:
    """Get information about available media files for a batch (MP4 only)"""
    batch_dir = Path('output') / batch_id
    
    info = {
        'batch_id': batch_id,
        'images': [],
        'videos': []
    }
    
    if not batch_dir.exists():
        return info
    
    # Find images
    image_files = list(batch_dir.glob('*.png'))
    for img_file in image_files:
        if not img_file.name.startswith('timelapse_'):
            info['images'].append({
                'filename': img_file.name,
                'path': str(img_file.relative_to(Path('output'))),
                'size': img_file.stat().st_size
            })
    
    # Find MP4 videos only
    mp4_files = list(batch_dir.glob('*.mp4'))
    for video_file in mp4_files:
        info['videos'].append({
            'filename': video_file.name,
            'path': str(video_file.relative_to(Path('output'))),
            'format': 'mp4',
            'size': video_file.stat().st_size
        })
    
    return info
