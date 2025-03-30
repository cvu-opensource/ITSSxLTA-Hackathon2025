import { Gauge, type LucideIcon, MessagesSquare, MapPin, MessageSquareQuote } from "lucide-react";

export type SiteConfig = typeof siteConfig;
export type Navigation = {
  icon: LucideIcon;
  name: string;
  href: string;
};

export const siteConfig = {
  title: "VisActor Next Template",
  description: "Template for VisActor and Next.js",
};

export const navigations: Navigation[] = [
  {
    icon: Gauge,
    name: "Dashboard",
    href: "/",
  },
  {
    icon: MapPin, // 🔹 Added "Map" icon
    name: "Map",  // 🔹 Added "Map" entry
    href: "/map", // 🔹 This will link to your map page
  },
  {
    name: "Planner",
    href: "/planner",
    icon: MessageSquareQuote, // optional icon
  },
];
