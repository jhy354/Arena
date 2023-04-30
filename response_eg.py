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
