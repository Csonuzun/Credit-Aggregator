import React, { useEffect, useState } from "react";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";

export function ThemeToggle() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    const html = document.documentElement;
    if (isDarkMode) {
      html.classList.add("dark");
    } else {
      html.classList.remove("dark");
    }
  }, [isDarkMode]);

  return (
      <div className="flex items-center space-x-2">
        <Switch
            onClick={() => setIsDarkMode((prev) => !prev)}
            className="bg-card-foreground text-card rounded-lg">
        </Switch>
        <Label htmlFor="theme">
            {isDarkMode ? "Dark" : "Light"} Mode
        </Label>

      </div>

  );
}
