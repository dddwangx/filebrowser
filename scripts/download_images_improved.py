#!/usr/bin/env python3
"""
下载自然风景和动物特写图片
使用Picsum Photos作为备选方案（无需API密钥）
"""
import os
import requests
import json
import time
from pathlib import Path

def download_placeholder_images(num_images=15, output_dir='frontend/public/logos'):
    """
    下载占位图片
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 图片主题和对应的Unsplash搜索关键词
    themes = [
        ('mountain_sunset', 'mountain,sunset,landscape'),
        ('ocean_waves', 'ocean,waves,beach'),
        ('forest_nature', 'forest,trees,nature'),
        ('tiger_portrait', 'tiger,wildlife,animal'),
        ('eagle_flying', 'eagle,bird,sky'),
        ('panda_bamboo', 'panda,bamboo,cute'),
        ('wolf_winter', 'wolf,snow,winter'),
        ('dolphin_ocean', 'dolphin,ocean,water'),
        ('lion_savanna', 'lion,africa,wildlife'),
        ('deer_forest', 'deer,forest,wildlife'),
        ('waterfall_scenic', 'waterfall,nature,scenic'),
        ('aurora_night', 'aurora,night,sky'),
        ('cherry_blossom', 'cherry,blossom,spring'),
        ('butterfly_flower', 'butterfly,flower,macro'),
        ('hummingbird', 'hummingbird,bird,flight')
    ]
    
    downloaded = []
    
    print(f"开始下载 {num_images} 张图片...")
    print("=" * 60)
    
    for i in range(min(num_images, len(themes))):
        theme_name, keywords = themes[i]
        filename = f'logo_{i+1:02d}.jpg'
        filepath = os.path.join(output_dir, filename)
        
        # 如果文件已存在且大小合理，跳过
        if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
            print(f"[{i+1}/{num_images}] ✓ 已存在: {filename}")
            downloaded.append(filename)
            continue
        
        print(f"[{i+1}/{num_images}] 下载: {theme_name}...")
        
        # 尝试多个图片源
        success = False
        
        # 方法1: Unsplash Source (随机图片)
        try:
            url = f'https://source.unsplash.com/800x600/?{keywords}'
            response = requests.get(url, timeout=15, allow_redirects=True)
            if response.status_code == 200 and len(response.content) > 10000:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"  ✓ 成功 (Unsplash): {len(response.content)} bytes")
                downloaded.append(filename)
                success = True
                time.sleep(1.5)  # 避免请求过快
        except Exception as e:
            print(f"  ✗ Unsplash失败: {e}")
        
        # 方法2: Picsum Photos (如果方法1失败)
        if not success:
            try:
                # 使用随机ID
                pic_id = 100 + i * 10
                url = f'https://picsum.photos/800/600?random={pic_id}'
                response = requests.get(url, timeout=15, allow_redirects=True)
                if response.status_code == 200 and len(response.content) > 10000:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"  ✓ 成功 (Picsum): {len(response.content)} bytes")
                    downloaded.append(filename)
                    success = True
                    time.sleep(1)
            except Exception as e:
                print(f"  ✗ Picsum失败: {e}")
        
        # 方法3: 创建彩色占位图（如果都失败）
        if not success:
            print(f"  ⚠ 创建占位图...")
            create_colored_placeholder(filepath, i)
            downloaded.append(filename)
    
    # 保存清单
    manifest = {
        'images': downloaded,
        'themes': [t[0] for t in themes[:num_images]],
        'count': len(downloaded),
        'updated': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    manifest_file = os.path.join(output_dir, 'manifest.json')
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print("=" * 60)
    print(f"✓ 完成！成功处理 {len(downloaded)}/{num_images} 张图片")
    print(f"✓ 保存位置: {output_dir}")
    print(f"✓ 清单文件: {manifest_file}")
    
    return downloaded

def create_colored_placeholder(filepath, index):
    """
    创建简单的彩色占位图（使用PIL如果可用）
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # 创建渐变色背景
        colors = [
            (102, 126, 234),  # 蓝紫
            (118, 75, 162),   # 紫色
            (240, 147, 251),  # 粉紫
            (79, 172, 254),   # 天蓝
            (0, 242, 254),    # 青色
            (255, 107, 107),  # 红色
            (255, 159, 64),   # 橙色
            (255, 206, 86),   # 黄色
            (75, 192, 192),   # 青绿
            (153, 102, 255),  # 紫罗兰
        ]
        
        color = colors[index % len(colors)]
        
        img = Image.new('RGB', (800, 600), color)
        draw = ImageDraw.Draw(img)
        
        # 添加渐变效果
        for y in range(600):
            alpha = y / 600
            new_color = tuple(int(c * (1 - alpha * 0.3)) for c in color)
            draw.line([(0, y), (800, y)], fill=new_color)
        
        # 添加文字
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        text = f"Logo {index + 1}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((800 - text_width) // 2, (600 - text_height) // 2)
        
        draw.text(position, text, fill=(255, 255, 255), font=font)
        
        img.save(filepath, 'JPEG', quality=85)
        
    except ImportError:
        # 如果PIL不可用，创建一个最小的JPEG
        # 这是一个1x1像素的有效JPEG
        minimal_jpeg = bytes([
            0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46,
            0x49, 0x46, 0x00, 0x01, 0x01, 0x01, 0x00, 0x48,
            0x00, 0x48, 0x00, 0x00, 0xFF, 0xDB, 0x00, 0x43,
            0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0xFF, 0xFF, 0xC0, 0x00, 0x0B, 0x08, 0x00, 0x01,
            0x00, 0x01, 0x01, 0x01, 0x11, 0x00, 0xFF, 0xC4,
            0x00, 0x14, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0xFF, 0xDA, 0x00, 0x08,
            0x01, 0x01, 0x00, 0x00, 0x3F, 0x00, 0x7F, 0xFF,
            0xD9
        ])
        with open(filepath, 'wb') as f:
            f.write(minimal_jpeg)

if __name__ == '__main__':
    download_placeholder_images(15)
