// src/app/page.js

'use client'
import React, { use } from "react";
import Navbar from "@/components/Navbar";
import Sidebar from "@/components/Sidebar";
import JobCard from "@/components/JobCard";
import { useState, useEffect } from "react";
// const jobs = [
//   {
//     id: 1,
//     date: "20 May, 2023",
//     company: "Amazon",
//     title: "Senior UI/UX Designer",
//     type: ["Part time", "Senior level", "Distant"],
//     rate: "$250/hr",
//     location: "San Francisco, CA",
//     logo: "/amazon.png",
//     bgColor: "bg-orange-100",
//   },
//   {
//     id: 2,
//     date: "4 Feb, 2023",
//     company: "Google",
//     title: "Junior UI/UX Designer",
//     type: ["Full time", "Junior level", "Distant"],
//     rate: "$150/hr",
//     location: "California, CA",
//     logo: "/google.png",
//     bgColor: "bg-green-100",
//   },
//   // Add more job listings here
// ];



export default function Dashboard() {
  const [jobs, setJobs] = useState([]);
  const [page, setPage] = useState(1);
  const limit = 10;


 
  const fetchjobs = async () => { 
    try {
      const response = await fetch(`/api/jobs?page=${page}&limit=${limit}`);
      const data = await response.json();
      // setJobs(data);
      setJobs((prevJobs) => [...prevJobs, ...data]); // Append new jobs
    } catch (error) {
      console.error("Error fetching jobs:", error);
    }
  };


  // useEffect(() => {
  //   fetch(`/api/jobs?page=${page}&limit=${limit}`)
  //     .then((res) => res.json())
  //     .then((data) => setJobs(data))
  //     .catch((error) => console.error("Error fetching jobs:", error));
  // }, []);
  useEffect(() => {
    fetchjobs();
  }, [page]);
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <Navbar />
      <div className="flex flex-row p-6">
        <Sidebar />
        <div className="flex-1 px-6">
          <h2 className="text-2xl font-semibold mb-4">Recommended Jobs</h2>
          <div className="grid grid-cols-3 gap-6">

            {jobs.map((job) => (
              <JobCard key={`${job.id}-${job.title}-${Math.random().toString(36).substr(2, 9)}`} job={job} />
            ))}

          </div>
        </div>
      </div>
      {/* <button
        onClick={() => setPage(page + 1)}
        className="mt-4 bg-blue-500 text-white px-4 py-2 rounded"
      >
        Load More Jobs
        // HYDRATION ERROR: Page is not hydrated
      </button> */}
      <button
  onClick={() => setPage((prevPage) => prevPage + 1)}
  className="mt-4 bg-blue-500 text-white px-4 py-2 rounded"
>
  Load More Jobs
</button>

    </div>
  );
}
