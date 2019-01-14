insert into contestant
    values
    (1, '316126510034', 'Ajay Raj Nelapudi', 'ANITS', 3),
    (2, '316126510050', 'Shiv Shankar Singh', 'ANITS', 3),
    (3, '901290328430', 'Sai Sri Anagha Garimella', 'GVP', 3),
    (4, '786230304943', 'Gouri Lakshmi Chennuri', 'AU', 3);

insert into duel
    values
    (1, 2),
    (3, 4);

insert into problem
    values
    (1, 1, 'Sum Of N', '...', 1),
    (2, 1, 'Prime Number', '...', 1),
    (3, 2, 'Prime Range', '...', 3),
    (4, 2, 'Factors', '...', 2),
    (5, 3, 'Max Of Array', '...', 2),
    (6, 3, 'Graph Traversal', '...', 6),
    (7, 4, 'Huffman', '...', 10),
    (8, 4, 'Convex Hull', '...', 9);

insert into testcase
    values
    (1, 1, 'input1', 'output1'),
    (2, 1, 'input2', 'output2'),
    (3, 1, 'input3', 'output3'),
    (4, 2, 'input1', 'output1'),
    (5, 2, 'input2', 'output2'),
    (6, 2, 'input3', 'output3'),
    (7, 3, 'input1', 'output1'),
    (8, 3, 'input2', 'output2'),
    (9, 3, 'input3', 'output3'),
    (10, 4, 'input1', 'output1'),
    (11, 4, 'input2', 'output2'),
    (12, 4, 'input3', 'output3'),
    (13, 5, 'input1', 'output1'),
    (14, 5, 'input2', 'output2'),
    (15, 5, 'input3', 'output3'),
    (16, 6, 'input1', 'output1'),
    (17, 6, 'input2', 'output2'),
    (18, 6, 'input3', 'output3'),
    (19, 7, 'input1', 'output1'),
    (20, 7, 'input2', 'output2'),
    (21, 7, 'input3', 'output3'),
    (22, 8, 'input1', 'output1'),
    (23, 8, 'input2', 'output2'),
    (24, 8, 'input3', 'output3');

insert into directory
    values
    ('spec', '/Users/ajayraj/Documents/CodeDuelCursors2019/spec'),
    ('src', '/Users/ajayraj/Documents/CodeDuelCursors2019/src'),
    ('test', '/Users/ajayraj/Documents/CodeDuelCursors2019/test');