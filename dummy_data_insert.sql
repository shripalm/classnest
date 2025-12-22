
-- Insert dummy data for classes
INSERT INTO classes (id, name) VALUES
(101, 'Maths & Science'),
(102, 'Coding & Robotics'),
(201, 'Language & Literacy'),
(202, 'Reading & Writing'),
(301, 'Arts & Design'),
(302, 'Music & Performance'),
(401, 'Sports & Fitness'),
(402, 'Physical Education'),
(501, 'Social Studies'),
(502, 'Environmental Studies');

-- Insert dummy data for courses with class_id
INSERT INTO courses (id, name, class_id) VALUES
-- Maths & Science (101)
(1, 'Art & Creativity', 101),
(2, 'Music & Performing Arts', 101),
(3, 'Basic Mathematics', 101),
(4, 'Physics Fundamentals', 101),
(5, 'Chemistry Basics', 101),

-- Coding & Robotics (102)
(6, 'Sports (Team & Individual)', 102),
(7, 'STEM (Science, Tech, Engineering, Math)', 102),
(8, 'Python Programming', 102),
(9, 'Web Development', 102),
(10, 'Robotics Basics', 102),
(11, 'AI & Machine Learning', 102),

-- Language & Literacy (201)
(12, 'Language & Communication', 201),
(13, 'English Grammar', 201),
(14, 'Literature Analysis', 201),
(15, 'Creative Writing', 201),
(16, 'Public Speaking', 201),

-- Reading & Writing (202)
(17, 'Leadership & Life Skills', 202),
(18, 'Advanced Writing', 202),
(19, 'Poetry & Prose', 202),
(20, 'Journalism', 202),

-- Arts & Design (301)
(21, 'Visual Arts', 301),
(22, 'Digital Design', 301),
(23, 'Graphic Design', 301),
(24, 'Painting & Drawing', 301),
(25, 'Sculpture & 3D Art', 301),

-- Music & Performance (302)
(26, 'Instrument Training', 302),
(27, 'Vocal Training', 302),
(28, 'Music Theory', 302),
(29, 'Dance Basics', 302),
(30, 'Theatre & Drama', 302),

-- Sports & Fitness (401)
(31, 'Soccer', 401),
(32, 'Basketball', 401),
(33, 'Tennis', 401),
(34, 'Swimming', 401),
(35, 'Fitness Training', 401),

-- Physical Education (402)
(36, 'Yoga & Flexibility', 402),
(37, 'Martial Arts', 402),
(38, 'Badminton', 402),
(39, 'Cricket', 402),
(40, 'Gymnastics', 402),

-- Social Studies (501)
(41, 'World History', 501),
(42, 'Civics & Government', 501),
(43, 'Economics Basics', 501),
(44, 'Geography & Culture', 501),

-- Environmental Studies (502)
(45, 'Climate & Sustainability', 502),
(46, 'Conservation Biology', 502),
(47, 'Renewable Energy', 502),
(48, 'Environmental Ethics', 502);
