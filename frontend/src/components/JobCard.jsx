import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Calendar } from "lucide-react";

const JobCard = ({ job }) => {
  return (
    <Card className="p-4 rounded-2xl shadow-md bg-[${job.bgColor}]">
      <div className="flex justify-between items-center mb-2">
        <div className="flex items-center gap-2 text-gray-600 text-sm">
          <Calendar className="w-4 h-4" />
          <span>{job.date}</span>
        </div>
        <img src={job.companyLogo} alt="company logo" className="w-6 h-6" />
      </div>
      <h3 className="text-lg font-semibold mb-1">{job.title}</h3>
      <p className="text-sm text-gray-500">{job.company}</p>
      <div className="flex flex-wrap gap-1 my-3">
        {job.tags?.map((tag, index) => (
          <Badge key={index} variant="secondary" className="text-xs px-2 py-1">
            {tag}
          </Badge>
        ))}
      </div>
      <p className="text-lg font-bold">${job.salary}/hr</p>
      <p className="text-sm text-gray-500 mb-3">{job.location}</p>
      <Button variant="outline" className="w-full">Details</Button>
    </Card>
  );
};

export default JobCard;
