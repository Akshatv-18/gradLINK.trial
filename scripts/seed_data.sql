-- Seed data for GRADLINK database
USE gradlink_db;

-- Insert sample universities
INSERT INTO accounts_university (name, location, website, description, established_year, created_at) VALUES
('Harvard University', 'Cambridge, MA', 'https://harvard.edu', 'Ivy League research university', 1636, NOW()),
('Stanford University', 'Stanford, CA', 'https://stanford.edu', 'Private research university', 1885, NOW()),
('MIT', 'Cambridge, MA', 'https://mit.edu', 'Institute of Technology', 1861, NOW()),
('UC Berkeley', 'Berkeley, CA', 'https://berkeley.edu', 'Public research university', 1868, NOW()),
('Yale University', 'New Haven, CT', 'https://yale.edu', 'Ivy League university', 1701, NOW());

-- Insert job categories
INSERT INTO jobs_jobcategory (name, description, created_at) VALUES
('Software Engineering', 'Software development and engineering roles', NOW()),
('Data Science', 'Data analysis and machine learning positions', NOW()),
('Product Management', 'Product strategy and management roles', NOW()),
('Marketing', 'Marketing and growth positions', NOW()),
('Finance', 'Financial services and analysis roles', NOW()),
('Consulting', 'Management and strategy consulting', NOW()),
('Healthcare', 'Medical and healthcare positions', NOW()),
('Education', 'Teaching and educational roles', NOW());

-- Insert event categories
INSERT INTO events_eventcategory (name, description, color, created_at) VALUES
('Networking', 'Professional networking events', '#28a745', NOW()),
('Career Development', 'Career growth and development', '#007bff', NOW()),
('Technical Workshops', 'Technical skills and training', '#6f42c1', NOW()),
('Industry Insights', 'Industry trends and insights', '#fd7e14', NOW()),
('Social Events', 'Social gatherings and meetups', '#20c997', NOW());

-- Note: User data should be created through the Django admin or registration process
-- to ensure proper password hashing and user profile creation
