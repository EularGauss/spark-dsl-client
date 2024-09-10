allowed_operators = {
    'string': [
        ('=', 'symbol'),
        ('!=', 'symbol'),
        ('contains', 'method'),
        ('startsWith', 'method'),
        ('endsWith', 'method'),
        ('regex', 'method')
    ],
    'long': [
        ('=', 'symbol'),
        ('!=', 'symbol'),
        ('>', 'symbol'),
        ('<', 'symbol'),
        ('>=', 'symbol'),
        ('<=', 'symbol'),
        ('between', 'method')
    ],
    'double': [
        ('=', 'symbol'),
        ('!=', 'symbol'),
        ('>', 'symbol'),
        ('<', 'symbol'),
        ('>=', 'symbol'),
        ('<=', 'symbol'),
        ('between', 'method')
    ],
    'enum': [
        ('=', 'symbol'),
        ('!=', 'symbol'),
        ('in', 'method')
    ],
    'map': [
        ('containsKey', 'method'),
        ('containsValue', 'method')
    ],
    'array': [
        ('array_contains', 'method'),
        ('in', 'method')
    ],
    'timestamp': [
        ('=', 'symbol'),
        ('!=', 'symbol'),
        ('>', 'symbol'),
        ('<', 'symbol'),
        ('>=', 'symbol'),
        ('<=', 'symbol'),
        ('between', 'method')
    ],
    'null': [
        ('isNull', 'method'),
        ('isNotNull', 'method')
    ]
}
