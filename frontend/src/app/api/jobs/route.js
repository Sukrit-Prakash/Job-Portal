// app/api/jobs/route.js

import { NextResponse } from "next/server";
import connectDB from "@/lib/mongodb";
import getJobModel from "@/models/Job";
// import { parse } from "next/dist/build/swc/generated-native";


const DATABASES = ["linkedin", "weworkremotely", "internshala"];

export async function GET(req){
  try {
    await connectDB();

    // const url = new URL(req.url, "http://localhost:3000");
  
      const url = new URL(req.url);
 

    // const page = url.searchparams.get("page") || 1;
    // const page = parseInt(url.searchparams.get("page")) ||1;
    const page = parseInt(url.searchParams.get("page")) || 1;

    const limit = parseInt(url.searchParams.get("limit")) || 10;
    const skip =(page-1)*limit;
    const joblist =[];
    for(const database of DATABASES){
      const job = getJobModel(database);
      const jobs = await job.find().sort({scrapedAt: -1}).skip(skip).limit(limit);
      joblist.push(...jobs);
  }
  
  return NextResponse.json(joblist);
  } catch (error) {
    console.error(error);
    return NextResponse.error(new Error("Failed to fetch jobs"));
    
  }
}




