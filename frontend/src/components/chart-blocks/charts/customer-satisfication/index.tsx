import { SmilePlus, ThumbsDown, ThumbsUp } from "lucide-react";
import {
  customerSatisfication,
  totalCustomers,
} from "@/data/customer-satisfication";
import ChartTitle from "../../components/chart-title";
import LinearProgress from "./components/linear-progress";

const customerSatisficationOptions = [
  {
    label: "Low",
    color: "#5fb67a",
    percentage: customerSatisfication.positive,
    icon: <ThumbsUp className="h-6 w-6" stroke="#5fb67a" fill="#5fb67a" />,
  },
  {
    label: "Medium",
    color: "#f5c36e",
    percentage: customerSatisfication.neutral,
    icon: <ThumbsUp className="h-6 w-6" stroke="#f5c36e" fill="#f5c36e" />,
  },
  {
    label: "High",
    color: "#da6d67",
    percentage: customerSatisfication.negative,
    icon: <ThumbsDown className="h-6 w-6" stroke="#da6d67" fill="#da6d67" />,
  },
];

export default function CustomerSatisfication() {
  return (
    <section className="flex h-full flex-col gap-2">
      <ChartTitle title="Priority Ratio" icon={SmilePlus} />
      <div className="my-4 flex h-full items-center justify-center">
        <div className="grid w-full grid-cols-1 gap-6">
          {customerSatisficationOptions.map((option) => (
            <LinearProgress
              key={option.label}
              label={option.label}
              color={option.color}
              percentage={option.percentage}
              icon={option.icon}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
