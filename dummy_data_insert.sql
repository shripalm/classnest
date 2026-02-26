truncate table subjects CASCADE;
truncate table courses CASCADE;
INSERT INTO courses (id, name) VALUES
(601, 'Speech & Drama - English'),
(602, 'Speech & Drama - Mandarin'),
(603, 'Art & Craft'),
(604, 'Lego Robotics'),
(605, 'Music'),
(606, 'Dance Styles (Ballet, Hip Hop, Contemporary, etc.)'),
(607, 'Academic Tuitions (Math, Science, English, etc.)'),
(608, 'Languages (French, Spanish, etc.)'),
(609, 'Phonics & Early Literacy Classes (Singapore)'),
(610, 'Sports Coaching - Football, Badminton, Swimming, Basketball, Athletics / Running');

INSERT INTO subjects (id, subject_name, course_id) VALUES
(1001, 'Speech & Drama - English', 601),
(1002, 'Speech & Drama - Mandarin', 602),
(1003, 'Art & Craft', 603),
(1004, 'Lego Robotics', 604),
(1005, 'Music', 605),
(1006, 'Ballet Classes (Singapore)', 606),
(1007, 'Hip Hop Classes (Singapore)', 606),
(1008, 'Contemporary Dance Classes (Singapore)', 606),
(1009, 'K-Pop Dance Classes (Singapore)', 606),
(1010, 'Jazz & Lyrical Dance Classes (Singapore)', 606),
(1011, 'Mathematics Tuition (Singapore)', 607),
(1012, 'Science Tuition (Singapore)', 607),
(1013, 'English Tuition (Singapore)', 607),
(1014, 'Mandarin Tuition (Singapore)', 607),
(1015, 'French Language Classes (Singapore)', 608),
(1016, 'Spanish Language Classes (Singapore)', 608),
(1017, 'Japanese Language Classes (Singapore)', 608),
(1018, 'Mandarin Language Classes (Singapore)', 608),
(1019, 'Phonics & Early Literacy Classes (Singapore)', 609),
(1020, 'Football/Soccer Coaching (Singapore)', 610),
(1021, 'Badminton Coaching (Singapore)', 610),
(1022, 'Swimming Coaching (Singapore)', 610),
(1023, 'Basketball Coaching (Singapore)', 610),
(1024, 'Athletics / Running Coaching (Singapore)', 610);