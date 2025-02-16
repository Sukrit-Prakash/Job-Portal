"use client";
import { useState } from "react";
import { Filter } from "lucide-react";
import { Button } from "@/components/ui/button";

const Sidebar = () => {
  const [filters, setFilters] = useState({
    workingSchedule: "Full time",
    employmentType: "Full day",
  });

  return (
    <aside className="w-72 p-6 bg-white rounded-xl shadow-md">
      <div className="flex flex-col gap-4">
        <h2 className="text-lg font-semibold">Filters</h2>
        
        <div>
          <h3 className="text-sm font-medium mb-2">Working schedule</h3>
          {[
            "Full time",
            "Part time",
            "Internship",
            "Project work",
            "Volunteering",
          ].map((option) => (
            <label key={option} className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="workingSchedule"
                value={option}
                checked={filters.workingSchedule === option}
                onChange={() => setFilters({ ...filters, workingSchedule: option })}
              />
              {option}
            </label>
          ))}
        </div>
        
        <div>
          <h3 className="text-sm font-medium mb-2">Employment type</h3>
          {[
            "Full day",
            "Flexible schedule",
            "Shift work",
            "Distant work",
            "Shift method",
          ].map((option) => (
            <label key={option} className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="employmentType"
                value={option}
                checked={filters.employmentType === option}
                onChange={() => setFilters({ ...filters, employmentType: option })}
              />
              {option}
            </label>
          ))}
        </div>
        
        <Button className="mt-4 flex items-center gap-2">
          <Filter size={16} /> Apply Filters
        </Button>
      </div>
    </aside>
  );
};

export default Sidebar;
