truncate table courses;
truncate table classes;

-- Insert new classes
INSERT INTO classes (id, name) VALUES
(601, 'Speech & Drama - English'),
(602, 'Speech & Drama - Mandarin'),
(603, 'Art & Craft'),
(604, 'Lego Robotics'),
(605, 'Music'),
(606, 'Dance'),
(607, 'Academic Tuitions'),
(608, 'Languages'),
(609, 'Phonics & Early Literacy Classes'),
(610, 'Sports Coaching');

-- Insert courses mapped to classes

INSERT INTO courses (id, name, class_id) VALUES

-- Speech & Drama - English (601)
(1001, 'Speech & Drama - English', 601),

-- Speech & Drama - Mandarin (602)
(1002, 'Speech & Drama - Mandarin', 602),

-- Art & Craft (603)
(1003, 'Art & Craft', 603),

-- Lego Robotics (604)
(1004, 'Lego Robotics', 604),

-- Music (605)
(1005, 'Music', 605),

-- Dance (606)
(1006, 'Ballet Classes', 606),
(1007, 'Hip Hop Classes', 606),
(1008, 'Contemporary Dance Classes', 606),
(1009, 'K-Pop Dance Classes', 606),
(1010, 'Jazz & Lyrical Dance Classes', 606),

-- Academic Tuitions (607)
(1011, 'Mathematics Tuition', 607),
(1012, 'Science Tuition', 607),
(1013, 'English Tuition', 607),
(1014, 'Mandarin Tuition', 607),

-- Languages (608)
(1015, 'French', 608),
(1016, 'Spanish', 608),
(1017, 'Japanese', 608),
(1018, 'Mandarin', 608),

-- Phonics & Early Literacy Classes (609)
(1019, 'Phonics & Early Literacy Classes', 609),

-- Sports Coaching (610)
(1020, 'Football/Soccer', 610),
(1021, 'Badminton Coaching', 610),
(1022, 'Swimming', 610),
(1023, 'Basketball', 610),
(1024, 'Athletics / Running', 610);