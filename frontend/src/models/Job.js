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


const getJobModel = (databaseName) => {
  const db = mongoose.connection.useDb(databaseName);
  return db.models.Job || db.model("Job", JobSchema, "jobs");
};


// module.exports = mongoose.model("Job", JobSchema);

export default getJobModel;




// const JobSchema = new mongoose.Schema(
//   {
//     title: String,
//     company: String,
//     location: String,
//     description: String,
//     posted_date: String, // Keep as string if scraped as empty
//     url: String,
//     tags: [String],
//     job_type: String,
//     salary: String,
//     skills: [String],
//     scraped_at: Date,
//   },
//   { timestamps: true }
// );

