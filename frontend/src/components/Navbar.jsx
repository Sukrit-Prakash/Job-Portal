import { FaSearch } from "react-icons/fa";
import { IoMdNotificationsOutline } from "react-icons/io";
import { Avatar } from "@/components/ui/avatar";

const Navbar = () => {
  return (
    <nav className="flex items-center justify-between bg-black text-white px-6 py-4">
      <div className="flex items-center gap-4">
        <h1 className="text-xl font-semibold">LuckyJob</h1>
        <ul className="flex gap-6">
          <li className="cursor-pointer">Find Job</li>
          <li className="cursor-pointer">Messages</li>
          <li className="cursor-pointer">Hiring</li>
          <li className="cursor-pointer">Community</li>
          <li className="cursor-pointer">FAQ</li>
        </ul>
      </div>
      <div className="flex items-center gap-4">
        <span>New York, NY</span>
        <IoMdNotificationsOutline size={24} />
        <Avatar>
          <img src="/profile.jpg" alt="Profile" className="w-8 h-8 rounded-full" />
        </Avatar>
      </div>
    </nav>
  );
};

export default Navbar;
