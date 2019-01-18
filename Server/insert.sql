insert into contestant
    values
    (1, '316126510034', 'Ajay Raj Nelapudi', 'ANITS', 3),
    (2, '316126510050', 'Shiv Shankar Singh', 'ANITS', 3),
    (3, '901290328430', 'Raghu Mylapilli', 'GVP', 3),
    (4, '786230304943', 'Sai Pranav Nistala', 'AU', 3);

insert into duel
    values
    (1, 2),
    (3, 4);

insert into problem
    values
    (1, 1, 'SumOfN', 1),
    (2, 1, 'PrimeNumber', 1),
    (3, 2, 'PrimeRange', 3),
    (4, 2, 'Factors', 2),
    (5, 3, 'MaxOfArray', 2),
    (6, 3, 'GraphTraversal', 6),
    (7, 4, 'Huffman', 10),
    (8, 4, 'ConvexHull', 9);

insert into testcase
    values
    (1, 1, 'input1', 'output1', 5),
    (2, 1, 'input2', 'output2', 5),
    (3, 1, 'input3', 'output3', 10),
    (4, 2, 'input1', 'output1', 5),
    (5, 2, 'input2', 'output2', 5),
    (6, 2, 'input3', 'output3', 10),
    (7, 3, 'input1', 'output1', 5),
    (8, 3, 'input2', 'output2', 5),
    (9, 3, 'input3', 'output3', 10),
    (10, 4, 'input1', 'output1', 5),
    (11, 4, 'input2', 'output2', 5),
    (12, 4, 'input3', 'output3', 10),
    (13, 5, 'input1', 'output1', 5),
    (14, 5, 'input2', 'output2', 5),
    (15, 5, 'input3', 'output3', 10),
    (16, 6, 'input1', 'output1', 5),
    (17, 6, 'input2', 'output2', 5),
    (18, 6, 'input3', 'output3', 10),
    (19, 7, 'input1', 'output1', 5),
    (20, 7, 'input2', 'output2', 5),
    (21, 7, 'input3', 'output3', 10),
    (22, 8, 'input1', 'output1', 5),
    (23, 8, 'input2', 'output2', 5),
    (24, 8, 'input3', 'output3', 10);

insert into score
    values
    (1, 1, 12, NOW()),
    (1, 2, 13, NOW()),
    (1, 3, 9, NOW()),
    (2, 1, 6, NOW()),
    (2, 2, 10, NOW()),
    (2, 3, 12, NOW()),
    (3, 1, 13, NOW()),
    (3, 2, 6, NOW()),
    (3, 3, 4, NOW()),
    (4, 1, 3, NOW()),
    (4, 2, 3, NOW()),
    (4, 3, 1, NOW());


insert into directory
    values
    ('spec', '/Users/ajayraj/Documents/CodeDuelCursors2019/spec'),
    ('src', '/Users/ajayraj/Documents/CodeDuelCursors2019/src'),
    ('test', '/Users/ajayraj/Documents/CodeDuelCursors2019/test');