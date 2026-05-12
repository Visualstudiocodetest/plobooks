-- Migration: Add image_link to article table
ALTER TABLE article ADD COLUMN image_link VARCHAR(500) NULL AFTER description;