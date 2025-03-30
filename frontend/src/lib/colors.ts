export function getColor(name: string): string {
    const colors: Record<string, string> = {
      primary: "#3b82f6", // Tailwind's blue-500
      success: "#10b981",
      danger: "#ef4444",
      warning: "#f59e0b",
      neutral: "#6b7280",
    };
  
    return colors[name] || colors.neutral;
  }
  