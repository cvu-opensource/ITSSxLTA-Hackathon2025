export type ChatRole = "LTA" | "ITSS";

export interface HighwayChat {
  highway: string;
  conversation: { role: ChatRole; message: string }[];
}

export const highwayChats: HighwayChat[] = [
  {
    highway: "PIE",
    conversation: [
      { role: "LTA", message: "We observed severe congestion near the Toa Payoh exit during peak hours." },
      { role: "ITSS", message: "Adaptive traffic lights could help reduce bottlenecks in that area." },
      { role: "LTA", message: "We've tried re-routing buses, but cars still dominate the flow." },
      { role: "ITSS", message: "How about AI-driven carpool matching for frequent commuters?" },
    ],
  },
  {
    highway: "CTE",
    conversation: [
      { role: "LTA", message: "CTE sees the highest occupancy every weekday from 7-9am." },
      { role: "ITSS", message: "Could we integrate predictive congestion alerts to advise alternate routes?" },
      { role: "LTA", message: "That may need coordination with Waze/Google." },
      { role: "ITSS", message: "We could prototype a dashboard with historical congestion heatmaps first." },
    ],
  },
  {
    highway: "AYE",
    conversation: [
      { role: "LTA", message: "Roadwork near Jurong is slowing things down." },
      { role: "ITSS", message: "Real-time diversion plans could reduce stress on adjacent segments." },
    ],
  },
];
