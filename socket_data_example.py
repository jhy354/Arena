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
            ]  
        }
    ], 
    'timer': 3  # 游戏倒计时时间
}

# Client Send
response = {  # 在./server.py/ResponseHandler(CLASS)中处理
    'action': 'commands',  # 调用handle_commands()
    'value': 
    {
        'commands': 
        [
            {'movement': {  # 调用handle_movement()
                'id': '1', 
                'pos': (531, 781)
            }},
            
            {'animation': {  # 调用handle_animation()
                'id': '1', 
                'skin': 'p_pale', 
                'status': 'idle', 
                'frame_index': 0.79, 
                'face_direction': 'right'
            }}, 
            
            {'bullet': {  # 调用handle_bullet()
                'id': '1', 
                'bullet_list': 
                [{
                    'pos': (124, 750), 
                    'image_path': './assets/game/weapon/gun/bullet/bullet.png', 
                    'damage': 50
                }]
            }}
        ], 
        'id': '1'  # data sender
    }
}

'''
OLD FASHION(老版本用的)
'''

# data sent from client 
client_send = {
    'action': 'commands',
    'value': {
        'commands': [
            {
                'animation': {
                    'dir': 1,
                    'id': '3',
                    'pos': (128.0, 128.0),
                    'stats': {
                        'alive': True,
                        'animating': True,
                        'attack': 5,
                        'attack_speed': 5,
                        'attacking': False,
                        'defense': 0.3,
                        'foreground_idx': 5,
                        'foreground_loc': {
                            'attacking': [
                                (0, 0),
                                (0, 0),
                                (0, -64),
                                (0, -64),
                                (0, -128),
                                (0, -128),
                                (0, -192),
                                (0, -192),
                                (0, -256),
                                (0, -256)],
                            'default': [
                                (0, 0),
                                (0, 0),
                                (0, 0),
                                (0, 0),
                                (0, -64),
                                (0, -64),
                                (0, -64),
                                (0, -64)]
                        },
                        'hp': 100,
                        'max_hp': 100,
                        'move_speed': 8,
                        'moving': False,
                        'speaking': False,
                        'speaking_time': 5000,
                        'text': ''
                    }
                }
            }
        ],
        'id': '3'
    }
}

# data received from server
client_receive = {
    'enemies': [],
    'players': [
        {
            'dir': 0,
            'id': '1',
            'pos': (40.0, 0.0),
            'stats': {
                'alive': True,
                'animating': True,
                'attack': 5,
                'attack_speed': 5,
                'attacking': False,
                'defense': 0.3,
                'foreground_idx': 7,
                'foreground_loc': {
                    'attacking': [
                        (0, 0),
                        (0, 0),
                        (0, -64),
                        (0, -64),
                        (0, -128),
                        (0, -128),
                        (0, -192),
                        (0, -192),
                        (0, -256),
                        (0, -256)
                    ],
                    'default': [
                        (0, 0),
                        (0, 0),
                        (0, 0),
                        (0, 0),
                        (0, -64),
                        (0, -64),
                        (0, -64),
                        (0, -64)
                    ]
                },
                'hp': 100,
                'max_hp': 100,
                'move_speed': 8,
                'moving': False,
                'speaking': False,
                'speaking_time': 5000,
                'text': ''
            }
        },
        {
            'dir': 0,
            'id': '2',
            'pos': (184.0, -40.0),
            'stats': {
                'alive': True,
                'animating': True,
                'attack': 5,
                'attack_speed': 5,
                'attacking': False,
                'defense': 0.3,
                'foreground_idx': 6,
                'foreground_loc': {
                    'attacking': [
                        (0, 0),
                        (0, 0),
                        (0, -64),
                        (0, -64),
                        (0, -128),
                        (0, -128),
                        (0, -192),
                        (0, -192),
                        (0, -256),
                        (0, -256)
                    ],
                    'default': [
                        (0, 0),
                        (0, 0),
                        (0, 0),
                        (0, 0),
                        (0, -64),
                        (0, -64),
                        (0, -64),
                        (0, -64)
                    ]
                },
                'hp': 100,
                'max_hp': 100,
                'move_speed': 8,
                'moving': False,
                'speaking': False,
                'speaking_time': 5000,
                'text': ''
            }
        }
    ],
    'working': True
}
