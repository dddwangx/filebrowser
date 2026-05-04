#!/usr/bin/env python3
"""
从必应搜索下载自然风景和动物特写图片
"""
import os
import requests
import json
import time
from urllib.parse import quote

def download_bing_images(query, num_images=15, output_dir='frontend/public/logos'):
    """
    使用必应图片搜索API下载图片
    注意：这里使用模拟的方式，实际生产环境需要API密钥
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 预定义的图片主题
    themes = [
        'mountain landscape sunset',
        'ocean waves beach',
        'forest trees nature',
        'tiger close up portrait',
        'eagle flying sky',
        'panda bamboo forest',
        'wolf snow winter',
        'dolphin ocean water',
        'lion savanna africa',
        'deer forest wildlife',
        'waterfall nature scenic',
        'aurora borealis night',
        'cherry blossom spring',
        'butterfly flower macro',
        'hummingbird flight'
    ]
    
    # 使用Unsplash API（免费，无需密钥的随机图片）
    downloaded = []
    
    for i, theme in enumerate(themes[:num_images]):
        try:
            # 使用Unsplash的随机图片API
            keywords = theme.replace(' ', ',')
            url = f'https://source.unsplash.com/800x600/?{keywords}'
            
            print(f"正在下载图片 {i+1}/{num_images}: {theme}...")
            
            response = requests.get(url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                filename = f'logo_{i+1:02d}.jpg'
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                downloaded.append(filename)
                print(f"  ✓ 已保存: {filename}")
                time.sleep(1)  # 避免请求过快
            else:
                print(f"  ✗ 下载失败: HTTP {response.status_code}")
        except Exception as e:
            print(f"  ✗ 错误: {e}")
    
    # 保存图片列表
    manifest_file = os.path.join(output_dir, 'manifest.json')
    with open(manifest_file, 'w') as f:
        json.dump({
            'images': downloaded,
            'themes': themes[:num_images],
            'count': len(downloaded)
        }, f, indent=2)
    
    print(f"\n✓ 成功下载 {len(downloaded)} 张图片到 {output_dir}")
    return downloaded

if __name__ == '__main__':
    print("开始下载必应图片...")
    download_bing_images('nature wildlife', 15)
