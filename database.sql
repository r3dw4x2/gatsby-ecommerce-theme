-- Data Entry System Database Schema
-- Run this SQL in your Supabase SQL Editor

-- Create the main data_entries table
CREATE TABLE IF NOT EXISTS data_entries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    category VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_data_entries_name ON data_entries(name);
CREATE INDEX IF NOT EXISTS idx_data_entries_email ON data_entries(email);
CREATE INDEX IF NOT EXISTS idx_data_entries_category ON data_entries(category);
CREATE INDEX IF NOT EXISTS idx_data_entries_created_at ON data_entries(created_at);

-- Add a trigger to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_data_entries_updated_at 
    BEFORE UPDATE ON data_entries 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data (optional)
INSERT INTO data_entries (name, email, phone, category, description) VALUES
('John Doe', 'john.doe@example.com', '+1-555-0123', 'business', 'CEO of Tech Solutions Inc. Primary business contact for partnership discussions.'),
('Jane Smith', 'jane.smith@gmail.com', '+1-555-0124', 'personal', 'Friend from college. Lives in San Francisco, works in tech.'),
('Bob Johnson', 'bob@marketing.com', '+1-555-0125', 'business', 'Marketing director at Digital Agency. Contact for promotional campaigns.'),
('Alice Brown', 'alice.brown@university.edu', '+1-555-0126', 'education', 'Professor of Computer Science. Collaboration on research projects.'),
('Charlie Wilson', 'charlie@health.org', '+1-555-0127', 'health', 'Doctor at City Hospital. Family physician and health consultant.')
ON CONFLICT DO NOTHING;

-- Optional: Create a view for reporting
CREATE OR REPLACE VIEW entry_summary AS
SELECT 
    category,
    COUNT(*) as total_entries,
    COUNT(email) as entries_with_email,
    COUNT(phone) as entries_with_phone,
    MIN(created_at) as first_entry,
    MAX(created_at) as latest_entry
FROM data_entries 
GROUP BY category
ORDER BY total_entries DESC;

-- Grant necessary permissions (adjust as needed for your setup)
-- Note: In Supabase, permissions are typically managed through Row Level Security (RLS)
-- and the dashboard interface. Uncomment and modify as needed:

-- Enable Row Level Security (optional)
-- ALTER TABLE data_entries ENABLE ROW LEVEL SECURITY;

-- Create a policy for authenticated users (optional)
-- CREATE POLICY "Users can view all entries" ON data_entries
--     FOR SELECT USING (true);

-- CREATE POLICY "Users can insert entries" ON data_entries
--     FOR INSERT WITH CHECK (true);

-- CREATE POLICY "Users can update entries" ON data_entries
--     FOR UPDATE USING (true);

-- CREATE POLICY "Users can delete entries" ON data_entries
--     FOR DELETE USING (true);