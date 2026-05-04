#!/usr/bin/env python3
"""
Filebrowser用户管理脚本
生成管理员和随机用户凭据
"""
import json
import random
import string
import hashlib
import os
from datetime import datetime

def generate_password(length=12):
    """生成随机密码"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def generate_username():
    """生成随机用户名"""
    adjectives = ['happy', 'sunny', 'bright', 'swift', 'clever', 'brave', 'calm', 'wise', 'kind', 'cool']
    nouns = ['tiger', 'eagle', 'dolphin', 'panda', 'wolf', 'fox', 'bear', 'lion', 'hawk', 'deer']
    return f"{random.choice(adjectives)}_{random.choice(nouns)}_{random.randint(100, 999)}"

def hash_password(password):
    """简单的密码哈希（实际使用中filebrowser会用bcrypt）"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_users(num_users=20):
    """生成用户凭据"""
    users = []
    
    # 生成管理员
    admin_password = generate_password(16)
    admin = {
        'id': 1,
        'username': 'admin',
        'password': admin_password,
        'password_hash': hash_password(admin_password),
        'scope': '/srv',
        'locale': 'zh-cn',
        'viewMode': 'list',
        'perm': {
            'admin': True,
            'execute': True,
            'create': True,
            'rename': True,
            'modify': True,
            'delete': True,
            'share': True,
            'download': True
        },
        'commands': [],
        'lockPassword': False,
        'hideDotfiles': False
    }
    users.append(admin)
    
    # 生成普通用户
    for i in range(num_users):
        username = generate_username()
        password = generate_password()
        user = {
            'id': i + 2,
            'username': username,
            'password': password,
            'password_hash': hash_password(password),
            'scope': f'/srv/users/{username}',
            'locale': 'zh-cn',
            'viewMode': 'list',
            'perm': {
                'admin': False,
                'execute': True,
                'create': True,
                'rename': True,
                'modify': True,
                'delete': True,
                'share': True,
                'download': True
            },
            'commands': [],
            'lockPassword': False,
            'hideDotfiles': False
        }
        users.append(user)
    
    return users

def save_credentials(users, output_dir='config'):
    """保存凭据到文件"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存完整的用户信息（包含明文密码）
    credentials_file = os.path.join(output_dir, 'user_credentials.json')
    with open(credentials_file, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)
    
    # 保存简化的登录凭据列表
    login_info = []
    for user in users:
        login_info.append({
            'username': user['username'],
            'password': user['password'],
            'role': 'admin' if user['perm']['admin'] else 'user'
        })
    
    login_file = os.path.join(output_dir, 'login_credentials.txt')
    with open(login_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("Filebrowser 登录凭据\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        for info in login_info:
            f.write(f"用户名: {info['username']}\n")
            f.write(f"密码: {info['password']}\n")
            f.write(f"角色: {info['role']}\n")
            f.write("-" * 60 + "\n")
    
    print(f"✓ 凭据已保存到: {credentials_file}")
    print(f"✓ 登录信息已保存到: {login_file}")
    print(f"\n管理员凭据:")
    print(f"  用户名: admin")
    print(f"  密码: {users[0]['password']}")

if __name__ == '__main__':
    print("正在生成Filebrowser用户凭据...")
    users = generate_users(20)
    save_credentials(users)
    print(f"\n✓ 成功生成 {len(users)} 个用户（1个管理员 + 20个普通用户）")
