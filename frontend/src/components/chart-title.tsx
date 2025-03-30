import type { LucideIcon } from "lucide-react";

export default function ChartTitle({
  title,
  icon: Icon,
}: {
  title: string;
  icon?: LucideIcon;
}) {
  return (
    <h2 className="flex items-center text-lg font-semibold">
      {Icon && <Icon className="mr-2" size={16} />} {title}
    </h2>
  );
}
