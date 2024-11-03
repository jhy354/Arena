"""
Socket传输数据样例
"""

# Server Send
status = {
    'map': 1,  # 地图编号
    'bg': 2,  # 背景编号
    'players':  # 游戏中的玩家角色
    [
        {
            'id': '1',  # 角色编号
            'pos': (608, 653),  # 角色坐标
            'skin': 'p_pale',  # 角色皮肤
            'status': 'idle',  # 角色状态机
            'frame_index': 0.86,  # 状态机动画帧索引(取整)
            'face_direction': 'right',  # 角色面向的方向
            'bullet_list':  # 场景中存在的子弹
            [
                {
                    'pos': (1129, 682),  # 子弹坐标
                    'image_path': './assets/game/weapon/gun/bullet/bullet.png',  # 子弹贴图
                    'damage': 50  # 子弹伤害
                }
            ],
            'score': 0
        }
    ], 
    'timer':  # 游戏倒计时时间
    {
        'time': 1,
        'finished': False  # False/True
    }
}

# Client Send
response = {  # 在./server.py/ResponseHandler(CLASS)中处理
    'action': 'commands',  # 调用handle_commands()
    'value': 
    {
        'commands': 
        [
            {
                'movement': {  # 调用handle_movement()
                    'id': '1',
                    'pos': (531, 781)
                }
            },
            
            {
                'animation': {  # 调用handle_animation()
                    'id': '1',
                    'skin': 'p_pale',
                    'status': 'idle',
                    'frame_index': 0.79,
                    'face_direction': 'right'
                }
            },
            
            {
                'bullet': {  # 调用handle_bullet()
                    'id': '1',
                    'bullet_list':
                    [{
                        'pos': (124, 750),
                        'image_path': './assets/game/weapon/gun/bullet/bullet.png',
                        'damage': 50
                    }]
                }
            },

            {
                'score': {  # 调用handle_bullet()
                    'id': '1',
                    'score': 0
                }
            }
        ], 
        'id': '1'  # data sender
    }
}
