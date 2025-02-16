// models/job.model.js

import mongoose from "mongoose";
const { Schema } = mongoose;

const JobSchema = new Schema(
  {
    title: {
      type: String,
      required: true,
      index: true,
    },
    company: {
      type: String,
      required: true,
      index: true,
    },
    location: {
      type: String,
      index: true,
    },
    description: {
      type: String,
      required: true,
    },
    posted_date: {
      type: Date,
      required: true,
      index: true,
    },
    url: {
      type: String,
      required: true,
    },
    // An array of tags to mark job domains, industries, or categories.
    tags: {
      type: [String],
      index: true,
      default: [],
    },
    // Additional fields for further classification.
    job_type: {
      type: String,
      enum: ["Full Time", "Part Time", "Internship", "Contract", "Remote", "Freelance"],
      index: true,
    },
    salary: {
      type: String,
    },
    skills: {
      type: [String],
      index: true,
      default: [],
    },
  },
  {
    timestamps: true, // Automatically add createdAt and updatedAt timestamps
  }
);

// Create a text index on fields that might be searched together.
JobSchema.index({
  title: "text",
  description: "text",
  company: "text",
  location: "text",
  tags: "text",
  skills: "text",
});

module.exports = mongoose.model("Job", JobSchema);